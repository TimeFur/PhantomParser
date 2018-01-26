import requests
import logging
import json
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.alert import Alert
from time import sleep

#logging.basicConfig(level = logging.DEBUG)

# The youtube should be used the latest browser for parsing chat data

class YT_download():

    def __init__ (self, driver, _url):
        self.driver = driver
        self.list_url = _url
        self.youtube_list = []
        self.youtubeto_list = []

        self.once_flag = True
        self.main_window = None
        
    def showlist(self):
        pass
        print (help(gdata))

    def download(self, _url):

        timeout = 0
        convert_url = "https://www.converto.io/en"
        self.driver.get(convert_url)

        #self.main_window = self.driver.current_window_handle
        #self.driver.switch_to_window(self.main_window)
        print ("Access to download website")
        
        #
        while (self.driver.page_source.find("youtube-url")) < 0:
            pass
        text_bar = self.driver.find_element_by_id("youtube-url")
        text_bar.send_keys(_url)
        print ("Send url done~")
        
        #
        while (self.driver.page_source.find("display: inline-block;")) < 0:
            pass
        covert_btn = self.driver.find_element_by_css_selector("a.btn.lg.convert-btn")
        while covert_btn.is_displayed() == False:
            pass
        covert_btn.click()
        print ("Click covert done~")
        #self.driver.switch_to_window(self.main_window)
        print (self.driver.window_handles)
        
        #
        while (self.driver.page_source.find("Click here")) < 0:
            timeout += 1
            if timeout > 1000:
                timeout = 0
                covert_btn.click()
            pass
        download_btn = self.driver.find_element_by_id("download-url")
        while download_btn.is_displayed() == False:
            pass
        download_btn.click()
        print ("Download click done~")
        
    def _download_youtubeto_(self, _url):
        iframe_pop_pattern = "MP3Format"
        default_pattern = "DownloadMP3_text"
        pattern = "IframeChooseDefault"

        #self.driver.implicitly_wait(30)
        self.driver.get(_url)
         
        while (self.driver.page_source.find(pattern)) < 0:
            pass
        print ("iframe get")
        frm_template = self.driver.switch_to.frame(self.driver.find_element_by_id(pattern))
        
        print ("Click download")
        try:
            print self.driver.find_element_by_id(iframe_pop_pattern)
            self.driver.find_element_by_id(iframe_pop_pattern).click()
        except:
            self.driver.switch_to_default_content()
            self.driver.find_element_by_id(default_pattern).click()
        
    def listDownload(self, _url):
        self.youtube_list, self.youtubeto_list = self.parseTubeList(_url)
        
        for l_url in self.youtubeto_list:
            print ("Download " + l_url)
            self._download_youtubeto_(l_url)
            #sleep(1)            

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
        result_to_pattern = "https://www.youtubeto.com"
        
        current_list = []
        result_list = []
        result_to_list = []
        
        self.driver.get(_url)
        while (self.driver.page_source.find(pattern)) < 0:
            pass
        print ("======Get item======")
        
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        current_list = soup.find_all("a", class_ = pattern, href = True) # Find the keyword through pattern
        for l in current_list:
            website = l['href']
            msg = website[:website.find("&list")]
            result_list.append(result_pattern + msg)
            result_to_list.append(result_to_pattern + msg)
        print (result_list)
        print (result_to_list)
        print ("======Done======")
        return result_list, result_to_list
        
def main():
    #---------------------Selenium Driver------------------------------
    #driver = webdriver.PhantomJS()
    #driver = webdriver.Firefox()
    chrome_path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    driver = webdriver.Chrome(chrome_path)


    #---------------------Flow------------------------------
    _url  = "https://www.youtube.com/playlist?list=PLCQf7od9epZmcWjwT3031Alo0KZFFM89f"
    #_url  = "https://www.youtubeto.com/zh/?v=c9qdwZtzvbQ"

    yt_obj = YT_download(driver, _url)
    yt_obj.listDownload(_url)

    #yt_obj._download_youtubeto_(_url)
    #yt_obj.parseTubeList(_url)

    #_url  = "https://www.youtubeto.com/zh/?v=rXLU30MceTc"
    #yt_obj.download(_url)
    
    #driver.close()
    
if __name__ == "__main__":
    main()
