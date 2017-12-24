import imageio

imageio.plugins.ffmpeg.download()

from InstagramAPI import InstagramAPI
from tools import sleep
from config import my_username,my_pwd,my_user_id


username = my_username
pwd = my_pwd
user_id = my_user_id

following_list = []
followers_list = []

API = InstagramAPI(username, pwd)
API.login()

API.getUsernameInfo(user_id)
following = []
next_max_id = True
while next_max_id:
    if next_max_id == True: next_max_id = ''
    _ = API.getUserFollowings(user_id, maxid=next_max_id)
    following.extend(API.LastJson.get('users', []))
    next_max_id = API.LastJson.get('next_max_id', '')

len(following)
unique_following = {
    f['pk']: f
    for f in following
}
len(unique_following)
following_dict = {}
count = 0
for user in following:
    following_list.append(user['username'])
    following_dict[user['username']] = user['pk']
    count += 1
print str(count) + ' following'

followers = []
next_max_id = True
while next_max_id:
    if next_max_id == True: next_max_id = ''
    _ = API.getUserFollowers(user_id, maxid=next_max_id)
    followers.extend(API.LastJson.get('users', []))
    next_max_id = API.LastJson.get('next_max_id', '')

len(followers)
unique_following = {
    f['pk']: f
    for f in followers

}

len(unique_following)
count = 0
for user in followers:
    followers_list.append(user['username'])
    count += 1
print str(count) + ' followers'

count_unfollower = 0
for user_following in following_list:
    if user_following not in followers_list:
        count_unfollower += 1
        print str(user_following) + " doesn't follow you."

        API.unfollow(userId=following_dict[user_following])
        print str(user_following) + " unfollowing."
        #sleep(3*70)

print count_unfollower," Unfollowers"