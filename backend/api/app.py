from datetime import datetime
from dotenv import load_dotenv
import os

from flask import Flask
from flask_mailman import Mail, EmailMessage
from celery import Celery
from celery.schedules import crontab

from repo import get_due_reminders

load_dotenv()

app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Celery configuration
app.config['broker_url'] = 'sqla+sqlite:///celery.sqlite'
app.config['result_backend'] = 'db+sqlite:///results.sqlite'

mail = Mail(app)
celery = Celery(app.name, broker=app.config['broker_url'])
celery.conf.update(app.config)

def send_reminder_mail(to, message):
    with app.app_context():
        msg = EmailMessage(
            "Subject of the mail",
            message,
            from_email="manjushreeroshan@gmail.com",
            to=[to]
        )
        msg.send()

@celery.task
def check_reminders():
    print("Checking reminders...")
    with app.app_context():
        for reminder in get_due_reminders():
            send_reminder_mail(reminder.email, reminder.message)
            print(f"Reminder mail sent to: {reminder.email}")
    return "Reminders checked and sent"

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(300.0, check_reminders.s(), name='check reminders every 5 minutes')

@app.route('/')
def hello():
    return "Hello! The reminder checking task is running in the background."

if __name__ == '__main__':
    app.run(debug=True)