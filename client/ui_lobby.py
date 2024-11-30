from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

class LobbyScreen(QDialog):
    def __init__(self):
        super(LobbyScreen, self).__init__()
        loadUi('qt\Lobby.ui', self)