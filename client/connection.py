from PyQt5.QtCore import QObject, pyqtSignal
import socket
import time
import json
import pickle

HEADERSIZE = 10

class SocketWorker(QObject):

    signal_server_on = pyqtSignal(bool)
    signal_data_recived = pyqtSignal(list)

    def __init__(self):
        QObject.__init__(self)
        # self.socket = socket.socket()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data = 'empty'
        self.stop_check = False
        self.receivedJson = {}
        self.test_started = False

        self.COMPUTER_NAME = 0
        self.SERVER_IP = ''

    def set_settings(self, name, ip):
        self.COMPUTER_NAME = name
        self.SERVER_IP = ip
             

    def check_server(self):
        while True:
            if self.stop_check:
                break
            self.socket = socket.socket()
            result = self.socket.connect_ex((self.SERVER_IP, 1234))
            if result:
                status = 0
            else:
                status = 1
                self.stop_check = True
                self.signal_server_on.emit(status)


    def message_exchange(self):
        msg = 'empty'
        msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + pickle.dumps(self.data)
        self.socket.send(msg)
        self.data = ['connected', self.COMPUTER_NAME]
                
        while True:
            try:
                msg = pickle.dumps(self.data)
                msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg
                self.socket.sendall(msg)
                self.data = 'empty1'
            except:
                pass
            
            try:
                full_msg = b''
                new_msg = True
                reciveing = True
                while reciveing:
                    msg = self.socket.recv(16)
                    if new_msg:
                        msglen = int(msg[:HEADERSIZE])
                        new_msg = False

                    full_msg += msg

                    if len(full_msg)-HEADERSIZE >= msglen:
                        msg = pickle.loads(full_msg[HEADERSIZE:])
                        self.signal_data_recived.emit(msg)
                        new_msg = True
                        reciveing = False
                        full_msg = b""
            except:
                pass
            time.sleep(0.5) 
        
    def send_message(self, data):
        self.data = data

    def setHost(self, host):
        self.host = host