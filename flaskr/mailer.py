import smtplib
from flask_mail import MIMEMultipart,MIMEText


class Mail():

    def __init__(self,to_list,from_line,class_loc,class_date,class_msg,class_link):
        self.to_list = to_list
        self.class_loc = class_loc
        self.class_date = class_date
        self.class_msg = class_msg
        self.class_link  = class_link
        self.msg = MIMEMultipart('alternative')
        self.from_line  = from_line


    def send_mail(self):

        server = smtplib.SMTP("sendsmtp.seagen.com")

        to_line = ', '.join(self.to_list)
        from_line = self.from_line

        self.msg['From']=self.from_line
        self.msg['To']= to_line
        self.msg['Subject']=f"Python Training in {self.class_loc} on {self.class_date}"

        text = "<h4 style='color: green'>Python Training</h4>"
        text += f"<p>{self.class_msg}</p>"
        text += "<hr/>"
        text += f'<a href="{self.class_link}">Assignments</a>'

        html = MIMEText(text,'html')

        self.msg.attach(html)

        server.sendmail(self.from_line,self.to_list,self.msg.as_string(),)


