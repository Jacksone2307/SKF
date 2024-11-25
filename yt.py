import os
import requests
import google_auth_httplib2
import googleapiclient
import googleapiclient.discovery
import googleapiclient.errors
import google_auth_oauthlib.flow
import json
from googlesearch import search
import re
import webbrowser
import multiprocessing

API_KEY = "AIzaSyBkOjW6lPXQ23EbK-5NJ3NuiDUaSDFuemE"


scopes = ["https://www.googleapis.com/auth/youtube",
          "https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtubepartner"]


def remove_html_tags(text):
    """Remove html tags from a string"""

    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# class DataLoader:
#     def __init__(self, api_url, api_key):
#         self.api_url = api_url
#         self.api_key = api_key

#     def load_data(self, params):
#         # Make API call using self.api_url and self.api_key
#         # Return the loaded data
#         response = requests.get(self.api_url, params=params)
#         return response.json()
    



yt_search_url = "https://www.googleapis.com/youtube/v3/search"


def search_and_open_video(qry):
    for i in search(qry, num=1, stop=1):
            webbrowser.open(i)

def search_and_display_key(qry):
    for i in search(qry, num=1, stop=1):
            r = requests.get(i)
            text = remove_html_tags(str(r.content))
            key = re.search('with a ([A-G]) key and a (.*) mode', text)
            print(key.group(1), key.group(2))

def main():
    qry_input = str(input("Search for: "))
    while qry_input != "":
        yt_query = qry_input + " youtube"
        p1 = multiprocessing.Process(target=search_and_open_video, args=(yt_query, ))
        
        google_query = qry_input + " songbpm key"
        p2 = multiprocessing.Process(target=search_and_display_key, args=(google_query, ))
        p1.start()
        p2.start()
        p2.join()
        p1.join()
        qry_input = str(input("Search for: "))
        


    


    


if __name__ == "__main__":
    main()