""" file to deal with the configuration of the editor """

import configparser
import os

class ConfigManager:
    """ class to get and set configuration properties """



    def __init__(self):
        self.config_file = os.path.abspath('config/settings.ini')
        self.parser = configparser.ConfigParser()
        self.parser.read(self.config_file)


    def get_default(self,key):
        return self.parser.getint('DEFAULT',key)

    def set_default(self,key):
        if self.get_default(key) == None: # The key does not exist!
            return



