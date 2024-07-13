from flask import Flask, jsonify, request
import re
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from datetime import datetime
from celery_utils import get_celery_app_instance

load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# celery app instance
celery = get_celery_app_instance(app)

@celery.task
def send_email(to_email):
    from_email = os.getenv('SMTP_USER')
    from_password = os.getenv('SMTP_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')
    subject = 'Messaging System with RabbitMQ, Celery and Python Application Test Email'
    body = 'Testing the python application.'
    msg = MIMEMultipart()
    msg['From'] = os.getenv('SMTP_FROM')
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, from_password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
            return True
    except Exception:
            return False

@app.route('/', methods=['GET'])
def main():
    # check if sendmail is passed in the url query
    if 'sendmail' in request.args:
        email = request.args.get('sendmail')
        if email == "":
            return jsonify({'error': 'expected a params for sendmail' })
        
        # check if its valid email
        if check(email) == False:
            return jsonify({'error': 'params passed must be a valid email address' })

        # send email
        if send_email.delay(email):
            return jsonify({'success': 'sent email to: ' + email })
        else:
            return jsonify({'error': 'failed to send email to: ' + email })

    # check if talktome is passed in the url query
    if 'talktome' in request.args:
            return jsonify({'success': 'logged the current time'})

    return """<html>
    <h2>Messaging System with RabbitMQ/Celery and Python Flask Application, deployed behind Nginx</h2>
    <p>You can send an email by using ?sendmail=yourEmail@gmail.com</p>
    <em>E,g http://127.0.0.1:5000?sendmail=yourEmail@gmail.com'</em>
    <br><br>
    <p>You can log the current time by using</p>
    <em>E,g http://127.0.0.1:5000?talktome'</em>
    </html>"""

# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

# Define a function for
# for validating an Email
def check(email):
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
 
    else:
        return False
    
def log():
    file_folder = './var/logs/'
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)
    file_path = "./var/logs/messaging_system.log"
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
  
    s = open(file_path, 'a')
    s.write('Current time: ' + current_time + '\n')