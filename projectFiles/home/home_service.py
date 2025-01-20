import requests
from googlesearch import search
import re
import time
import concurrent.futures
from os import environ as env
import json








class SongNotFoundError(Exception):
    def __init__(self, qry):
        self.qry = qry

    def __str__(self):
         return f"'{self.qry}' not found."


def remove_html_tags(text):
    """Remove html tags from a string"""

    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
    
def get_auth_header(token):
     return {"Authorization": "Bearer " + token}


def search_and_open_video(qry):
    yt_qry = qry + " youtube"
    for i in search(yt_qry, num=1, stop=1):
            id = i.split("=")[1]
            url = f"https://www.youtube.com/embed/{id}?autoplay=1&mute=1"
            return url

def key_search(qry):
    google_qry = qry + " songbpm key"
    for i in search(google_qry, num=1, stop=1):
            r = requests.get(i)
            text = remove_html_tags(str(r.content))
            key = re.search('with a ([A-G]) key and a (.*) mode', text)
            try:
                if key is None:
                     raise SongNotFoundError(qry)
                print("Found KEY")
                return f"{key.group(1)} {key.group(2)}"
            except Exception as e:
                 return ""
    
    
                 

def induce_search(qry, get_key):



    key = None
    if get_key:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(key_search, qry)
            try:
                key = future.result(timeout=11)
            except concurrent.futures.TimeoutError:
                 key = ""
                 
    url = search_and_open_video(qry)
    return key, url