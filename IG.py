from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import scrapy
from scrapy.selector import Selector
import time
import random
import sys
import constants
import csv
import re
from datetime import date, datetime
import sys
from googletrans import Translator
from langdetect import detect, DetectorFactory
import numpy as np
from webdriver_manager.chrome import ChromeDriverManager

def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()


class InstagramBot:

    def __init__(self, username1, password1):
        self.username = username1
        self.password = password1
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def closebrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(2)
        #login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        #login_button.click()
        time.sleep(2)
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
        passworword_elem.clear()
        passworword_elem.send_keys(self.password)
        passworword_elem.send_keys(Keys.RETURN)
        time.sleep(2)

    def find_hashtags(self, pic_href):
        driver = self.driver
        scrapy_selector = Selector(text=driver.page_source)

        try:

            time_stamp = scrapy_selector.xpath('//time[@class="_1o9PC Nzb55"]/@datetime').extract_first()
            date_time_obj = datetime.strptime(time_stamp, '%Y-%m-%dT%H:%M:%S.%fZ')

            if date_time_obj.month >= 9:
                post = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span").get_attribute('textContent')

                post = re.sub(r"https?://[A-Za-z0-9./]*", " ", post)
                post = re.sub(r"[^a-zA-Z#]", " ", post)
                hsh = re.findall(r"#[a-zA-Z]+", post)
                for item in hsh:
                    post = post.replace(item, "")
                post = " ".join(post.split())
                print(post)
                print(hsh)

                influencer = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div[3]/div[1]/ul/div/li/div/div/div[2]/h2/div/span/a").get_attribute('textContent')

                print(influencer)
                if detect(post.lower()) == 'en':
                    print('EN')
                    with open('Hashtags.csv', 'a', encoding='utf-8-sig') as f1:
                        writer4 = csv.writer(f1)
                        for item in hsh:
                            # post = post.strip()
                            writer4.writerow([item.strip('#').lower()])

                    with open('Influencer.csv', 'a', encoding='utf-8-sig') as f2:
                        writer3 = csv.writer(f2)
                        writer3.writerow([influencer, hsh, post])
                else:
                    blacklist.add(pic_href)
            else:
                return

        except Exception as exp:
            print(exp)

    def like_photo(self, hashtag):
        driver = self.driver
        time.sleep(2)
        print('1')
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        print('2')
        time.sleep(2)

        # gathering photos until a certain date
        pic_hrefs = []
        check = 1

        while check:
            try:
                for i in range(3):
                    time.sleep(random.randint(4, 6))
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(random.randint(3, 4))
                    # scroll_from += scroll_limit

                    # get tags
                    hrefs_in_view = driver.find_elements_by_tag_name('a')

                    # finding relevant hrefs
                    hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                     if '.com/p/' in elem.get_attribute('href')]
                    # building list of unique photos
                    [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                    # print(pic_hrefs)
                    # print("Check: pic href length " + str(len(pic_hrefs)))
                pic_href = pic_hrefs[-1]
                print(pic_href)
                # open tab
                # You can use (Keys.CONTROL + 't') on other OSs
                curwindowhndl = driver.current_window_handle
                # open link in new tab keyboard shortcut
                driver.execute_script('''window.open("about:blank", "_blank");''')
                driver.switch_to.window(driver.window_handles[1])  # assuming new tab is at index 1
                # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.ENTER)
                time.sleep(1)  # wait until new tab finishes loading
                # Load a page
                driver.get(pic_href)
                time.sleep(random.randint(1, 2))
                # Make the tests...
                scrapy_selector = Selector(text=driver.page_source)
                time_stamp = scrapy_selector.xpath('//time[@class="_1o9PC Nzb55"]/@datetime').extract_first()
                date_time_obj = datetime.strptime(time_stamp, '%Y-%m-%dT%H:%M:%S.%fZ')
                print(date_time_obj.month)
                print(date_time_obj.day)
                if date_time_obj.month < 7:
                    # print(date_time_obj.month)
                    check = 0
                driver.close()  # closes new tab
                driver.switch_to.window(curwindowhndl)
                time.sleep(random.randint(2, 3))

                # close the tab
                # (Keys.CONTROL + 'w') on other OSs.
                # driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')

            except Exception as exp:
                print(exp)
                continue

        # Liking photos
        unique_photos = len(pic_hrefs)
        for pic_href in pic_hrefs:
            if pic_href not in blacklist:
                print(pic_href)
                driver.get(pic_href)
                time.sleep(random.randint(2, 4))
                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                try:
                    time.sleep(random.randint(2, 4))
                    ig.find_hashtags(pic_href)
                    #print(description)
                    driver.find_element_by_xpath("//section/span/button/div/span[*[local-name()='svg']/@aria-label='Like']").click()
                    #like_button = lambda: driver.find_element_by_xpath(" //button[normalize-space(@class)='wpO6b']/*[name()='svg']")
                    #like_button().click()
                    for second in reversed(range(0, random.randint(22, 28))):
                       print_same_line("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                                       + " | Sleeping " + str(second))
                       time.sleep(random.randint(1, 2))
                except Exception as exp:
                    print(exp)
                    time.sleep(2)
                unique_photos -= 1

    def finish(self):
        driver = self.driver
        driver.quit()


if __name__ == "__main__":
    translator = Translator()

    """with open('Influencer.csv', 'w', encoding='utf-8-sig') as f:
        writer2 = csv.writer(f)
        writer2.writerow(['Influencer', 'Hashtags', 'Post'])

    with open('Hashtags.csv', 'w', encoding='utf-8-sig') as f:
        writer1 = csv.writer(f)
        writer1.writerow(['Hashtag'])"""

    username = constants.username2
    password = constants.password2

    ig = InstagramBot(username, password)
    ig.login()
    blacklist = set()
    hashtags = ['happy']
    # while check:
    try:
        # Choose a random tag from the list of tags
        tag = random.choice(hashtags)
        ig.like_photo(hashtags[0])
        ig.finish()
    except Exception as e:
        print(e)
        ig.closebrowser()
        time.sleep(60)
        ig = InstagramBot(username, password)
        ig.login()
