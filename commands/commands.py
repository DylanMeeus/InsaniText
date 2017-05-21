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
            self.controller.save_active_document()
        elif command == "save as":
            self.controller.save_active_document_as()
        elif command == "save exit":
            self.controller.save_active_document()
            sys.exit()
        elif command == "open":
            self.controller.open_file()
        else:
            print("Command not found!")
