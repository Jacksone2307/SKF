import requests
from googlesearch import search
import re
from multiprocessing import Process, Queue


"""

USE JINJA/FLASK INSTEAD OF TKINTER, MORE FUNCTIONAL

"""

class SongNotFoundError(Exception):
    def __init__(self, qry):
        self.qry = qry

    def __str__(self):
         return f"'{self.qry}' not found."


def remove_html_tags(text):
    """Remove html tags from a string"""

    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
    



yt_search_url = "https://www.googleapis.com/youtube/v3/search"


def search_and_open_video(qry, queue):
    yt_qry = qry + " youtube"
    for i in search(yt_qry, num=1, stop=1):
            # webbrowser.open(i)
            id = i.split("=")[1]
            url = f"https://www.youtube.com/embed/{id}?autoplay=1&mute=1"
            print(url)
            queue.put([url])


def search_and_display_key(qry, queue):
    google_qry = qry + " songbpm key"
    for i in search(google_qry, num=1, stop=1):
            r = requests.get(i)
            text = remove_html_tags(str(r.content))
            key = re.search('with a ([A-G]) key and a (.*) mode', text)
            try:
                if key is None:
                     raise SongNotFoundError
                queue.put([f"{key.group(1)} {key.group(2)}"])
            except Exception as e:
                 queue.put(["NotFound"])
                 

def induce_search(qry):
    q = Queue()
    p1 = Process(target=search_and_open_video, args=(qry, q))
    
    p2 = Process(target=search_and_display_key, args=(qry, q))
    p1.start()
    p2.start()
    p2.join()
    url = q.get()[0]
    p1.join()
    key = q.get()[0]
    print(f"key {key}, url {url}")


    return key, url