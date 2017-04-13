import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


currentFile = None # current filename


""" class that represents the data/state of the editor """
class EditorModel():
    def __init__(self):
        self.wordCount = 0
        self.textContent = ""

    def setText(self,text):
        self.textContent = text
        self.updateState()
        print(self.wordCount)

    # When the text changes, we might need to update multiple variables.
    def updateState(self):
        self.wordCount = self.countWords()


    def countWords(self):
        return len(self.textContent.split(" "))

""" controller for the editor """
class EditorController():
    def __init__(self):
        self.editorModel = EditorModel()

    def setTextContent(self,textContent):
        self.editorModel.setText(textContent)
        
"""  Custom class that is essentially an improved QTextEdit """
class InsaniTextEdit(QTextEdit):
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def keyPressEvent(self,e):
        super().keyPressEvent(e)
        self.controller.setTextContent(self.toPlainText())

# todo: override keypress events

""" GUI class for the editor """
class EditorGUI(QMainWindow): # extends mainwindow

    textArea = None
    controller = EditorController()
    
    def __init__(self):
        super().__init__()
        self.setupGUI()
        self.setupShortcuts()

    def setupGUI(self):
        # set size
        self.resize(800,800)
        self.move(500,300)
        self.setWindowTitle('InsaniText')

        #set icon
        self.setWindowIcon(QIcon("/resources/icons/icon.ico"))

        # text area
        self.textArea = InsaniTextEdit(self.controller)
        self.textArea.setTabStopWidth(20) # tab size (in pixels) is purely graphical. It does not convert to X spaces
        self.setCentralWidget(self.textArea)


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





if __name__ == '__main__':
    print("started editor")
    app = QApplication(sys.argv)
    gui = EditorGUI()
    sys.exit(app.exec_())
