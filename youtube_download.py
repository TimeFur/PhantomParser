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

def folder_list(path):
    print "Folder"
    

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
        print ("iframe get")
        frm_template = self.driver.switch_to.frame(self.driver.find_element_by_id(pattern))
        
        print ("Click download")
        try:
            print (self.driver.find_element_by_id(iframe_pop_pattern))
            self.driver.find_element_by_id(iframe_pop_pattern).click()
        except:
            self.driver.switch_to_default_content()
            self.driver.find_element_by_id(default_pattern).click()
        
    def listDownload(self, _url):
        self.youtube_list, self.youtubeto_list = self.parseTubeList(_url)
        
        main_tab = self.driver.current_window_handle
        print ("Main tab = " + str(main_tab))
        
        for i, l_url in enumerate(self.youtubeto_list):
            print ("Download " + l_url + "-----" + str(i))
            self._download_youtubeto_(l_url)
            
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
        
        for i, l in zip(name_list, current_list):
            website = l['href']
            msg = website[:website.find("&list")]
            
            result_list.append(result_pattern + msg)
            result_to_list.append(result_to_pattern + msg)
            result_name_list.append(i['title'])
            
        print ("result_list = " + str(len(result_list)))
        print ("======Done======")
        return result_list, result_to_list, result_name_list
        
def main():
    #---------------------Selenium Driver------------------------------
    #driver = webdriver.PhantomJS()
    #driver = webdriver.Firefox()
    chrome_path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    driver = webdriver.Chrome(chrome_path)

    #---------------------Flow------------------------------
    _url  = "https://www.youtube.com/playlist?list=PL-sWiDCbVIJ4OHFXaTEr1agQyeQd_GEA_"

    yt_obj = YT_download(driver, _url)
    a, b, c = yt_obj.parseTubeList(_url)
    print c

    #---------------------Close driver------------------------------
    driver.close()
    
if __name__ == "__main__":
    main()
