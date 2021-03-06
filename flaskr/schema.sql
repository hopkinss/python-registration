DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  registered TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  password TEXT NOT NULL
);