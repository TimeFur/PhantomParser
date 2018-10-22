# -*- coding: cp950 -*-
import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

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
    try:
        while True:
            current_set = set()
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            msg = soup.find_all(pattern)
            #get the latest msg
            for m in msg:
                result = m.find_all(id = "message")
                for i in result:
                    current_set.add(i.string)
                    
            if current_set != previous_set:
                for msg in (current_set - previous_set):
                    print msg
            previous_set = current_set
                
    except Exception,e:
        print (e)

def Chatroom_flow():
    url = raw_input("URL = ")
    chat_show(url)

def main():
    Chatroom_flow()
    
if __name__ == "__main__":
    main()
