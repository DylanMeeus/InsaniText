import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit,QMainWindow


""" GUI class for the editor"""
class EditorGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupGUI()

    def setupGUI(self):
        textArea = QTextEdit()
        self.setCentralWidget(textArea)

        self.resize(800,800)
        self.move(300,300)
        self.setWindowTitle('Editor')


        self.show()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = EditorGUI()
    sys.exit(app.exec_())