import urllib.request as ul
import json
import constants
import csv
# name=input("Enter username: ")
key = constants.youtube_API_key

with open('yt.txt') as source:
	f = source.read().splitlines()
	all_yt_user = [element for element in f]

with open('youtube_followers.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Username', 'Subscriptors'])


for username in all_yt_user:
    print(username)
    try:
        data = ul.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername="+username+"&key="+key).read()
        data2 = ul.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&id="+username+"&key="+key).read()
        if json.loads(data)["items"]:
            print(json.loads(data))
            subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
            with open('youtube_followers.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([username,subs])

            print(username + " has " + "{:,d}".format(int(subs)) + " subscribers!")
        elif json.loads(data2)["items"]:
            print(json.loads(data2))
            subs = json.loads(data2)["items"][0]["statistics"]["subscriberCount"]
            with open('youtube_followers.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([username,subs])
            print(username + " has " + "{:,d}".format(int(subs)) + " subscribers!")
    except Exception as e:
        print(e)
