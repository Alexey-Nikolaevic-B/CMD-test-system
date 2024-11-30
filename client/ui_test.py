from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.uic import loadUi
from PyQt5 import QtGui, QtCore
import re
import threading
import time
import os

import subprocess
import shlex

class TestScreen(QDialog):

    signal_update_status = pyqtSignal(list)
    signal_goto_result   = pyqtSignal(list)

    def __init__(self):
        super(TestScreen, self).__init__()

        self.cur_task = 0
        self.c = 300
        self.tasks = ['Создай файл file1.txt на рабочем столе Создай файл file1.txt на рабочем столеСоздай файл file1.txt на рабочем столеСоздай файл file1.txt на рабочем столеСоздай файл file1.txt на рабочем столеСоздай файл file1.txt на рабочем столеСоздай файл file1.txt на рабочем столе', 'Создай папку TestDir на рабочем столе', 'Переименуй файл file1.txt в myfile.txt']
        self.checks = ['1', '2', 'Переименуй файл file1.txt в myfile.txt']
        self.n = len(self.tasks)
        self.grades = [1, 2, 3, 4]
        self.mark = 2
        self.correct = [0]*10
        self.answers = ['']*10

        self.cur_dir = 'C:\dev\cmd_test_system\server\lessons'
        
        self.init_ui()
        self.thread_counter = threading.Thread(target=self.counter, daemon=True)

        self.ln_cmd.returnPressed.connect(self.check)

        self.btn_backward.clicked.connect(lambda: self.update(0))
        self.btn_forward.clicked.connect(lambda: self.update(1))
        self.btn_end_test.clicked.connect(self.gotoResultScreen)

    def cmd(self, command_line):
        if "icacls" in command_line:
            return

        os.chdir(self.cur_dir)
        args = shlex.split(command_line)
        process = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        output = output.decode('cp866')
    
        pattern_1 = re.compile('cd ?\.\.')
        pattern_2 = re.compile('(cd *)(C:.+)')
        pattern_3 = re.compile('(cd *)(.+)')

        temp_dir = self.cur_dir 

        if pattern_1.match(command_line):
            temp_dir = re.sub(r'\\[^\\]*$', '', self.cur_dir)
        elif pattern_2.match(command_line):
            result = re.search(r'(cd *)(.+)', command_line)

            temp_dir = result.group(2)
        elif pattern_3.match(command_line):
            result = re.search(r'(cd *)(.+)', command_line)
            temp_dir = self.cur_dir + "/" +result.group(2)
    
        if os.path.exists(temp_dir):
            self.cur_dir = temp_dir

        self.lbl_output.setText(output)


    def check(self):
        pattern = re.compile(self.checks[self.cur_task])
        command = self.ln_cmd.text()
        if pattern.match(command):
            self.ln_cmd.setStyleSheet("color: rgb(0, 0, 0); font:16pt \"Consolas\"; background-color: rgb(147, 181, 72);")
            self.correct[self.cur_task] = 1
            self.answers[self.cur_task] = command

        n = self.correct.count(1)
        self.signal_update_status.emit([self.cur_task + 1, n])

        self.cmd(command)

    def counter(self):
        while self.c >= 0:
            mins, secs = divmod(self.c, 60) 
            timer = '{:02d}:{:02d}'.format(mins, secs) 
            print(timer, end="\r") 

            self.c = self.c - 1
            self.lbl_time.setText(str(timer))

            time.sleep(1)
        
        self.gotoResultScreen()

    def update(self, option):
        self.ln_cmd.setStyleSheet("color: rgb(255, 255, 255); font:16pt \"Consolas\"; background-color: rgb(50, 50, 50);")
        if (option == 0) and (self.cur_task > 0): 
            self.cur_task = self.cur_task - 1
        if (option == 1) and (self.cur_task < len(self.tasks)-1):
            self.cur_task = self.cur_task + 1

        self.btn_backward.setEnabled(True)
        self.btn_forward.setEnabled(True)
        self.btn_end_test.hide()
        if (self.cur_task < 1):
            self.btn_backward.setEnabled(False)
        if (self.cur_task == len(self.tasks)-1):
            self.btn_forward.setEnabled(False)
            self.btn_end_test.show()

        self.lbl_task_num.setText("Задание " + str(self.cur_task + 1))
        self.lbl_task.setText(self.tasks[self.cur_task])
        self.ln_cmd.setText('')

        n = self.correct.count(1)
        self.signal_update_status.emit([self.cur_task + 1, n])

    def gotoResultScreen(self):
        i = self.correct.count(1)
        per = i / self.n * 100
        self.mark = 2
        if per >= self.grades[2]:
            self.mark = 5
        elif per >= self.grades[1]:
            self.mark = 4
        elif per >= self.grades[0]:
            self.mark = 3
        self.signal_goto_result.emit([self.mark, i, self.n])

    def set_settings(self, tasks, checks, grades, c):
        self.tasks  = tasks
        self.checks = checks
        self.grades = grades
        self.c      = c 
        self.n      = len(self.tasks)

        self.lbl_task.setText(self.tasks[self.cur_task])
        self.thread_counter.start()

    def startTimer(self):
        self.thread_counter.start()

    def init_ui(self):
        loadUi('qt\Test.ui', self)
        
        self.btn_backward.setIconSize(QtCore.QSize(100,40))
        self.btn_forward.setIconSize(QtCore.QSize(100,40))
        style_btn = "QPushButton {color: rgb(0, 0, 0); border-radius: 5px; background-color : rgb(255, 230, 85); font: 25pt \"Consolas\"; } QPushButton::hover {color: rgb(0, 0, 0); background-color : rgb(255, 255, 127); font: 25pt \"Consolas\"; }"
        self.btn_backward.setStyleSheet(style_btn) 
        self.btn_forward.setStyleSheet(style_btn) 
        self.btn_end_test.setStyleSheet(style_btn) 

        self.lbl_task.setText(self.tasks[self.cur_task])

        self.btn_backward.setEnabled(False)
        self.btn_end_test.hide()


    