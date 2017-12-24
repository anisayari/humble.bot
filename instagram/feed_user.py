import csv

from InstagramAPI import InstagramAPI
from config import my_user_id , TRASH_username, TRASH_user_id, TRASH_pwd


def follow_me():
    with open('data_feeded.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        i = 0
        info_generate = {}
        for row in reader:
            info_generate[i] = {}
            info_generate[i]['username'] = row[0]
            info_generate[i]['password'] = row[1]
            info_generate[i]['email'] = row[2]
            info_generate[i]['full_name'] = row[3]
            info_generate[i]['user_id'] = row[3]
            username = info_generate[i]['username']
            pwd = info_generate[i]['password']
            user_id = info_generate[i]['user_id']
            API = InstagramAPI(username, pwd)
            try:
                API.login()
                API.follow(my_user_id)
                print API.LastJson
            except: continue
            i += 1

def main():
    with open('data.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        i=0
        info_generate = {}
        for row in reader:
            info_generate[i]={}
            info_generate[i]['username'] = row[0]
            info_generate[i]['password'] = row[1]
            info_generate[i]['email'] = row[2]
            info_generate[i]['full_name'] = row[3]
            i+=1

    username = TRASH_username
    pwd = TRASH_pwd
    user_id = TRASH_user_id
    API = InstagramAPI(username, pwd)
    API.login()
    info_generate_tmp ={}

    i=0

    count_user_found  = 0
    count_user_no_found  = 0
    for item in info_generate.values():
        while True:
            API.searchUsername(item['username'])
            request = API.LastJson
            if 'message' in request.keys():
                if request['message'] == "Please wait a few minutes before you try again.":
                    print "change user"
                    username = info_generate_tmp[i - 1]['username']  # Take the last know user
                    pwd = info_generate_tmp[i - 1]['password']
                    user_id = info_generate_tmp[i - 1]['user_id']
                    API = InstagramAPI(username, pwd)
                    API.login()
                    print "retry...."
                    break
            else:
                if request['status'] == "ok":
                    info_generate_tmp[i]['user_id'] = request['user']['pk']
                    print 'User found'
                    count_user_found += 1
                    i += 1
                    info_generate_tmp[i] = item
                else:
                    print request['message']
                    count_user_no_found += 1


    print '-----TOTAL-----'
    print count_user_found, ' User OK'
    print count_user_found, ' User FAIL'
    print '---------------'

    print "Start save data"
    with open('data_feeded.csv', 'a') as f:
        w = csv.writer(f, delimiter=',',lineterminator='\n')
        for row in info_generate_tmp.values():
            if row['user_id']!= None:
                w.writerow([str(row['username']), row['password'], row['email'] ,row['full_name'], row['user_id']])

    print "Data saved"

follow_me()