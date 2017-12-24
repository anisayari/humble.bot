#humble instagram bot
#Anis Ayari


from InstagramAPI import InstagramAPI
import time
import sys
#from genderize import Genderize
from tools import sleep, send_email, save_data, init_header
from config import my_username,my_pwd,my_user_id, file_data
import os
import random
import time

def check_block():
    API.getSelfUserFeed(maxid=1)
    json = API.LastJson
    media = json['items'][1] #try to like one picture
    os._exit(1)
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



def open_file(file_name):
    file = open(file_name, "r")
    return file

def write_in_file(file_name, to_write):
    file_name.write(to_write)


def main(API):
    init_header(file_data, reset=False)
    response = API.LastJson
    if response['status'] == 'fail':
        try:
            send_email(str(response['error_type']), str(response['error_title']) + ' ' + str(response['message']))
        except:
            print "Unexpected error:", sys.exc_info()[0]
            print 'Fail send email , ending process'
        os._exit(1)
    t0 = time.clock()
    count_follower = 0
    like_count = 0
    reset_count = 0
    count_error =  0
    fail = 0
    for i in range(0,100):
        if i%2 != 0:
        #if False:
            choice = 'popular'
            print "popular feed"
            if fail == 5:
                try:
                    send_email('ALERT API','cannot get feed')
                    os._exit(1)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    print 'Fail send email , ending process'
                    os._exit(1)
            try:
                API.getPopularFeed()
                json = API.LastJson
            except:
                print "Unexpected error:", sys.exc_info()[0]
                print 'ERROR call API for '+choice
                sleep(20)
                fail +=1
                continue
            max = 100
        else:
            choice = "hastags"
            print "hastag feed"
            try:
                API.getHashtagFeed('french')
                json = API.LastJson
            except:
                print "Unexpected error:", sys.exc_info()[0]
                print 'ERROR call API for'+choice
                sleep(20)
                fail +=1
                continue
            max = 100
        fail = 0
        #for media in json['items'][0:max]:
            #sleep(3)
        for media in json['items']:
            if choice == 'hastags' :
                try:
                    '''try:
                        followers_number = len(API.getTotalFollowers(media['caption']['user_id']))
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        response = API.LastJson
                        if response['status'] == 'fail':
                            try:
                                send_email(u' '.join((response['status'])).encode('utf-8').strip(),
                                           u' '.join((response['message'])).encode('utf-8').strip())
                            except:
                                print "Unexpected error:", sys.exc_info()[0]
                                print 'Fail send email , ending process'
                            os._exit(1)'''
                    followers_number = 101
                    #if not media['user']['full_name'] != '':
                        #continue
                    #name = str(media['user']['full_name']).rsplit()[0]
                    #response = Genderize().get([name])
                    #if followers_number < 100 or response[0]['gender'] != 'female' or media['like_count'] < 10:# condition on followers user, condition on media like
                    if media['like_count'] < 5:# condition on followers user, condition on media like
                        #print 'FAIL: ', media['user']['full_name'],followers_number ,' followers, ',response[0]['gender'],', ', media['like_count'], ' Likes'
                        count_error += 1
                        continue
                    else:
                        #print name, ' ', response[0]['gender'], '\x1b[1;37;42m' + 'OK' + '\x1b[0m'
                        print(str(media['like_count']) + ' like on this publication OK')
                        print 'SUCESS after ' + str(count_error) + ' trial'
                        count_error = 0
                except UnicodeEncodeError:
                    print media['user']['full_name'],' Bad format'
                    count_error += 1
                    continue
            else:
                print 'no verification'
            try:
                data = []
                '''
                name = str(media['user']['full_name']).rsplit()[0]
                    response = Genderize().get([name])
                    if response[0]['gender'] != 'female' or media['like_count'] < 10:# condition on followers user, condition on media like

                if not media['like_count'] < 5:
                    pass
                '''

                print 'USER : https://instagram.com/'+str(media['user']['username'])
                API.like(media['caption']['media_id'])
                response= API.LastJson
                if response['status'] == 'fail':
                    try:
                        send_email('LIKE BLOCKED',
                               'Cannot lik post')
                        check_block()
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        print 'Fail send email , ending process'
                else:
                    like_count += 1
                print str(media['image_versions2']['candidates'][0]['url']) + ' liked !'
                liked = 1
                API.getUserFeed(media['caption']['user_id'])
                feed = API.LastJson
                if len(feed)>5:
                    for media_feed in feed['items'][4:5]:
                        API.like(media_feed['caption']['media_id'])
                        if response['status'] == 'fail':
                            '''try:
                                send_email('LIKE BLOCKED',
                                           'Cannot lik post')
                                check_block()
                            except:
                                print "Unexpected error:", sys.exc_info()[0]
                                print 'Fail send email , ending process'''
                            continue
                        else:
                            like_count += 1
                        print str(media_feed['image_versions2']['candidates'][0]['url']) + ' liked !'
                        liked = 2
                if reset_count == 10:
                    API.follow(media['caption']['user_id'])
                    print str(media['user']['username']) + ' followed!'
                    count_follower += 1
                    reset_count = 0
                    followed = 1
                else:
                    followed= 0
                timed = str(time.strftime("%d/%m/%Y"))+str(time.strftime("%H:%M:%S"))
                data = [timed,media['user']['username'],media['caption']['user_id'], liked, followed, choice]
                save_data(data,file_data)
                print 'number: ' + str(count_follower)
                print 'Security break ON...'
                time_process = (time.clock() - t0)/60.
                print '%.2f min since the beginning' % time_process
                print str(count_follower) + ' users followed'
                print str(like_count) + ' media liked'
                sleep(2*(30+random.randint(1,10)))
                print '\nSecurity break OFF'
                print 'count: '+str(reset_count)+'/7'
                reset_count += 1
            except:
                print "Unexpected error:", sys.exc_info()[0]
                continue

if __name__ == '__main__':
    username = my_username
    pwd = my_pwd
    user_id = my_user_id
    API = InstagramAPI(username, pwd)
    API.login()
    main(API)