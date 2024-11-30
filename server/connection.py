from PyQt5.QtCore import QObject, pyqtSignal
import socket
from _thread import *
import time
import pickle


host = '172.18.4.48'
port = 2620
dataPackageSize = 1024
HEADERSIZE = 10

class SocketWorker(QObject):

    signal_data_recived = pyqtSignal(list)

    def __init__(self):
        QObject.__init__(self)

        self.data = ['empty'] * 12

        self.ThreadCount = 0
        self.sendJSON = {}
        self.clients = []
        self.ip = ''

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def set_settings(self, ip):
        self.ip = ip

    def process(self):
        try:
            self.socket.bind((self.ip, 1234))
            self.socket.listen(20)

            
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            print(ip_address)
        except socket.error as e:
            print(str(e))

        while True:
            client, address = self.socket.accept()
            self.clients.append((client,))
            start_new_thread(self.threaded_client, (client,))

            self.ThreadCount += 1

    def threaded_client(self, connection):

        thread_number = self.ThreadCount
        while True:
            try:            
                msg = pickle.dumps(self.data[thread_number])
                msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg
                connection.send(msg)
                self.data[thread_number] = 'empty'
            except:
                pass
            
            try:
                full_msg = b''
                new_msg = True
                reciveing = True
                while reciveing:
                    msg = connection.recv(2048)
                    if new_msg:
                        msglen = int(msg[:HEADERSIZE])
                        new_msg = False

                    full_msg += msg

                    if len(full_msg)-HEADERSIZE >= msglen:
                        self.signal_data_recived.emit(pickle.loads(full_msg[HEADERSIZE:]))
                        new_msg = True
                        reciveing = False
                        full_msg = b""
            except:
                pass
            time.sleep(0.5) 

    def send_message(self, dat):
        for x in range(12):
            self.data[x] = dat
            

