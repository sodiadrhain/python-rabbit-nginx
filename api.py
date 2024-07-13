from datetime import datetime
from email.mime.text import MIMEText
import os
from flask import Flask, jsonify, request
import re
import smtplib

app = Flask(__name__)

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
    
def send_email(email):
    # creates SMTP session
    s = smtplib.SMTP('smtp-relay.brevo.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login("77f7d0001@smtp-brevo.com", "PzNOXcDgthU8JnQI")

    # send message
    message = "\r\n".join([
  "From: Soji <adesojiawobajo@gmail.com>",
  "To: sodiadrhain@gmail.com",
  "Subject: Messaging System with RabbitMQ test email",
  "",
  "Good Evening, how are you?"
  ])
    # # Create MIMEText object
    # message = MIMEText(text, "plain")
    # message["Subject"] = "Messaging System with RabbitMQ test email"
    # sending the mail
    s.sendmail(from_addr='sodiadrhain1@gmail.com', to_addrs='sodiadrhain@gmail.com', msg=message)
    s.close()


def log():
    file_folder = './var/logs/'
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)
        
    file_path = "./var/logs/messaging_system.log"
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
  
    s = open(file_path, 'a')
    s.write(current_time + "\n")

@app.route('/', methods=['GET'])
def get_request():

# check if sendmail is passed in the url query
    if 'sendmail' in request.args:
        email = request.args.get('sendmail')
        if email == "":
            return jsonify({'error': 'expected a params for sendmail' })
        
        # check if its valid email
        if check(email) == False:
            return jsonify({'error': 'params passed must be a valid email address' })
        
        # send email
        send_email_res = send_email(email)
        if send_email_res != None: 
            return jsonify({'error': 'failed to send email, error: '+ send_email_res })
    
        return jsonify({'success': 'email sent successfully to: ' + email })

# check if talktome is passed in the url query
    if 'talktome' in request.args:
        log()
        return jsonify({'success': 'logged the current time'})
    
# no params passed
    return jsonify({'error': 'no query passed, kindly pass sendmail to send a mail or talktome'})

if __name__ == '__main__':
    app.run()