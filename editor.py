import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


currentFile = None # current filename


"""  Custom class that is essentially an improved QTextEdit """
class InsaniTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()

# todo: override keypress events

""" GUI class for the editor"""
class EditorGUI(QMainWindow): # extends mainwindow

    textArea = None

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
        self.textArea = InsaniTextEdit()
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

    """ read a file into the text editor"""
    def open(self):
        global currentFile
        result = QFileDialog.getOpenFileName()

        if result:
            currentFile = result[0]
            file = open(currentFile,'r')
            fileContent = (file.read())
            self.textArea.setText(fileContent)


    def wordCount(self,event):
        text = self.textArea.toPlainText()
        print(text)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = EditorGUI()
    sys.exit(app.exec_())