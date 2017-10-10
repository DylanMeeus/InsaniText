from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


"""
Diacritic panel
"""
class DiacriticPanel(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupGUI()



    def setupGUI(self):

        # set up buttons for all the diacritics..
        
        # characters = dict(
        #     aup = 'á',
        #     eup = 'é',
        #     iup = 'í',
        #     nj = 'ñ',
        #     oup = 'ó',
        #     uup = 'ú',
        #     uumlaut = 'ü',
        #     reversequestion = '¿',
        #     reversebang = '¡'
        # )

        characters = ['á','é','í','ñ','ó','ú','ü','¿','¡']

        grid = QGridLayout()
        i = 0
        j = 0
        for char in characters:
            button = QPushButton(char)
            button.clicked.connect(self.make_handler(char))
            grid.addWidget(button,i,j)
            j += 1
            if j % 5 == 0:
                i += 1
                j = 0


        self.setLayout(grid)

    def make_handler(self,char):
        return lambda: self.handle_click(char)

    def handle_click(self, char):
        print(char)
