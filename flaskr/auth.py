import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email=request.form['email']

        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password,email) VALUES (?, ?,?)',
                (username, generate_password_hash(password),email)
            )
            db.commit()
            return redirect(url_for('auth.index'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('auth.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/')
def index():
    db = get_db()
    students = db.execute(
        'SELECT id,username,email,registered'
        ' FROM user'
        ' ORDER BY username '
    ).fetchall()
    return render_template('auth/index.html', students=students)


def get_student(id, check_author=True):
    student = get_db().execute(
        'SELECT id, username,email,registered'
        ' FROM user'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if student is None:
        abort(404, "Student id {0} doesn't exist.".format(id))

    if check_author and student['id'] != g.user['id']:
        abort(403)

    return student

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    student = get_student(id)

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        error = None

        if not username:
            error = 'Username is required.'
        if not email:
            error = 'email is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE user SET  username = ?, email = ?'
                ' WHERE id = ?',
                (username, email, id)
            )
            db.commit()
            return redirect(url_for('auth.index'))

    return render_template('auth/update.html', student=student)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_student(id)
    db = get_db()
    db.execute('DELETE FROM user WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('auth.index'))