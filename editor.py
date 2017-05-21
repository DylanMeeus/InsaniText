import sys,os

from gui import gui, preferences

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



def parse_cli_files(args):
    """ Parse the files that are passed on the CLI, to open all of them in the editor"""
    return args[1] if(len(args) > 1) else None

if __name__ == '__main__':
    print("started editor")

    filename = parse_cli_files(sys.argv)
    fileContent = open(filename,'r').read() if filename != None else ""

    app = QApplication(sys.argv)
    # determine screen size for GUI
    screen_rect = app.desktop().screenGeometry()
    resolution = (screen_rect.width(),screen_rect.height())
    ui = gui.EditorGUI(resolution)
    ui.loadText(fileContent,filename)
    sys.exit(app.exec_())

