#!usr/bin/env python
import requests
from bs4 import BeautifulSoup
import urllib.parse as urlparse
def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass

target_url = "http://192.168.209.130/mutillidae/index.php?page=dns-lookup.php"
response = request(target_url)

parsed_html = BeautifulSoup(response.text, 'html.parser')
forms_list = parsed_html.findAll("form")
for form in forms_list:
    action = form.get("action")
    method = form.get("method")
    post_data = {}
    for field in form.findAll("input"):
        field_name = field.get("name")
        field_type = field.get("type")
        field_value = field.get("value")
        post_url = urlparse.urljoin(target_url, action)
        if field_type == "text":
            field_value = "test"
        post_data[field_name] = field_value
    # print(post_url)
    result = requests.post(post_url, data=post_data)
    print(result.text)
