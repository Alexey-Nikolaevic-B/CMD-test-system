from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5 import QtCore

class LessonScreen(QDialog):
    def __init__(self):
        super(LessonScreen, self).__init__()
        loadUi('qt\Lesson.ui', self)

        self.lessons = ['']
        self.answers = ['']

        delegate = AlignJustify(self.table_lesson)
        self.table_lesson.setItemDelegateForColumn(1, delegate)

        delegate = AlignCenter(self.table_lesson)
        self.table_lesson.setItemDelegateForColumn(0, delegate)
        self.table_lesson.setItemDelegateForColumn(2, delegate)

        self.table_lesson.resizeColumnsToContents()
        self.table_lesson.resizeRowsToContents()

        header = self.table_lesson.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

    def set_lessons(self, lessons, answers):
        self.lessons = lessons
        self.answers = answers
        # self.table_lesson.clear()
        self.table_lesson.setRowCount(0)

        for task in self.lessons:
            rowPosition = self.table_lesson.rowCount()
            self.table_lesson.insertRow(rowPosition)
            self.table_lesson.setItem(rowPosition, 0, QTableWidgetItem(str(rowPosition+1)))
            self.table_lesson.setItem(rowPosition, 1, QTableWidgetItem(task))
            self.table_lesson.setItem(rowPosition, 2, QTableWidgetItem(answers[rowPosition]))

class AlignJustify(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignJustify, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignJustify

class AlignCenter(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignCenter, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter