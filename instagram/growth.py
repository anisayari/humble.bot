#humble instagram bot
#Anis Ayari


import random
import time

from InstagramAPI import InstagramAPI
from config import my_username,my_pwd,my_user_id
from tools import sleep,  check_block, like, check


def main(API):
    response = API.LastJson
    check(response, status= 'get API')
    t0 = time.clock()
    count_follower = 0
    like_count = 0
    reset_count = 0
    count_error =  0
    for i in range(0,100):
        if i%2 != 0:
            choice = 'popular'
            print "popular feed"
            API.getPopularFeed() #APPEL API
            json = API.LastJson
            check(json, status='popular feed')
            max = 100
        else:
            choice = "hastags"
            print "hastag feed"
            API.getHashtagFeed('french')#APPEL API
            json = API.LastJson
            check(json, status='hastags feed')
            max = 100
        for media in json['items'][0:max]:
            sleep(3)
            if choice == 'hastags':
                if media['like_count'] < 5:
                    print 'Likes inf to 5'
                    count_error += 1
                else:
                    print(str(media['like_count']) + ' like on this publication OK')
                    print 'SUCESS after ' + str(count_error) + ' trial'
                    count_error = 0
            else:
                print 'no verification'
            print 'USER : https://instagram.com/'+str(media['user']['username'])
            like(API=API,media=media, like_count=like_count)
            print str(media['image_versions2']['candidates'][0]['url']) + ' liked !'
            API.getUserFeed(media['caption']['user_id']) #APPEL API
            feed = API.LastJson
            for media_feed in feed['items'][4:5]:
                like(API=API, media=media_feed, like_count=like_count)
                print str(media_feed['image_versions2']['candidates'][0]['url']) + ' liked !'
                if reset_count == 10:
                    API.follow(media['caption']['user_id'])
                    print str(media['user']['username']) + ' followed!'
                    count_follower += 1
                    reset_count = 0
                print 'number: ' + str(count_follower)
                print 'Security break ON...'
                time_process = (time.clock() - t0)/60.
                print '%.2f min since the beginning' % time_process
                print str(count_follower) + ' users followed'
                print str(like_count) + ' media liked'
                sleep(60+random.randint(1,10))
                print '\nSecurity break OFF'
                print 'count: '+str(reset_count)+'/7'
                reset_count += 1

if __name__ == '__main__':
    username = my_username
    pwd = my_pwd
    user_id = my_user_id
    API = InstagramAPI(username, pwd)
    API.login()
    main(API)



