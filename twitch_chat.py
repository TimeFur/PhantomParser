import requests
import logging
import json
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.PhantomJS()
logging.basicConfig(level = logging.DEBUG)


def twitch_chat(driver, _url):
    twitch_pattern = "chat-line__message"

    driver.get(_url)
    
    while driver.page_source.find("chat-line__message") < 0:
        pass

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #print (soup.prettify())
    l = (soup.find_all("div", class_="chat-line__message"))
    for i in l:
        print ("---------------")
        print (i)

def main():
    _url  = "https://www.twitch.tv/kandytung"
    twitch_chat(driver, _url)
    
if __name__ == "__main__":
    main()
