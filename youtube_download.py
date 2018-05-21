from __future__ import unicode_literals

import requests
import logging
import json
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.alert import Alert
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
EXIST_DIR_PATH = "C:\\Users\\djs86\\Downloads\\"
DOWNLOAD_URL = "https://www.youtube.com/playlist?list=PL-sWiDCbVIJ4OHFXaTEr1agQyeQd_GEA_"

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
        
    def download(self, download_url):
        pafy_obj = pafy.new(download_url)
        stream = pafy_obj.getbestaudio() #Return the stream type

        print pafy_obj.title
        
        filename = stream.download(quiet = True, callback = self.mycb)

    def playlistdownload(self, list_url):
        self.pafy_obj = pafy.get_playlist(list_url)
        print "List is almost ", len(self.pafy_obj['items'])
        for i in range (len(self.pafy_obj['items'])):
            print self.pafy_obj['items'][i]['pafy'].title

            filename = self._check_filename(self.pafy_obj['items'][i]['pafy'].title)
                        
            stream = self.pafy_obj['items'][i]['pafy'].getbestaudio()
            
            stream.download(filepath = './' + filename + '.mp3',quiet = True, callback = self.mycb)


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
            filename = self._check_filename(link.title)
            stream = link.getbestaudio()
            stream.download(filepath = './' + filename + '.mp3',quiet = True)
            print link.title + "Done"
    #Chuck download
    #Total bytes in stream (int)
    #Total bytes in downloaded (int)
    #ratio download (float)
    #download rate (kbps) (float)
    #ETA in seconds (float)
    def mycb(self, total, recvd, ratio, rate, eta):
        print(recvd, ratio, eta)

    def _check_filename(self, f):
        f = f.replace('<', '')
        f = f.replace('>', '')
        f = f.replace(':', '')
        f = f.replace('"', '')
        f = f.replace('/', '')
        f = f.replace('\\', '')
        f = f.replace('|', '')
        f = f.replace('?', '')
        f = f.replace('*', '')
        return f
            
