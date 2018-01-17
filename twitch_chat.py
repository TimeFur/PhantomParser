import requests
import logging
import json
import sys
from bs4 import BeautifulSoup
from selenium import webdriver

#logging.basicConfig(level = logging.DEBUG)

def youtube_chat(driver, _url):
    
    youtube_pattern = "style-scope yt-live-chat-item-list-renderer"
    previous_chat_list = []
    current_chat_list = []
    
    driver.get(_url)

    #Wait for loading the chat message
    while driver.page_source.find(youtube_pattern) < 0:
        pass
    
    #Listening the msg
    try:
        while True:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            current_chat_list = (soup.find_all("div", class_ = youtube_pattern))
            if current_chat_list != previous_chat_list:
                latest_msg = set(current_chat_list) - set(previous_chat_list)
                for msg in latest_msg:
                    try:
                        print (msg.get_text())
                    except:
                        print ("----pass-----")
                        pass
                previous_chat_list = current_chat_list
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print ("Error Line=" + exc_tb.tb_lineno)
        print ("Log chat done")

def twitch_chat(driver, _url):
    twitch_pattern = "chat-line__message"
    previous_chat_list = []
    current_chat_list = []
    
    driver.get(_url)

    #Wait for loading the chat message
    while driver.page_source.find(twitch_pattern) < 0:
        pass
    
    #Listening the msg
    try:
        while True:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            current_chat_list = (soup.find_all("div", class_="chat-line__message"))
            if current_chat_list != previous_chat_list:
                latest_msg = set(current_chat_list) - set(previous_chat_list)
                for msg in latest_msg:
                    try:
                        print (msg.get_text())
                    except:
                        print ("----pass-----")
                        pass
                previous_chat_list = current_chat_list
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print ("Error Line=" + exc_tb.tb_lineno)
        print ("Log chat done")
    
def main():
    driver = webdriver.PhantomJS()
    _url  = "https://www.twitch.tv/leejuju"
    twitch_chat(driver, _url)
    #_url  = "https://www.youtube.com/watch?v=wUPPkSANpyo"
    #youtube_chat(driver, _url)
    
if __name__ == "__main__":
    main()
