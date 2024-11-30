from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import*
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtWidgets, QtGui

from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore

import threading
import time
import json

import ui_lesson
import ui_create

class MainScreen(QDialog):

    signal_toggle_test = pyqtSignal(list)
    signal_show_lesson = pyqtSignal(str)

    def __init__(self):
        super(MainScreen, self).__init__()

        self.number_of_tasks = 10
        self.test_settings = ''

        self.count = True

        self.c = 300
        self.toggle = True

        self.lessson_name = ''
        self.tasks        = ['d']
        self.checks       = ['q']
        self.answers      = ['w']
        self.mark         = [60, 80, 85]
        self.lessson      = 0

        self.lessson_window = ui_lesson.LessonScreen()
        self.create_window  = ui_create.CreateScreen()

        self.create_window.signal_show_lesson.connect(self.show_lesson)

        self.init_ui()

        self.thread_counter = threading.Thread(target=self.counter, daemon=True)

        self.btn_start_test.clicked.connect(self.launch_test)
        self.btn_save_settings.clicked.connect(self.save_settings)
        self.btn_choose.clicked.connect(self.choose_lesson)
        self.btn_name.clicked.connect(self.show_lesson)
        self.btn_create.clicked.connect(self.show_create)


    def show_create(self):
        self.create_window.show()  

    def choose_lesson(self):
        lesson, _ = QFileDialog.getOpenFileName(self, 'Open file', "lessons",'*.json')

        if lesson != '':
            with open(lesson, encoding='utf-8') as config_file:
                data = json.load(config_file)

            self.tasks   = data['tasks']
            self.checks  = data['checks']
            self.answers = data['answers']

    def show_lesson(self):
        self.lessson_window.set_lessons(self.tasks, self.answers)
        self.lessson_window.show()  

    def save_settings(self):    
        self.c = int(self.lbl_time.text()) * 60

        self.mark[0] = int(self.mark_3.text())
        self.mark[1] = int(self.mark_4.text())
        self.mark[2] = int(self.mark_5.text())

        self.test_settings = ['start']
        self.test_settings.append(self.tasks)
        self.test_settings.append(self.checks)
        self.test_settings.append(self.mark)
        self.test_settings.append(self.c)

    def launch_test(self):
        if self.toggle == True:
            self.thread_counter.start()
            self.toggle = False
            self.signal_toggle_test.emit(self.test_settings)
            self.btn_start_test.setText('Закончить тест')
        else:
            self.signal_toggle_test.emit(['finish'])
            self.btn_start_test.setText('Запустить тест')
            self.count = False


    def update_users(self, id, name, current, correct):
        self.table_1.setItem(int(id)-1, 0, QTableWidgetItem(str(id)))
        self.table_1.setItem(int(id)-1, 1, QTableWidgetItem(str(name)))
        self.table_1.setItem(int(id)-1, 2, QTableWidgetItem(str(current)))
        self.table_1.setItem(int(id)-1, 3, QTableWidgetItem(str(correct)))
        self.table_1.setItem(int(id)-1, 4, QTableWidgetItem('—'))

    def set_mark(self, id, mark):
        self.table_1.setItem(int(id)-1, 4, QTableWidgetItem(str(mark)))

    def counter(self):
        while self.count and self.c >= 0:
            mins, secs = divmod(self.c, 60) 
            timer = '{:02d}:{:02d}'.format(mins, secs) 
            print(timer, end="\r") 

            self.c = self.c - 1
            self.lbl_counter.setText(str(timer))

            time.sleep(1)
        
        self.signal_toggle_test.emit(['finish'])

    def init_ui(self):
        image = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap("img\login_1.jpg")
        image.setPixmap(pixmap)
        image.setGeometry(QtCore.QRect(0, 0, 2000, 1100))
        image.setScaledContents(True)
        image.show()

        loadUi('qt\Main.ui', self)
        self.mark_3.setText(str(self.mark[0]))
        self.mark_4.setText(str(self.mark[1]))
        self.mark_5.setText(str(self.mark[2]))

        self.lbl_time.setText(str(int(self.c  / 60)))

        self.save_settings()

        style_btn = "QPushButton {color: rgb(0, 0, 0); border-radius: 5px; background-color : rgb(255, 230, 85); font: 16pt \"Consolas\"; } QPushButton::hover {color: rgb(0, 0, 0); background-color : rgb(255, 255, 127); font: 16pt \"Consolas\"; }"
        style_btn_1 = "QPushButton {color: rgb(0, 0, 0); border-radius: 10px; background-color : rgb(255, 230, 85); font: 30pt \"Consolas\"; } QPushButton::hover {color: rgb(0, 0, 0); background-color : rgb(255, 255, 127); font: 30pt \"Consolas\"; }"
        self.btn_save_settings.setStyleSheet(style_btn)
        self.btn_start_test.setStyleSheet(style_btn_1)
        self.btn_name.setStyleSheet(style_btn)
        self.btn_create.setStyleSheet(style_btn)

        header = self.table_1.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

        delegate = AlignCenter(self.table_1)
        self.table_1.setItemDelegateForColumn(0, delegate)
        self.table_1.setItemDelegateForColumn(1, delegate)
        self.table_1.setItemDelegateForColumn(2, delegate)
        self.table_1.setItemDelegateForColumn(3, delegate)
        self.table_1.setItemDelegateForColumn(4, delegate)

class AlignCenter(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignCenter, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter