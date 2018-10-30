# -*- coding: cp950 -*-
import os


from bs4 import BeautifulSoup
import requests
from selenium import webdriver

import logging as log

'''
CLIENT_SECRETS_FILE = 'client_secret.json'

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
'''

'''--------------------------
    YOUTUBE　METHOD
--------------------------'''
'''
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def channels_list_by_username(service, **kwargs):
    results = service.channels().list(**kwargs).execute()

    print("This channel\ 's ID is %s. Its title is %s, and it has %s views." %
          (results['items'][0]['id'],
           results['items'][0]['snippet']['title'],
           results['items'][0]['statistics']['viewCount']))
'''

def chat_show(url):
    chat_url = url.replace('watch', 'live_chat')
    print (chat_url)

    #Open the browser
    pattern = "yt-live-chat-text-message-renderer"
    chrome_path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    driver = webdriver.Chrome(chrome_path)
    web_request = driver.get(chat_url)

    #Loop page source
    previous_set = set()
    previous_chat_dict = {}
    try:
        while True:
            current_set = set()
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            msg = soup.find_all(pattern)
            
            #get the latest msg
            current_chat_dict = {}
            for m in msg:
                _id = m.get('id')
                chat_author = m.find_all(id = "author-name")
                chat_time = m.find_all(id = "timestamp")
                chat_msg = m.find_all(id = "message")
                
                current_chat_dict[str(_id)] = [chat_time[0], chat_author[0], chat_msg[0]]
                
                for i in chat_msg:
                    current_set.add(i.string)
                    
            if previous_chat_dict != current_chat_dict:
                update_id = set(current_chat_dict) - set(previous_chat_dict)
                for _id in update_id:
                    chat_time = current_chat_dict[_id][0].get_text()
                    chat_author = current_chat_dict[_id][1].get_text()
                    chat_msg = current_chat_dict[_id][2].get_text()
                    
                    print (chat_time + " " + chat_author + " : " + chat_msg)
                previous_chat_dict = current_chat_dict
                
    except Exception, e:
        print (e)

def Chatroom_flow():
    #url = raw_input("URL = ")
    url = "https://www.youtube.com/watch?v=u5X_hiHtKkM"
    chat_show(url)

def main():
    Chatroom_flow()
    
if __name__ == "__main__":
    main()
