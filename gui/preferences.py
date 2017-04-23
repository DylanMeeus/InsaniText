""" gui file for the preferences framework """

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



class EditorPreferences(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupGUI()
        self


    def setupGUI(self):
        self.resize(400,400)
        xPos = 400
        yPos = 400
        self.move(xPos,yPos)
        self.show()
