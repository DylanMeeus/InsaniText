import time
from controllers import controllers
from models import editorobservers

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

currentFile = None # current filename

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
        self.wordLabel.setText("words: " + str(self.controller.getWordCount()))
        self.charcountLabel.setText("characters: " + str(self.controller.getCharCount()))
        self.cpmLabel.setText("cpm: " + str(self.controller.getCPM()))
        self.wpmLabel.setText("wpm: " + str(self.controller.getWPM()))


class InsaniTextEdit(QTextEdit):
    """  Custom class that is essentially an improved QTextEdit """

    BUFFER_THRESHOLD = 20
    def __init__(self, controller):
        super().__init__()
        self.lastpress = None
        self.controller = controller
        self.charbuffer = [] # Buffer for the characters that are in the current "count-cycle" for the WPM average.
        # some variables for timing how long we have been typing
        self.startbuffer_time = 0
        # Set solarized-light background
        self.setStyleSheet("background-color:#fdf6e3")

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
        if(delta < 2000):
            self.charbuffer.append(e.text())
            if len(self.charbuffer) >= self.BUFFER_THRESHOLD:
                # clean the buffer and calculate the wpm. Could do this based on timestamps as well though
                self.controller.dumpcharbuffer(self.charbuffer,self.startbuffer_time,self.lastpress)
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
        self.controller.setTextContent(self.toPlainText())


class EditorGUI(QMainWindow, editorobservers.EditorObserver):  # extends mainwindow
    """ GUI class for the editor """
    textArea = None
    controller = controllers.EditorController()

    def __init__(self, resolution):
        super().__init__()

        # subscribe to the model
        self.controller.subscribe(self)
        self.resolution = resolution

        self.setupGUI()
        self.setupShortcuts()


    def setupGUI(self):
        # create the menubar
        self.setupMenubar()

        # set size
        xSize = 600
        ySize = 600
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


    def save(self):
        """ save content from the text editor into a file"""
        global currentFile
        textInEditor = (self.textArea.toPlainText())

        if currentFile is None or currentFile == "":
            result = QFileDialog.getSaveFileName()
            if result:
                filename = result[0]
                # todo: allow non-txt extensions
                if(not len(filename.split("."))==2):
                    filename = filename+".txt"

                currentFile = filename


        file = open(currentFile,'w')
        file.write(textInEditor)

    def saveAs(self):
        global currentFile
        # prompt the user for saving the file
        result = QFileDialog.getSaveFileName()
        if result:
            filename = result[0]
            currentFile = filename
            file = open(currentFile,'w')
            file.write(self.textArea.toPlainText())


    def open(self):
        """ read a file into the text editor"""
        global currentFile
        result = QFileDialog.getOpenFileName()

        if result:
            currentFile = result[0]
            file = open(currentFile,'r')
            fileContent = (file.read())
            self.textArea.setText(fileContent)


    def update(self):
        pass

