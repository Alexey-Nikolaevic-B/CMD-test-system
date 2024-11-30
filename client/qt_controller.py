from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal

import threading
import connection
import json

import ui_lobby
import ui_login 
import ui_result
import ui_test

class QT_Controler(QObject):

    server_on            = pyqtSignal(int)
    signal_goto_lobby    = pyqtSignal(str)
    signal_data_recived  = pyqtSignal(list)
    signal_update_status = pyqtSignal(list)
    signal_goto_result   = pyqtSignal(list)
    signal_set_host      = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self)

        self.widget   = QtWidgets.QStackedWidget()
        self.login    = ui_login.LoginScreen()
        self.lobby    = ui_lobby.LobbyScreen()
        self.test     = ui_test.TestScreen()
        self.result   = ui_result.ResultScreen()

        self.worker  = connection.SocketWorker()

        self.COMPUTER_NAME = 0
        self.SERVER_IP = ''
        self.current_dir = 'C:'

        self.load_settings()
        self.signals()
        self.run()
        
    def load_settings(self):
        with open('_config.json') as config_file:
            data = json.load(config_file)

        self.COMPUTER_NAME = data['COMPUTER_NAME']
        self.SERVER_IP = data['SERVER_IP']

        self.worker.set_settings(self.COMPUTER_NAME, self.SERVER_IP)

    def run(self):
        self.connection = threading.Thread(target=self.worker.check_server, daemon=True)
        self.connection.start()

        self.widget.addWidget(self.login)
        self.widget.show()

    def signals(self):
        self.worker.signal_server_on.connect(self.set_server_status)
        self.worker.signal_data_recived.connect(self.process_recived_data)

        self.login.signal_goto_lobby.connect(self.gotoLobbyScreen)     

        self.test.signal_update_status.connect(self.update_status)
        self.test.signal_goto_result.connect(self.gotoResultScreen)

    def update_status(self, data):
        self.student_name = data
        self.signal_update_status.emit(self.student_name)
        self.worker.send_message(['status', self.COMPUTER_NAME] + data)

    def process_recived_data(self, data):
        self.student_name = data
        self.signal_data_recived.emit(self.student_name)

        if data[0] == 'start':
            self.gotoTestScreen()
            self.test.set_settings(data[1], data[2], data[3], data[4])

        if data[0] == 'finish':
            self.test.gotoResultScreen()

    def setHost(self, host):
        self.host = host
        self.signal_set_host.emit(self.host)  
        self.worker.setHost(host)

    def set_server_status(self, status):
        self.server_status = status
        self.server_on.emit(self.server_status)
        if self.server_status:
            self.connections = threading.Thread(target=self.worker.message_exchange, daemon=True)
            self.connections.start()
            self.login.server_is_on()

    def gotoLobbyScreen(self, name):
        self.student_name = name
        self.signal_goto_lobby.emit(self.student_name)

        self.worker.send_message(['name', self.COMPUTER_NAME, str(self.student_name)])

        self.widget.addWidget(self.lobby)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)    

    def gotoTestScreen(self):
        self.widget.addWidget(self.test)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)
        self.worker.send_message(['status', self.COMPUTER_NAME, 1, 0])

    def gotoResultScreen(self, mark):
        self.mark = mark
        self.signal_goto_result.emit(self.mark)

        self.result.set_mark(mark[0], mark[1], mark[2])

        self.worker.send_message(['finished', self.COMPUTER_NAME, mark[0]])

        self.widget.addWidget(self.result)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)