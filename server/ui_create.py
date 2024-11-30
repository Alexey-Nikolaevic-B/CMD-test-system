from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import*
from PyQt5 import QtCore

import json
import random

class CreateScreen(QDialog):

    signal_show_lesson = pyqtSignal(str)

    def __init__(self):
        super(CreateScreen, self).__init__()

        self.random = False 

        self.lesson_name = ''

        self.lesson = {
            "type"  : "random",
            "n_1": 0,
            "n_2": 0,
            "n_3": 0,
            "n_4": 0
        }

        self.init_ui()

        self.btn_create.clicked.connect(self.setup_test)

    def setup_test(self):

        self.lesson_name = self.test_name.text()

        self.lesson["n_1"] = int(self.lbl_type_1.text())
        self.lesson["n_2"] = int(self.lbl_type_2.text())
        self.lesson["n_3"] = int(self.lbl_type_3.text())
        self.lesson["n_4"] = int(self.lbl_type_4.text())

        json_object = json.dumps(self.lesson, indent=4)
        
        # Writing to sample.json
        with open('lessons/' + self.lesson_name + '.json', "w") as outfile:
            outfile.write(json_object)

        self.signal_show_lesson.emit('lessons/' + self.lesson_name + '.json')


    def create_test(self):
        with open('lessons\pull\lesson_pull.json', encoding='utf-8') as config_file:
            data = json.load(config_file)

        tasks = random.sample(data['type_1'], self.lesson["n_1"]) + random.sample(data['type_2'], self.lesson["n_2"]) + random.sample(data['type_3'], self.lesson["n_3"]) + random.sample(data['type_4'], self.lesson["n_4"])


    def init_ui(self):
        loadUi('qt\Create.ui', self)

        self.lbl_type_1.setText(str(5))
        self.lbl_type_2.setText(str(5))
        self.lbl_type_3.setText(str(5))
        self.lbl_type_4.setText(str(5))

        style_btn = "QPushButton {color: rgb(0, 0, 0); border-radius: 5px; background-color : rgb(255, 230, 85); font: 16pt \"Consolas\"; } QPushButton::hover {color: rgb(0, 0, 0); background-color : rgb(255, 255, 127); font: 16pt \"Consolas\"; }"
        self.btn_create.setStyleSheet(style_btn)
