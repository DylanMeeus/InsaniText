""" class to run CLI-like commands inside the application """
import sys

class CommandRunner:
    def __init__(self, controller):
        self.controller = controller


    def run(self,command):
        """ finds the course of action to take for the command"""
        if command == "exit":
            sys.exit()
        elif command == "save":
            self.controller.saveActiveDocument()
        elif command == "save as":
            self.controller.saveActiveDocumentAs()
        elif command == "open":
            self.controller.openFile()
