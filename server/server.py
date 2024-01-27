import threading
import time

import requests

from socket import *
from utils import *

from config_utils import *

class Server:
    def __init__(self, ip, port):
        print(f'SERVER IP: {ip}\nSERVER PORT: {port}\n')
        self.ser = socket(AF_INET, SOCK_STREAM)
        self.ser.bind(
            (ip, port)
        )
        self.ser.listen(3)

    def sender(self, user, text):
        user.send(text.encode('utf-8'))

    def start_server(self):
        while True:
            user, addr = self.ser.accept()
            print(f'CLIENT CONNECTED: IP {addr[0]}\tPORT: {addr[1]}')
            self.listen(user)


    def start_ping(self):
        timeout = 15
        while True:
            execute_ping()
            time.sleep(timeout)

    def start(self):
        start_db()
        self.ping_thread = threading.Thread(target=self.start_ping)
        self.listen_thread = threading.Thread(target=self.start_server)
        self.send_noti = threading.Thread(target=send_notification)


        self.ping_thread.start()
        self.listen_thread.start()
        self.send_noti.start()


    def listen(self, user):
        self.sender(user, 'YOU ARE CONNECTED!')
        is_work = True
        while is_work:
            try:
                data = user.recv(1024)
                self.sender(user, '200')
            except Exception as e:
                data = ''
                is_work = False

            if len(data) > 0:
                msg = data.decode('utf-8')
                store_info(msg)



            else:
                print('CLIENT DISCONNECTED')
                is_work = False


Server('192.168.0.104', 7000).start()
#192.168.0.103