import requests
from googlesearch import search
import re
import time
from multiprocessing import Process, Queue
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
            # webbrowser.open(i)
            id = i.split("=")[1]
            url = f"https://www.youtube.com/embed/{id}?autoplay=1&mute=1"
            return url

# def search_spotify(token, qry):
#     url = "https://api.spotify.com/v1/search"
#     headers = get_auth_header(token)
#     spotify_qry = f"?q={qry}&type=track&limit=1"      #Search for track, grab first one
#     qry_rul = url + spotify_qry
#     r = requests.get(qry_rul, headers=headers)
#     json_result = json.loads(r.content)["tracks"]["items"]
#     #Grab the id of the track
#     try:
#         if len(json_result) == 0:
#              raise SongNotFoundError(qry)
#         return json_result[0]
        
#     except Exception as e:
#         return None

def key_search(qry, queue):
    # Spotify API deprecated feature
    # url = f"https://api.spotify.com/v1/tracks/{id}"
    # headers = get_auth_header(token)
    # r = requests.get(url, headers=headers)
    # print(r)
         

    google_qry = qry + " songbpm key"
    for i in search(google_qry, num=1, stop=1):
            r = requests.get(i)
            text = remove_html_tags(str(r.content))
            key = re.search('with a ([A-G]) key and a (.*) mode', text)
            try:
                if key is None:
                     raise SongNotFoundError(qry)
                print("Found KEY")
                queue.put(f"{key.group(1)} {key.group(2)}")
            except Exception as e:
                 return "NotFound"
    
    
                 

def induce_search(qry):
    start = time.time()

    q = Queue()
    p = Process(target=key_search, args=(qry,q))
    p.start()
    p.join(timeout=10)
    if p.is_alive():
        p.terminate()

    key = "NotFound"
    if not q.empty() or q.qsize() > 0:
        key = q.get()
        
    q.close()

    url = search_and_open_video(qry)
    print(f"Time taken: {time.time() - start} sec")

    
    return key, url