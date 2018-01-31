import requests
import logging
import json
import sys
import io

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.alert import Alert
from time import sleep

#logging.basicConfig(level = logging.DEBUG)

# The youtube should be used the latest browser for parsing chat data

class LineTV_download():

    def __init__ (self, driver, _url):
        self.driver = driver
        self.list_url = _url
        self.youtube_list = []
        self.youtubeto_list = []

        self.once_flag = True
        self.main_window = None

    def _download_(self, _url):

        #non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        #s = (res.text.translate(non_bmp_map))
        #s = (res.text.encode())
        
        res = requests.get(_url)
        
        with io.open("1.mp4", 'wb') as f:
            f.write(res.content)
        
        
    def show_link(self, _url):
        pattern = "subt-font-2 subt-bg-transparent subt-color-white _hide_controls"
        download_link_list = []
        
        self.driver.get(_url)
        while (self.driver.page_source.find(pattern)) < 0:
            pass
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        _list = soup.find_all("video", class_ = "subt-font-2 subt-bg-transparent subt-color-white _hide_controls")
        
        main_link = ""
        for i in _list:
            main_link = i['data-src']

        for i in range(100):
            num = '-' + str(i).zfill(6) + '.ts'
            link = main_link.replace('.m3u8', num)
            download_link_list.append(link)
            print (link)
        return download_link_list
    
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
        list_tmp = []
        result_list = []
        result_to_list = []
        
        self.driver.get(_url)
        while (self.driver.page_source.find(pattern)) < 0:
            pass
        print ("======Get item======")
        
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        
        list_tmp = soup.find_all("a", class_ = pattern, href = True) # Find the keyword through pattern
        while current_list != list_tmp:
            current_list = soup.find_all("a", class_ = pattern, href = True) # Find the keyword through pattern

            self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            
            sleep(5)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            list_tmp = soup.find_all("a", class_ = pattern, href = True) # Find the keyword through pattern
        
        for l in current_list:
            website = l['href']
            msg = website[:website.find("&list")]
            result_list.append(result_pattern + msg)
            result_to_list.append(result_to_pattern + msg)
        print ("result_list = " + str(len(result_list)))
        print ("======Done======")
        return result_list, result_to_list
        
def main():
    #---------------------Selenium Driver------------------------------
    #driver = webdriver.PhantomJS()
    #driver = webdriver.Firefox()
    chrome_path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    driver = webdriver.Chrome(chrome_path)

    #---------------------Flow------------------------------
    _url  = "https://tv.line.me/v/2612428_lunam-%E6%88%91%E7%9A%84%E7%94%B7%E5%AD%A9-ep6-1"

    linetv_obj = LineTV_download(driver, _url)
    #linetv_obj.show_link(_url)

    _url  = "https://tv-line.pstatic.net/global/read/navertv_2018_01_26_16/hls/2e5840de-0243-11e8-999e-0000000049b9-000098.ts?__gda__=1517415988_9ab590e41a85e70d623b80c920f62bc6"
    #_url  = "http://python.ez2learn.com/basic/unicode.html"
    linetv_obj._download_(_url)
    

    #---------------------Close driver------------------------------
    driver.close()
    
if __name__ == "__main__":
    main()
