import requests
from googlesearch import search
import re
import webbrowser
from multiprocessing import Process, Queue


"""

USE JINJA/FLASK INSTEAD OF TKINTER, MORE FUNCTIONAL

"""


def remove_html_tags(text):
    """Remove html tags from a string"""

    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
    



yt_search_url = "https://www.googleapis.com/youtube/v3/search"


def search_and_open_video(qry, queue):
    for i in search(qry, num=1, stop=1):
            # webbrowser.open(i)
            id = i.split("=")[1]
            url = f"https://www.youtube.com/embed/{id}?autoplay=1"
            print(url)
            queue.put([url])


def search_and_display_key(qry, queue):
    for i in search(qry, num=1, stop=1):
            r = requests.get(i)
            text = remove_html_tags(str(r.content))
            key = re.search('with a ([A-G]) key and a (.*) mode', text)

            queue.put([f"{key.group(1)} {key.group(2)}"])

def induce_search(qry):
    yt_query = qry + " youtube"
    q = Queue()
    p1 = Process(target=search_and_open_video, args=(yt_query, q))
    
    google_query = qry + " songbpm key"
    p2 = Process(target=search_and_display_key, args=(google_query, q))
    p1.start()
    p2.start()
    p2.join()
    url = q.get()[0]
    p1.join()
    key = q.get()[0]
    print(f"key {key}, url {url}")


    return key, url