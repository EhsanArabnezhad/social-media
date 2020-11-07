# Get instance
import instaloader
import constants
L = instaloader.Instaloader()

# Login or load session
L.login(constants.username3, constants.password3)

# Obtain profile metadata
profile = instaloader.Profile.from_username(L.context, "programmers_fun_official")

follower_list = []
following_list = []
count = 0

for followee in profile.get_followers():
    username = followee.username
    follower_list.append(username)
print(len(follower_list))

for following in profile.get_followees():
    username = following.username
    following_list.append(username)
print(len(following_list))

diff_list = [x for x in following_list if x not in follower_list]

with open('following_but_not_follower.txt', 'a') as file:
    for member in diff_list:
        file.write(member + '\n')
