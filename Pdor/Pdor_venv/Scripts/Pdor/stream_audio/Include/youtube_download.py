from __future__ import unicode_literals

import requests
import logging
import json
import sys
from time import sleep
import os

import pafy
import threading
import Queue as queue
import time
#logging.basicConfig(level = logging.DEBUG)

# The youtube should be used the latest browser for parsing chat data
'''------------------------------
        Default Setting
------------------------------'''

def folder_list(path):
    file_list = []
    print "===== Exist Files ====="
    #os.walk lists three element in recursively and each tuple represent
    #('path', 'folder', 'file')
    for dirName, dirNames, fileNames in os.walk(path):
        if dirName.find(".git") == -1:
            for i in fileNames:
                file_list.append((i[:-4])) #Remove the ".mp3"
                print i[:-4]
    print "======================="
    return file_list

class Pafy_obj(threading.Thread):
    def __init__ (self, queue = None):
        threading.Thread.__init__(self)
        
        self.pafy_obj_list = None
        self.pafy_obj = None
        self.queue = queue
        
    def download(self, download_url, download_type = "AUDIO"):
        pafy_obj = pafy.new(download_url)

        print pafy_obj.title
        
        if download_type == "AUDIO":
            stream = pafy_obj.getbestaudio() #Return the stream type

            filename = pafy_obj.title

            filename = stream.download(filepath = './' + filename + '.mp3',
                                       quiet = True,
                                       callback = self.mycb)
        elif download_type == "VIDEO":
            stream = pafy_obj.getbest(preftype = "mp4") #Return the stream type

            filename = pafy_obj.title

            filename = stream.download(filepath = './' + filename + "." + stream.extension,
                                       quiet = True,
                                       callback = self.mycb)
        else:
            print ("In Pady_obj module, the download function [download type] not found!!!")

    def playlistdownload(self, list_url):
        self.pafy_obj = pafy.get_playlist(list_url)
        print "List is almost ", len(self.pafy_obj['items'])
        for i in range (len(self.pafy_obj['items'])):
            print self.pafy_obj['items'][i]['pafy'].title

            filename, checkbit = self._check_filename(self.pafy_obj['items'][i]['pafy'].title)

            if checkbit == 0:                        
                stream = self.pafy_obj['items'][i]['pafy'].getbestaudio()

                stream.download(filepath = './' + filename + '.mp3',
                                quiet = True,
                                callback = self.mycb)


    def pafy_list_obj(self, list_url):
                
        self.pafy_obj_list = pafy.get_playlist(list_url)
        return self.pafy_obj_list

    def run(self):
        if self.queue == None:
            print "The Queue is empty!!!"
            return False
        
        while self.queue.qsize() > 0:
            link = self.queue.get()

            print link.title + "Downloading..."
            filename, checkbit= self._check_filename(link.title)

            if checkbit == 0:
                stream = link.getbestaudio()
                stream.download(filepath = './' + filename + '.mp3',quiet = True)
            
    #Chuck download
    #Total bytes in stream (int)
    #Total bytes in downloaded (int)
    #ratio download (float)
    #download rate (kbps) (float)
    #ETA in seconds (float)
    def mycb(self, total, recvd, ratio, rate, eta):
        print(recvd, ratio, eta)

    def _check_filename(self, f):
        i = 0
        f = f.replace('<', '')
        f = f.replace('>', '')
        f = f.replace(':', '')
        f = f.replace('"', '')
        f = f.replace('/', '')
        f = f.replace('\\', '')
        f = f.replace('|', '')
        f = f.replace('?', '')
        f = f.replace('*', '')

        _filwname = f + '.mp3'
        if _filwname in os.listdir('.'):
            print "File name " + f + " exist~~~"
            i += 1
            
        return f, i
    
def Mutiple_thread_download(list_url, thread_num):

    stream_queue = queue.Queue()
    pafy_obj = Pafy_obj().pafy_list_obj(list_url)
    threads = []
    
    #Get the stream data into Queue
    for i in range(len(pafy_obj['items'])):
        print pafy_obj['items'][i]['pafy'].title
        #stream = pafy_obj['items'][i]['pafy'].getbestaudio()
        _link = pafy_obj['items'][i]['pafy']
        stream_queue.put(_link)

    #Create the thread
    for i in range(thread_num):
        threads.append(Pafy_obj(stream_queue))
        threads[i].start()
        
    for _thread in threads:
        _thread.join()
    
    
def PafyFlow():
    ytdl_type = raw_input("Choose the download type ([1]Single youtbe download. [2]Playlist download) :")

    if ytdl_type == '1':
        print "Download Single youtube"
        _url = raw_input("Type the url : ")

        yt_obj = Pafy_obj()
        yt_obj.download(_url)
    elif ytdl_type == '2':
        print "Download Playlist"
        _url = raw_input("Type the url : ")
        Mutiple_thread_download(_url, 10)
    else:
        print "Do nothing"
        
def yt_download(url, download_type):
    check_pattern_with_security = "https://www.youtube.com/"
    check_pattern = "http://www.youtube.com/"
    if url.find(check_pattern) >= 0 or url.find(check_pattern_with_security) >= 0:
        yt_obj = Pafy_obj()
        try:
            yt_obj.download(url, download_type)
        except:
            print ("download load fail")
    else:
        print ("Url pattern is not found")
        
def main():
    PafyFlow()

def test():
    print "Youtube downloader!!!"
    
