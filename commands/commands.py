""" class to run CLI-like commands inside the application """
import sys, os

class CommandRunner:
    def __init__(self, controller):
        self.controller = controller


    def run(self,command):
        """ finds the course of action to take for the command"""
        if command == "exit":
            sys.exit()
        elif command == "reset metrics" or command == "resetmetrics": #todo: regex this so it accepts any combination
            self.controller.reset_metrics()
        elif command == "save":
            self.controller.save_active_document()
        elif command == "save as":
            self.controller.save_active_document_as()
        elif command == "save exit":
            self.controller.save_active_document()
            sys.exit()
        elif command == "open":
            self.controller.open_file()
        elif command.startswith("exec"):
            self.executeCLI(command)
        else:
            print("Command not found!")


    """ Execute a command on the CLI"""
    def executeCLI(self, command):
        cli_command = " ".join(command.split(" ")[1:])
        os.system(cli_command)
