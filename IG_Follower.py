#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
import csv


class Insta_Info_Scraper:

    def getinfo(self, url):
        html = urllib.request.urlopen(url, context=self.ctx).read()
        soup = BeautifulSoup(html, 'html5lib')
        data = soup.find('body')
        script_tag = data.find('script')
        raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
        json_data = json.loads(raw_string)
        print(json_data['entry_data']['ProfilePage'][0]['graphql']['user']['full_name'])

        info = {}
        if json_data['entry_data']['ProfilePage'][0]['graphql']['user']['full_name'] :
            info['Name'] = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['full_name']
        else:
            info['Name'] ="No_Name"
        info["Username"] = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['username']
        info["Followers"] = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_followed_by']['count']
        info["Following"] = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_follow']['count']
        info["Posts"] = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['count']
        self.info_arr.append(info)
        with open('IG.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([
                info['Name'], info["Username"],info["Followers"],
                info["Following"], info["Posts"]
            ])

    def main(self):

        with open('IG.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Username', 'Followers', 'Following', 'Posts'])
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE
        self.info_arr = []

        with open('IG.txt') as f:
            self.content = f.readlines()

        self.content = [x.strip() for x in self.content]
        for url in self.content:
            self.getinfo(url)

        with open('IG.json', 'w') as outfile:
            json.dump(self.info_arr, outfile, indent=4)
        print("Json file containing required info is created............")


if __name__ == '__main__':
    obj = Insta_Info_Scraper()
    obj.main()