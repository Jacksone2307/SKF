import requests
from googlesearch import search
import re
import webbrowser
import multiprocessing
from tkinter import *


"""

USE JINJA/FLASK INSTEAD OF TKINTER, MORE FUNCTIONAL

"""


def remove_html_tags(text):
    """Remove html tags from a string"""

    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
    



yt_search_url = "https://www.googleapis.com/youtube/v3/search"


def search_and_open_video(qry):
    for i in search(qry, num=1, stop=1):
            webbrowser.open(i)

def search_and_display_key(qry):
    for i in search(qry, num=1, stop=1):
            r = requests.get(i)
            text = remove_html_tags(str(r.content))
            key = re.search('with a ([A-G]) key and a (.*) mode', text)
            return (key.group(1), key.group(2))

def induce_search(qry):
    yt_query = qry + " youtube"
    p1 = multiprocessing.Process(target=search_and_open_video, args=(yt_query, ))
    
    google_query = qry + " songbpm key"
    p2 = multiprocessing.Process(target=search_and_display_key, args=(google_query, ))
    p1.start()
    p2.start()
    key = p2.join()
    p1.join()
    return key

def main():

    r = Tk()
    r.title("SKF")

    qryLabel = Label(r, text="Song Name")
    qryLabel.grid(row=0, column=0)

    qryEntry = Entry(r)
    qryEntry.grid(row=0,column=1)

    searchButton = Button(r, text="Search", command = lambda: induce_search(qryEntry.get()))
    searchButton.grid(row=1, column=0, columnspan=2)

    r.mainloop()

if __name__ == "__main__":
    main()