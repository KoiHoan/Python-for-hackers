#!usr/bin/env python

import requests

TARGER_URL = "http://192.168.209.130/dvwa/login.php"
data = {"username": "admin", "password": "ds", "Login": "Login"}
reponse = requests.post(TARGER_URL, data=data)
print(reponse.text)