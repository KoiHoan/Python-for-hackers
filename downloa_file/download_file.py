#!/usr/bin/env python
import requests

def download(url):
    get_response=requests.get(url)
    filename=url.split('/')[-1]
    print(filename)
    with open(filename, 'wb') as out_file:
        out_file.write(get_response.content)
download("https://media-cdn-v2.laodong.vn/Storage/NewsPortal/2020/8/21/829850/Bat-Cuoi-Truoc-Nhung-07.jpg")