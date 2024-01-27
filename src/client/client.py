from socket import *
import json
import time
from utils import get_info


class Client:
    def __init__(self, ip, port):
        self.cli = socket(AF_INET, SOCK_STREAM)
        self.cli.connect(
            (ip, port)
        )

    def connect(self):
        print("TRYING TO CONNECT.....")
        try:
            msg = self.cli.recv(1024).decode('utf-8')
            if msg == 'YOU ARE CONNECTED!':
                print(msg)
                self.listen()
        except Exception as e:
            print(f'ERROR: {str(e)}')
            exit()

    def sender(self, text):
        self.cli.send(text.encode('utf-8'))
        while self.cli.recv(1024).decode('utf-8') != '200':
            self.cli.send(text.encode('utf-8'))


    def listen(self):
        is_work = True
        timeout = 15

        while is_work:
            info = json.dumps(get_info())
            if info:
                self.sender(info)
            time.sleep(timeout)


Client('192.168.0.104', 7000).connect()