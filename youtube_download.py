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
        self.youtube_list = []
        
    def showlist(self):
        pass
        print (help(gdata))

    def download(self, url):
        pass
    
    def listDownload(self, url):
        pass

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
        result_pattern = "https://www.youtube.com"
        current_list = []
        
        self.driver.get(_url)
        while (self.driver.page_source.find(pattern)) < 0:
            pass
        print ("======Get item======")
        
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        current_list = soup.find_all("a", class_ = pattern, href = True) # Find the keyword through pattern
        for l in current_list:
            self.youtube_list.append(result_pattern + l['href'])
        print (self.youtube_list)
        print ("======Done======")
        
def main():
    #driver = webdriver.PhantomJS()
    #driver = webdriver.Firefox()
    chrome_path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    driver = webdriver.Chrome(chrome_path)
    
    _url  = "https://www.youtube.com/playlist?list=PLCQf7od9epZmcWjwT3031Alo0KZFFM89f"

    yt_obj = YT_download(driver, _url)
    yt_obj.parseTubeList(_url)
    
    driver.close()
    
if __name__ == "__main__":
    main()
