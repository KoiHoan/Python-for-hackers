#!/usr/bin/env python
import requests

TARGET_URL = "mercury.picoctf.net:27278/"

def check_request(url):
    url = f"http://{url}"
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass

def discover_subdomain(target_url):
    with open("smallwordlist.txt", "r") as wordlist:
        for line in wordlist:
            word = line.strip()
            url = f"{word}.{target_url}"
            response = check_request(url)
            if response:
                print(f"[+] Discovered subdomain --> {url}")

def discover_directory(target_url):
    with open("files-and-dirs-wordlist.txt", "r") as wordlist:
        for line in wordlist:
            word = line.strip()
            url = f"{target_url}/{word}"
            response = check_request(url)
            if response:
                print(f"[+] Discovered directory --> {url}")


discover_directory(TARGET_URL)