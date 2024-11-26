#!/usr/bin/env python
import requests
import re
import urllib.parse as urlparse

TARGET_URL = "192.168.209.130/mutillidae/"
target_links = []

def check_request(url):
    url = f"http://{url}"
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass

def extract_links_from(url):
    response = check_request(url)
    return re.findall('href="(.*?)"', response.text) #? is for non-greedy match

def crawl(url):
    href_links = extract_links_from(url)
    for link in href_links:
        link=urlparse.urljoin(url, link) #join the base url with the relative url
        print(link)
        if "#" in link:
            link = link.split("#")[0] #remove the anchor part of the url
        if TARGET_URL in link and link not in target_links: #remove external links and duplicates
            target_links.append(link)
            print(link)
            crawl(link) #crawl found links

crawl(TARGET_URL)
    
        