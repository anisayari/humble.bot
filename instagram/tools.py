# coding=utf-8

import time
import sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from config import sender, to , sender_pwd
from config import my_username,my_pwd,my_user_id, file_data
import os
import csv
from InstagramAPI import InstagramAPI

def check(json, status):
    if json['status'] == 'fail':
        send_email('ALERT API', 'cannot '+status+' feed')

    else:
        return True

def like(API,media, like_count):
    try:
        API.like(media['caption']['media_id'])
        response = API.LastJson
        if check(response, status='like'):
            like_count += 1
    except:
        pass
    response = API.LastJson
    if check(response, status='like'):
        like_count += 1
    return API, media, like_count

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
    os.exit(1)

def check_block():
    API.getSelfUserFeed(maxid=1)
    json = API.LastJson
    media = json['items'][1] #try to like one picture
    while True:
        API.like(media['caption']['media_id'])
        response = API.LastJson
        print "check...."
        if response['status'] == 'fail':
            print "check fail"
            sleep(60*60)
        else:
            API.unlike(media['caption']['media_id'])
            print "check ok"
            send_email('CONGRATS LIKE UNBLOCKED', 'You can launch again the script and enjoy like')
            return

def init_header(file, reset=False):
    if reset:
        f = open(file, "w+")
        f.close()
        data=['time','name','liked','followed']
        save_data(data,file)

def save_data(data, file):
    with open(file , 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def unfollow(data_file):
    username = my_username
    pwd = my_pwd
    user_id = my_user_id
    API = InstagramAPI(username, pwd)
    API.login()
    API.getUserFollowings(user_id, maxid=True)
    followers_dict= API.LastJson.get('users', [])
    followers_list = []
    for item in followers_dict:
        followers_list.append(item['username'])
    print 'Unfollow from file'
    with open(data_file, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] in followers_list and row[4] == str(1):
                API.unfollow(userId=str(row[2]))
                print str(row[1]) + " unfollowing."
                sleep(50)