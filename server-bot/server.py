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
        self.send_noti = threading.Thread(target=self.send_notification)


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

    def send_notification(self):
        while True:
            config = read_json(config_path)["TELEGRAM_BOT"]
            if config["NOTIFICATIONS"]:
                BOT_TOKEN = config["BOT_TOKEN"]
                CHAT_ID = config["CHAT_ID"]
                previous_activity = select_all_activity()
                time.sleep(35)
                current_activity = select_all_activity()
                for prev, curr in zip(previous_activity, current_activity):
                    if prev[4] and prev[2] and not curr[2]:
                        message = f'???\tName:{prev[0]}\t\tIP:{prev[1]}\t\tis offline'
                        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
                        requests.get(url).json()
            else:
                time.sleep(10)
                continue


Server('192.168.0.104', 7000).start()
#192.168.0.103