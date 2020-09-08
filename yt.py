import tkinter as tk
import os
import requests
import sys
from enum import Enum
from enum import IntEnum
from PIL import Image, ImageTk as itk

API_KEY = "API_KEY" #replace with your api key
CHANNEL_ID = "CHANNEL_ID" #replace with your channel id

BASE_URL = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id="
QUERY_ITEMS = "&key="

FONT_SIZE = 120
FONT = "ARCADE"
PADY = 10
PADX = 20
PADY_IMG = 10
PADX_IMG = 10
IMG = "yt.png" #should be in the same dir as yt.py

DISPLAY = ":0"

REFRESH_INTERVAL = 1000 * 10

class Statistic(Enum): 
    subscriberCount = "subscriberCount"
    viewCount = "viewCount"

class StatDisplayType(IntEnum): 
    subs = 0
    views = 1

class Stat():
    def __init__(self):
        self.stats = None
        self.types = list(map(int, StatDisplayType))

        self.complete_url = BASE_URL + CHANNEL_ID + QUERY_ITEMS + API_KEY
        self.refreshStats()
    
    def refreshStats(self):
        result = requests.get(self.complete_url)

        if isinstance(result.json(), dict):
            items = result.json()["items"]

            if isinstance(items, list) and len(items) > 0 :
                item = items[0]
                
                if isinstance(item, dict) and item["statistics"] != None :
                    newStats = item["statistics"]

                    self.stats = newStats

    def get(self, stat: Statistic):
        if self.stats == None: 
            return None
            
        if isinstance(self.stats, dict) and self.stats["subscriberCount"] != None :
            return self.stats[stat.value]

        return None


class App():
    def __init__(self):
        self.stats = Stat()
        self.statIndex = 0

        self.root = tk.Tk(DISPLAY)
        self.root.attributes('-fullscreen', True)

        self.main_frame = tk.Frame(self.root)
        self.main_frame.config(background='black', cursor='none')
        self.main_frame.pack(fill=tk.BOTH, expand=tk.TRUE)
        self.root.bind('<F3>', self.quit)
        
        self.setImage()
        self.setLabel()
        self.pack()

        self.poll()
        self.displayPoll()

        self.root.mainloop()

    def setLabel(self):
        
        self.typeText = tk.StringVar()
        self.typelabel = tk.Label(self.main_frame, 
                                    textvariable=self.typeText,
                                    font=("ARCADE", 25),
                                    foreground='white', 
                                    background='black')

        self.typeText.set("subs")

        self.text = tk.StringVar()
        self.ytSublabel = tk.Label(self.main_frame, 
                                   textvariable=self.text,
                                   font=("ARCADE", FONT_SIZE),
                                   foreground='white', 
                                   background='black')

        self.text.set("0")


    def setImage(self):
        photo = tk.PhotoImage(file = IMG)
        photo = photo.subsample(4)
        self.ytImage = tk.Label(self.main_frame, image=photo, width=200, height=100, background='black')
        self.ytImage.image = photo
    
    def pack(self):
        self.ytImage.pack(padx=(PADX, 0), pady=(PADY_IMG, 0))
        self.typelabel.pack(padx=(PADX, 0))
        self.ytSublabel.pack(padx=(PADX + 10, 0), pady=(PADY, 0))


    def quit(self, event):
        self.root.destroy()

    def formatNumber(self, subscribers: int) -> str:
        sub = int(subscribers)

        if sub > 1000000:
            sub = str(round(sub / 1000000, 1)) + "m"
            self.ytSublabel.font = ("ARCADE", FONT_SIZE - 40)
        
        elif sub > 1000:
            sub = str(round(sub / 1000, 1)) + "k"
            self.ytSublabel.font = ("ARCADE", FONT_SIZE - 40)

        return sub

    def display(self, type: StatDisplayType):
        dispText = None

        if type == StatDisplayType.subs:
            dispText = self.stats.get(Statistic.subscriberCount)
            self.typeText.set("subs")

        elif type == StatDisplayType.views:
            dispText = self.stats.get(Statistic.viewCount)
            self.typeText.set("views")

        if dispText != None: 
            formatted = self.formatNumber(int(dispText))
            self.text.set(str(formatted))
        else:
            self.text.set("")

    def getStatDisplayType(self):
        index = self.statIndex

        dispType = StatDisplayType(self.stats.types[index])

        self.statIndex += 1
        
        if self.statIndex > len(self.stats.types) - 1:
            self.statIndex = 0

        return dispType
        

    def displayPoll(self):
        self.display(self.getStatDisplayType())
        self.root.after(REFRESH_INTERVAL, self.displayPoll)

    def poll(self):
        self.stats.refreshStats()
        self.root.after(1000 * 60 * 15, self.poll)


App()
