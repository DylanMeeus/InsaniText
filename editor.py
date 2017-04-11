import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


currentFile = None # current filename

""" GUI class for the editor"""
class EditorGUI(QMainWindow): # extends mainwindow

    textArea = None
    def __init__(self):
        super().__init__()


        self.setupGUI()

    def setupGUI(self):
        # set size
        self.resize(800,800)
        self.move(500,300)
        self.setWindowTitle('Editor')

        # text area
        self.textArea = QTextEdit()
        self.setCentralWidget(self.textArea)


        #short cut
        self.textArea.shortcut = QShortcut(QKeySequence("CTRL+S"),self)
        self.textArea.shortcut.activated.connect(self.save)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu("File")



    # show the GUI
        self.show()


    def save(self):
        global currentFile
        print("Save action")
        textInEditor = (self.textArea.toPlainText())

        if currentFile is None or currentFile == "":
            result = QFileDialog.getSaveFileName()
            if result:
                filename = result[0]
                if(not filename.endswith(".txt")):
                    filename = filename+".txt"
                    currentFile = filename

        file = open(currentFile,'w')
        file.write(textInEditor)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = EditorGUI()
    sys.exit(app.exec_())