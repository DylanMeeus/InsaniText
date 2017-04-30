""" gui for the command runner """

from commands import commands
from controllers import controllers

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class CommandPopup(QInputDialog):
    """ popup for a single-line command to be entered"""
    def __init__(self, controller, parent = None, ):
        super().__init__(parent = parent)
        self.setupGUI()
        self.command_runner = commands.CommandRunner(controller)

    def setupGUI(self):
        self.setLabelText("Command:")
        self.show()

    def done(self, result):
        super().done(result)
        print("done")
        if result == 1:
            print(self.textValue())
            self.command_runner.run(self.textValue())


class CommandWindow(QMainWindow):
    def __init__(self):
        """ a command window that display input + output like a terminal window"""
        super().__init__()