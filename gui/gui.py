import os
import time
import re

from config import config
from controllers import controllers
from models import editorobservers
from gui import preferences
from commands import gui as commandgui

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


config = config.ConfigManager()


# PyQt QkeyEvent keycodes
KEY_BACKSPACE = 16777219
KEY_LEFT = 16777234
KEY_RIGHT = 16777236
KEY_UP = 16777235
KEY_DOWN = 16777237
KEY_SHIFT = 16777248


class InsaniStatusbar(QStatusBar, editorobservers.EditorObserver):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        controller.subscribe(self)
        self.wordLabel = QLabel("words: 0")
        self.addWidget(self.wordLabel)
        self.charcountLabel = QLabel("characters: 0")
        self.addWidget(self.charcountLabel)
        self.cpmLabel = QLabel("cpm: 0")
        self.addWidget(self.cpmLabel)
        self.wpmLabel = QLabel("wpm: 0")
        self.addWidget(self.wpmLabel)

    def update(self):
        self.wordLabel.setText("words: " + str(self.controller.get_wordcount()))
        self.charcountLabel.setText("characters: " + str(self.controller.get_charcount()))
        self.cpmLabel.setText("cpm: " + str(self.controller.get_CPM()))
        self.wpmLabel.setText("wpm: " + str(self.controller.get_WPM()))


class InsaniTextEdit(QTextEdit, editorobservers.EditorObserver):
    """  Custom class that is essentially an improved QTextEdit """

    BUFFER_THRESHOLD = 20
    def __init__(self, controller):
        super().__init__()
        self.lastpress = None
        self.controller = controller
        self.controller.subscribe(self)
        self.charbuffer = [] # Buffer for the characters that are in the current "count-cycle" for the WPM average.
        # some variables for timing how long we have been typing
        self.startbuffer_time = 0
        # Set solarized-light background
        self.setStyleSheet("background-color:#fdf6e3")
        self.filtered_keys= [KEY_BACKSPACE,KEY_DOWN,KEY_UP,KEY_LEFT,KEY_RIGHT]


    def keyPressEvent(self,e):
        # convert tabs to space!
        if (e.text() == "\t"):
            event = QKeyEvent(QEvent.KeyPress, Qt.Key_Space, Qt.NoModifier," ")
            for i in range(4):
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(e)

        # measure time since last press
        now = int(round(time.time() * 1000))
        delta = now - self.lastpress if self.lastpress != None else 0
        self.lastpress = now

        if e.key() not in self.filtered_keys:
            if(delta < 2000):
                self.charbuffer.append(e.text())
                if len(self.charbuffer) >= self.BUFFER_THRESHOLD:
                    # clean the buffer and calculate the wpm. Could do this based on timestamps as well though
                    self.controller.dump_charbuffer(self.charbuffer, self.startbuffer_time, self.lastpress)
                    self.charbuffer = []
                    self.startbuffer_time = now # reset buffer time

                # if we reached this and the timer is still 0, start the timer
                if(self.startbuffer_time == 0):
                    self.startbuffer_time = now
            else:
                # start a new buffer, and dump the current one
                self.charbuffer = []
                self.startbuffer_time = now
                self.charbuffer.append(e.text())
        else:
            # filtered key
            self.charbuffer = []
            self.startbuffer_time = now

        self.controller.set_textcontent(self.toPlainText())

    def update(self):
        if self.toPlainText() != self.controller.get_textcontent():
            print(self.toPlainText()+'.')
            print("vs")
            print(self.controller.get_textcontent() + '.')
            self.setText(self.controller.get_textcontent())


