import requests
import logging
import json
from selenium import webdriver

driver = webdriver.PhantomJS()
logging.basicConfig(level = logging.DEBUG)

def main():
    _url  = "https://www.twitch.tv/mobilmobil"

    session = requests.Session()
    driver.get(_url)
    
    while driver.page_source.find("chat-line__message") < 0:
        pass    
    print (driver.page_source)
    
if __name__ == "__main__":
    main()
