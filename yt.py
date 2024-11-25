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

API_KEY = "AIzaSyBkOjW6lPXQ23EbK-5NJ3NuiDUaSDFuemE"


scopes = ["https://www.googleapis.com/auth/youtube",
          "https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtubepartner"]


def remove_html_tags(text):
    """Remove html tags from a string"""

    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

class DataLoader:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def load_data(self, params):
        # Make API call using self.api_url and self.api_key
        # Return the loaded data
        response = requests.get(self.api_url, params=params)
        return response.json()
    



yt_search_url = "https://www.googleapis.com/youtube/v3/search"

def main():
    qry_input = str(input("Search for: "))
    # yt_query_params = { "key"       :   API_KEY     ,
    #                     "part"      :   "snippet"   ,
    #                     "q"         :   qry_input   ,
    #                     "type"      :   "video"     ,
    #                     "maxResults":   5           }

    # loader = DataLoader(yt_search_url, API_KEY)
    # data = loader.load_data(yt_query_params)
    # print(json.dumps(data, indent=4))


    yt_query = qry_input + " youtube"

    for i in search(yt_query, num=1, stop=1):
        webbrowser.open(i)

    google_query = qry_input + " songbpm key"
    for i in search(google_query, num=1, stop=1):
        r = requests.get(i)
        text = remove_html_tags(str(r.content))
        key = re.search('with a ([A-G]) key and a (.*) mode', text)
        print(key.group(1), key.group(2))


    


    


if __name__ == "__main__":
    main()