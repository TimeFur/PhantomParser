import requests
import logging
import json
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

#logging.basicConfig(level = logging.DEBUG)

# The youtube should be used the latest browser for parsing chat data

class YT_download():

    def __init__ (self, driver, _url):
        self.driver = driver
        self.list_url = _url

    def showlist(self):
        pass
        print (help(gdata))

    def download(self, url):
        pass
    
    def listDownload(self, url):
        pass

    def test(self, _url):
        twitch_pattern = "https://r2"
        previous_chat_list = []
        current_chat_list = []
        
        self.driver.get(_url)
        #Wait for loading the chat message
        while self.driver.page_source.find(twitch_pattern) < 0:
            pass
        #print (self.driver.page_source)
        #Listening the msg
        
        try:
            #while True:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            current_chat_list = (soup.find_all("a", class_="link link-download subname ga_track_events download-icon"))
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
        
def main():
    #driver = webdriver.PhantomJS()
    driver = webdriver.Firefox()
    
    _url  = "https://www.ssyoutube.com/watch?v=Qly4kNtckkg"

    yt_obj = YT_download(driver, _url)
    yt_obj.test(_url)
    
    driver.close()
if __name__ == "__main__":
    main()
