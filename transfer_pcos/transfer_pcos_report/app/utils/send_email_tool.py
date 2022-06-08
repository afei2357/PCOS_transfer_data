from threading import Thread
from flask import current_app
from flask_mail import Message,Mail
#from flaskext.mail import Mail
from app import create_app
from app.configs.config import Config 

#app = current_app.__get_current_object()
app = create_app(Config)
mail = Mail(app)

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body,
        attachments=None, sync=False):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()