class YT_download():

    def __init__ (self, driver, _url):
        self.driver = driver
        self.list_url = _url
        self.youtube_list = []
        self.youtubeto_list = []

        self.once_flag = True
        self.main_window = None

    def _download_youtubeto_(self, _url):
        iframe_pop_pattern = "MP3Format"
        default_pattern = "DownloadMP3_text"
        pattern = "IframeChooseDefault"

        #self.driver.implicitly_wait(30)
        self.driver.get(_url)
         
        while (self.driver.page_source.find(pattern)) < 0:
            pass
        #print ("iframe get")
        frm_template = self.driver.switch_to.frame(self.driver.find_element_by_id(pattern))
        
        #print ("Click download")
        try:
            print (self.driver.find_element_by_id(iframe_pop_pattern))
            self.driver.find_element_by_id(iframe_pop_pattern).click()
        except:
            self.driver.switch_to_default_content()
            self.driver.find_element_by_id(default_pattern).click()
        
    def listDownload(self, _url, exist_file):
        self.youtube_list = self.parseTubeList(_url)
        
        main_tab = self.driver.current_window_handle
        print ("Main tab = " + str(main_tab))
        
        for i, l_url in enumerate(self.youtube_list):
            #print ("Download " + l_url['Title'] + "-----" + str(i))
            title = (l_url['Title'])
            print title
            if title not in exist_file:
                self._download_youtubeto_(l_url['Download'])
            else:
                print title + " is exist"
                
            #Close other windows
            for i, handle in enumerate(self.driver.window_handles):
                if handle != main_tab:
                    self.driver.switch_to_window(handle)
                    self.driver.close()
            self.driver.switch_to_window(main_tab) #Back to main tab

    def test(self, _url):
        pattern = "yt-live-chat-text-message-renderer"
        previous_chat_list = []
        current_chat_list = []
        
        self.driver.get(_url)

        #Wait for loading the chat message
        while (self.driver.page_source.find(pattern)) < 0:
            pass
        #self.driver.find_element_by_id("CloseButton").click()
        #self.driver.find_element_by_class_name(pattern).click()
        #print (self.driver.page_source)

        #Listening the msg
        
        try:
            while True:
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                current_chat_list = (soup.find_all("span", class_="style-scope yt-live-chat-text-message-renderer"))
                if current_chat_list != previous_chat_list:
                    latest_msg = set(current_chat_list) - set(previous_chat_list)
                    for msg in latest_msg:
                        try:
                            print (msg)
                        except:
                            print ("----pass-----")
                            pass
                    previous_chat_list = current_chat_list
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print ("Error Line=" + exc_tb.tb_lineno)
            print ("Log chat done")

    def parseTubeList(self, _url):
        pattern = "yt-simple-endpoint style-scope ytd-playlist-video-renderer"
        title_pattern = "style-scope ytd-playlist-video-renderer"
        
        result_pattern = "https://www.youtube.com"
        result_to_pattern = "https://www.youtubeto.com"
        
        current_list = []
        name_list = []
        list_tmp = []
        result_list = []
        result_to_list = []
        result_name_list = []
        result_dict = []
        
        self.driver.get(_url)
        while (self.driver.page_source.find(pattern)) < 0:
            pass
        print ("======Get item======")
        
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        
        list_tmp = soup.find_all("a", class_ = pattern, href = True) # Find the keyword through pattern
        name_list_tmp = soup.find_all("span", class_ = title_pattern, title = True) # Find the keyword through pattern
        
        while current_list != list_tmp:
            current_list = soup.find_all("a", class_ = pattern, href = True) # Find the keyword through pattern
            name_list = soup.find_all("span", class_ = title_pattern, title = True) # Find the keyword through pattern

            self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);") #scroll down
            sleep(5)
            
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            list_tmp = soup.find_all("a", class_ = pattern, href = True) # Find the keyword through pattern
            name_list_tmp = soup.find_all("span", class_ = title_pattern, title = True) # Find the keyword through pattern


        if len(name_list) == len(current_list):
            print "Same amount of title and link"
        else:
            print "Error amount of title and link!!!"
            
        for i, l in zip(name_list, current_list):
            website = l['href']
            msg = website[:website.find("&list")]
            
            result_list.append(result_pattern + msg)
            result_to_list.append(result_to_pattern + msg)
            result_name_list.append(i['title'])

            result_dict.append({"Link": (result_pattern + msg),
                                "Download": (result_to_pattern + msg),
                                "Title": (i['title'])})
            
        print ("result_list = " + str(len(result_list)))
        print ("======Done======")

        return result_list, result_to_list

def AutoSeleFlow():
    #---------------------Selenium Driver------------------------------
    #driver = webdriver.PhantomJS()
    #driver = webdriver.Firefox()
    chrome_path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    driver = webdriver.Chrome(chrome_path)

    #---------------------Flow------------------------------
    _url  = DOWNLOAD_URL
    yt_obj = YT_download(driver, _url)
    
    exist_file = folder_list(EXIST_DIR_PATH)
    yt_obj.listDownload(_url, exist_file)

    #---------------------Close driver------------------------------
    driver.close()

def Mutiple_thread_download(list_url):

    #Get the stream data into Queue
    stream_queue = queue.Queue()
    pafy_obj = Pafy_obj().pafy_list_obj(list_url)
    for i in range(len(pafy_obj['items'])):
        print pafy_obj['items'][i]['pafy'].title
        #stream = pafy_obj['items'][i]['pafy'].getbestaudio()
        _link = pafy_obj['items'][i]['pafy']
        stream_queue.put(_link)

    #Create the thread
    p1 = Pafy_obj(stream_queue)
    p1.start()
    
    p2 = Pafy_obj(stream_queue)
    p2.start()
    
    p3 = Pafy_obj(stream_queue)
    p3.start()
    

    #
    p1.join()
    p2.join()
    p3.join()
    
    
def PafyFlow():
    _url  = "https://www.youtube.com/watch?v=VgjCj5Fj1Ts"
    _url  = "https://www.youtube.com/playlist?list=PLCQf7od9epZmcWjwT3031Alo0KZFFM89f"
    
    yt_obj = Pafy_obj(_url)
    
    #yt_obj.download(_url)
    Mutiple_thread_download(_url)
    
def main():
    #AutoSeleFlow()
    PafyFlow()
    
if __name__ == "__main__":
    main()
