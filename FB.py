import urllib.request as urllib2
import json
from constants import fb_api_key


def get_page_data(page_id, access_token):
    api_endpoint = "https://graph.facebook.com/v5.0/"
    fb_graph_url = api_endpoint + page_id + "?fields=id,name,likes,link&access_token=" + access_token
    try:
        api_request = urllib2.Request(fb_graph_url)
        api_response = urllib2.urlopen(api_request)

        try:
            return json.loads(api_response.read())
        except (ValueError, KeyError, TypeError):
            return "JSON error"

    except IOError as e:
        if hasattr(e, 'code'):
            return e.code
        elif hasattr(e, 'reason'):
            return e.reason


pages = "medipragma"  # username or id
page_data = get_page_data(pages, fb_api_key)
print(page_data)
# print ("Page Name:" + page_data['name'])
# print ("Likes:" + str(page_data['likes']))
# print ("Link:" + page_data['link'])
