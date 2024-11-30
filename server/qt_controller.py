from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal

import socket as socket
import threading
import connection
import json

import ui_main

class QT_Controler(QObject):

    signal_data_recived = pyqtSignal(list)
    signal_toggle_test  = pyqtSignal(list)

    def __init__(self):
        QObject.__init__(self)
        self.main   = ui_main.MainScreen()
        self.worker = connection.SocketWorker()
        self.widget = QtWidgets.QStackedWidget()
        
        self.test_is_started = False
        self.users = [None]*12

        self.load_settings()
        self.signals()
        self.run()
        
    def load_settings(self):
        with open('_config.json') as config_file:
            data = json.load(config_file)

        self.SERVER_IP = data['SERVER_IP']

        self.worker.set_settings(self.SERVER_IP)

    def run(self):
        self.checker = threading.Thread(target=self.worker.process, daemon=True)
        self.checker.start()
        
        self.widget.addWidget(self.main)
        self.widget.show()
        # self.widget.showFullScreen()

    def signals(self):
        self.worker.signal_data_recived.connect(self.process_recived_data)

        self.main.signal_toggle_test.connect(self.toggle_test)

    def toggle_test(self, data):
        self.student_name = data
        self.signal_toggle_test.emit(self.student_name)

        if not self.test_is_started:
            self.worker.send_message(data)
            self.test_is_started = True
        else:
            self.worker.send_message(data)

    def process_recived_data(self, data):
        self.student_name = data
        self.signal_data_recived.emit(self.student_name)

        if data[0] == 'connected':
            self.main.update_users(data[1], '—', '—', '—')

        if data[0] == 'name':
            self.main.update_users(data[1], data[2], '—', '—')
            self.users[data[1]-1] = data[2]

        if data[0] == 'status':
            self.main.update_users(data[1], self.users[data[1]-1], data[2], data[3])

        if data[0] == 'finished':
            self.main.set_mark(data[1], data[2])



        