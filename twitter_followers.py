import time
from twython import Twython
import json
import constants
import csv
# insert your Twitter keys here
API_KEY = constants.API_KEY
API_SECRET = constants.API_SECRET
ACCESS_TOKEN = constants.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = constants.ACCESS_TOKEN_SECRET

twitter = Twython(API_KEY, API_SECRET,
                  ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

content = []

with open('followers_tweets.csv', 'w') as f:
	writer = csv.writer(f)
	writer.writerow(['Name', 'Username', 'Followers', 'Following', 'Posts'])

with open('twitter.txt') as source:
	f = source.read().splitlines()
	all_dream_user = [element for element in f]

for username in all_dream_user:
	print(username)
	try:
		result = twitter.show_user(screen_name=username)
		print(result)
		# user_timeline = twitter.get_user_timeline(screen_name=username, count=100000)
		json_dict = {}
		# follower_from_TMG_reddit = []
		json_dict['Name'] = result['name']
		json_dict['Screen_Name'] = result['screen_name']
		json_dict['Follower'] = result['followers_count']
		print(json_dict['Follower'])
		json_dict['Following'] = result['friends_count']
		json_dict['Tweet_no'] = result['statuses_count']
		with open('followers_tweets.csv', 'a') as f:
			writer = csv.writer(f)
			writer.writerow([json_dict['Name'], json_dict['Screen_Name'], json_dict['Follower'], json_dict['Following'], json_dict['Tweet_no']])
		content.append(json_dict)

	except Exception as e:
		time.sleep(120)

with open('followers_tweets.txt', 'w') as outfile:
	json.dump(content, outfile,indent=4)

