# -*- coding: cp950 -*-
import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

from bs4 import BeautifulSoup
import requests
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
    url = url.replace('watch', 'live_chat')

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    print r.text
    
    msg = soup.find_all('yt-live-chat-text-message-renderer')
    for tag in msg:
        print tag.string
        
def main():
    url = raw_input("URL = ")
    chat_show(url)
    
if __name__ == "__main__":
    main()
