import time
import sys
# coding=utf-8
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from config import sender, to , sender_pwd


def sleep(num): #300 like max / per hour and 20 follow / hour
    for i in range(0,num):
        time.sleep(1)
        sys.stdout.write("\r%i sc / %i sc " % (i,num))
        sys.stdout.flush()


def send_email(type, message_to_send):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = to
    msg['Subject'] = 'Humble bot instagram - '+ str(type)
    msg.attach(MIMEText('Hello Anis, this is me, your bot ! I have to say you that : ' + str(message_to_send), 'plain'))
    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(sender, sender_pwd)
    mailserver.sendmail(sender, to, msg.as_string())
    print 'message to '+str(to)+ ' sent !'
    mailserver.quit()