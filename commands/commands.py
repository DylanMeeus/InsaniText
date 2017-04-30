""" class to run CLI-like commands inside the application """
import sys

class CommandRunner:
    def __init__(self):
        pass


    def run(self,command):
        """ finds the course of action to take for the command"""
        if command == "exit":
            sys.exit()
