""" gui file for the preferences framework """

from config import config

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class EditorPreferences(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupGUI()


    def setupGUI(self):
        self.resize(400,400)
        xPos = 400
        yPos = 400
        self.move(xPos,yPos)

        self.listwidget = QListWidget(self)
        self.listwidget.activated.connect(self.list_selection)


        self.tablewidget = QTableWidget(2,2,self)

        dock = QDockWidget()
        dock.setWidget(self.listwidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        self.populate_listwidget()

        self.setCentralWidget(self.tablewidget)

        self.show()


    def populate_listwidget(self):
        print("populating list widget..")
        conf = config.ConfigManager()
        sections = conf.parser.sections()
        for section in sections:
            self.listwidget.addItem(section)


    def populate_tablewidget(self):
        print("table widget")


    def list_selection(self):
        self.populate_tablewidget()