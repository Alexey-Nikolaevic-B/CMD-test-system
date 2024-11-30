from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import*
from PyQt5 import QtCore

class LoginScreen(QDialog):

    signal_goto_lobby = pyqtSignal(str)

    def __init__(self):
        super(LoginScreen, self).__init__()
        self.init_ui()
        self.is_connected = False
        self.user_name = ''

        self.btn_start_test.clicked.connect(self.gotoLobbyScreen)

    def server_is_on(self):
        self.is_connected = True
        style = "QPushButton {color: rgb(0, 0, 0); border-radius: 5px; background-color : rgb(255, 230, 85); font: 20pt \"Consolas\"; } QPushButton::hover {color: rgb(0, 0, 0); background-color : rgb(255, 255, 127); font: 20pt \"Consolas\"; }"
        self.btn_start_test.setStyleSheet(style)
        self.btn_start_test.setText('Подключиться')

    def gotoLobbyScreen(self):
        self.user_data = self.lbl_student_name.text()
        if (self.user_data == ''):
            self.lbl_error.setText('введите данные')
        elif (self.user_data != '' and not self.is_connected):
            self.lbl_error.setText('')
        elif self.is_connected:
            self.signal_goto_lobby.emit(self.user_data)

    def init_ui(self):
        image = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap("img\login_1.jpg")
        image.setPixmap(pixmap)

        image.setScaledContents(True)
        image.show()

        loadUi('qt\Login.ui', self)
        style = "QPushButton {color: rgb(0, 0, 0); border-radius: 5px; background-color : rgb(255, 121, 123); font: 20pt \"Consolas\"; }"
        self.btn_start_test.setStyleSheet(style)
        self.btn_start_test.setText('Нет подключения')