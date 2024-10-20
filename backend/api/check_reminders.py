from datetime import datetime
from dotenv import load_dotenv
import os

from flask import Flask
from flask_mailman import Mail, EmailMessage

load_dotenv()

# from flask_sqlalchemy import SQLAlchemy

mail = Mail()
app = Flask(__name__)

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail.init_app(app)

# def send_reminder_mail(to,message):
#     msg = EmailMessage(
#         "Subject of the mail",
#         "Body of the mail",
#         from_email="manjushreeroshan@gmail.com",
#         to=["levo@mailinator.com"]
#     )
#     msg.send()


def check_reminders():
    # now = datetime.now()
    # due_reminders =  'asdasdd'

    # for reminder in due_reminders:
    #     send_reminder_mail(reminder.email, reminder.message)
    #     db.sesssion.delete(reminder)
    #     db.sessio.commit()

    msg = EmailMessage(
        "Subject of the mail",
        "Body of the mail",
        from_email="manjushreeroshan@gmail.com",
        to=["levo@mailinator.com"]
    )
    msg.send()

if __name__ == '__main__':
    with app.app_context():
        check_reminders()
