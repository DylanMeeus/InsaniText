import sys
import re

from gui import gui
from models import editorobservers

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *




## Observable and observer classes (there are no interfaces in python apperantly)



if __name__ == '__main__':
    print("started editor")
    app = QApplication(sys.argv)

    # determine screen size for GUI
    screen_rect = app.desktop().screenGeometry()
    resolution = (screen_rect.width(),screen_rect.height())
    ui = gui.EditorGUI(resolution)
    sys.exit(app.exec_())
