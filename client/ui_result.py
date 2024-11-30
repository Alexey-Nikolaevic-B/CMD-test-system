from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

class ResultScreen(QDialog):
    def __init__(self):
        super(ResultScreen, self).__init__()
        self.init_ui()

        self.mark = 2

    def set_mark(self, x, y, z):
        self.mark = x
        self.lbl_result.setText(str(self.mark))

        self.lbl_result1.setText(str(y) + '/' + str(z))

        if x == 2:
            self.setStyleSheet('background-color: rgb(255, 71, 83)')
        if x == 3:
            self.setStyleSheet('background-color: rgb(255, 142, 76)')
        if x == 4:
            self.setStyleSheet('background-color: rgb(255, 230, 85)')
        if x == 5:
            self.setStyleSheet('background-color: rgb(147, 181, 72)')


    def init_ui(self):
        loadUi('qt\Result.ui', self)