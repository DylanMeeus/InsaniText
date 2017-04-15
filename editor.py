import sys
import re

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


currentFile = None # current filename



## Observable and observer classes (there are no interfaces in python apperantly)

class EditorObservable():
    def __init__(self):
        self.observers = []

    def addObserver(self,observer):
        self.observers.append(observer)

    def notify(self):
        for observer in self.observers:
            observer.update()

class EditorObserver():
    def update(self):
        pass



""" class that represents the data/state of the editor """
class EditorModel(EditorObservable):
    def __init__(self):
        super().__init__()
        self.wordCount = 0
        self.textContent = ""

    def setText(self,text):
        self.textContent = text
        self.updateState()
        super().notify()

    # When the text changes, we might need to update multiple variables.
    def updateState(self):
        self.wordCount = self.countWords()


    def countWords(self):
        words = re.split("[' '|'\\n']",self.textContent)
        # filter out empty blocks that somehow happen
        words = list(filter(lambda k: k != '',words))
        return len(words)

""" controller for the editor """
class EditorController():
    def __init__(self):
        self.editorModel = EditorModel()

    def setTextContent(self,textContent):
        self.editorModel.setText(textContent)

    def subscribe(self,object):
        self.editorModel.addObserver(object)

    def getWordCount(self):
        return self.editorModel.countWords()


class InsaniStatusbar(QStatusBar, EditorObserver):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        controller.subscribe(self)
        self.testLabel = QLabel("words: 0")
        self.addWidget(self.testLabel)

    def update(self):

        self.testLabel.setText("words: " + str(self.controller.getWordCount()))

        
"""  Custom class that is essentially an improved QTextEdit """
class InsaniTextEdit(QTextEdit):
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        # Set solarized-light background
        self.setStyleSheet("background-color:#fdf6e3")

    def keyPressEvent(self,e):
        super().keyPressEvent(e)
        self.controller.setTextContent(self.toPlainText())

# todo: override keypress events

""" GUI class for the editor """
class EditorGUI(QMainWindow, EditorObserver): # extends mainwindow

    textArea = None
    controller = EditorController()
    
    def __init__(self, resolution):
        super().__init__()

        # subscribe to the model
        self.controller.subscribe(self)

        self.setupGUI()
        self.setupShortcuts()
    

    def setupGUI(self):
        # set size
        xSize = 600
        ySize = 600
        self.resize(xSize,ySize)
        width = resolution[0]
        height = resolution[1]
        xPos = (width/2)  - (xSize/2)
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


        menubar = self.menuBar()
        fileMenu = menubar.addMenu("File")

        # show the GUI
        self.show()

    """ method to define shortcuts on the editor"""
    def setupShortcuts(self):
        self.textArea.shortcut = QShortcut(QKeySequence("CTRL+S"),self)
        self.textArea.shortcut.activated.connect(self.save)

        self.textArea.shortcut = QShortcut(QKeySequence("CTRL+O"),self)
        self.textArea.shortcut.activated.connect(self.open)

        self.textArea.shortcut = QShortcut(QKeySequence("CTRL+SHIFT+S"),self)
        self.textArea.shortcut.activated.connect(self.saveAs)

    """ save content from the text editor into a file"""
    def save(self):
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

    """ read a file into the text editor"""
    def open(self):
        global currentFile
        result = QFileDialog.getOpenFileName()

        if result:
            currentFile = result[0]
            file = open(currentFile,'r')
            fileContent = (file.read())
            self.textArea.setText(fileContent)



    def update(self):
        pass




if __name__ == '__main__':
    print("started editor")
    app = QApplication(sys.argv)

    # determine screen size for GUI
    screen_rect = app.desktop().screenGeometry()
    resolution = (screen_rect.width(),screen_rect.height())
    gui = EditorGUI(resolution)
    sys.exit(app.exec_())