class EditorGUI(QMainWindow, editorobservers.EditorObserver):  # extends mainwindow
    """ GUI class for the editor """
    textArea = None


    def __init__(self, resolution):
        super().__init__()
        self.controller = controllers.EditorController()

        # subscribe to the model
        self.controller.subscribe(self)
        self.resolution = resolution

        self.setupGUI()
        self.setupShortcuts()


    def setupGUI(self):
        # create the menubar
        self.setupMenubar()

        # set size
        xSize = config.get_default('InitialWidth')
        ySize = config.get_default('InitialHeight')
        self.resize(xSize,ySize)
        width = self.resolution[0]
        height = self.resolution[1]
        xPos = (width/2) - (xSize/2)
        yPos = height/2 - (ySize/2)
        self.move(xPos,yPos)
        self.setWindowTitle('InsaniText')

        #set icon
        self.setWindowIcon(QIcon("/resources/icons/icon.ico"))

        # text area
        self.textArea = InsaniTextEdit(self.controller)
        self.textArea.setTabStopWidth(20) # tab size (in pixels) is purely graphical. It does not convert to X spaces
        self.setCentralWidget(self.textArea)


        # create status bar
        self.setStatusBar(InsaniStatusbar(self.controller))


        # add sidebar
        self.filetree = InsaniFileTree(self.controller)
        dock = QDockWidget()
        dock.setWidget(self.filetree)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        self.controller.set_working_dir('.')

    # show the GUI
        self.show()

    def setupMenubar(self):
        menubar = self.menuBar()
        menubar.addMenu("File")
        menubar.addMenu("Preferences")


    def setupShortcuts(self):
        """ method to define shortcuts on the editor"""
        self.textArea.shortcut = QShortcut(QKeySequence("CTRL+S"),self)
        self.textArea.shortcut.activated.connect(self.save)

        self.textArea.shortcut = QShortcut(QKeySequence("CTRL+O"),self)
        self.textArea.shortcut.activated.connect(self.open)

        self.textArea.shortcut = QShortcut(QKeySequence("CTRL+SHIFT+S"),self)
        self.textArea.shortcut.activated.connect(self.saveAs)

        self.textArea.shortcut = QShortcut(QKeySequence("CTRL+P"),self)
        self.textArea.shortcut.activated.connect(self.open_preferences)

        self.textArea.shortcut = QShortcut(QKeySequence("CTRL+E"),self)
        self.textArea.shortcut.activated.connect(self.command_popup)

    def save(self):
        self.controller.save_active_document()

    def saveAs(self):
        self.controller.save_active_document_as()

    def open(self):
        """ read a file into the text editor"""
        self.controller.open_file()

    def open_preferences(self):
        preferences.EditorPreferences()

    def command_popup(self):
        x = commandgui.CommandPopup(self.controller, self)

    def loadText(self,text,doc):
        self.textArea.setText(text)
        self.controller.set_active_document(doc)

    def update(self):
        pass



def build_filetree(parent,path):
    """ attach all children to the parent """
    if os.path.isdir(path):
        children = os.listdir(path)
        for child in children:
            child_item = QStandardItem(child)
            child_item.setEditable(False)
            parent.appendRow(child_item)
            build_filetree(child_item,path+'/'+child)


class InsaniFileTree(QTreeView, editorobservers.EditorObserver):
    def __init__(self, controller):
        QTreeView.__init__(self)
        self.controller = controller
        self.controller.subscribe(self)
        self.root = '.'
        self.setModelRoot(self.root)
        self.doubleClicked.connect(self.double_clicked)

    def setModelRoot(self,root):
        self.root = root
        model = QStandardItemModel()
        rootItem = model.invisibleRootItem()
        # get all current children

        # Set launched dir as header name
        header_name = root.split('/')[-1:][0] if root != '.' else os.getcwd().split('/')[-1:][0]
        model.setHorizontalHeaderItem(0,QStandardItem(header_name))

        thisdir = os.listdir(root)
        for item in thisdir:
            standard_item = QStandardItem(item)
            standard_item.setEditable(False)
            build_filetree(standard_item,root+'/'+item)
            rootItem.appendRow(standard_item)

        self.setModel(model)

    def double_clicked(self):
        selected_index = self.selectedIndexes()[0]
        item = selected_index.model().itemFromIndex(selected_index)
        path = ""
        while(item != None):
            path = (item.text()) + '/' + path
            item = item.parent()

        path = (path[:-1]) # remove trailing /
        self.controller.set_document_by_path(path)

    def update(self):
        """ update root if necessary """
        if (self.controller.get_root() != None):
            if self.root != self.controller.get_root():
                self.root = self.controller.get_root()
                self.setModelRoot(self.root)




