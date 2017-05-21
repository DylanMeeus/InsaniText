""" file to deal with the configuration of the editor """

import configparser
import os

class ConfigManager:
    """ class to get and set configuration properties """



    def __init__(self):
        this_dir = os.path.dirname(__file__)
        self.config_file = os.path.join(this_dir, 'settings.ini')
        self.parser = configparser.ConfigParser()
        self.parser.read(self.config_file)
        print("Loaded config")


    def get_default(self,key):
        return self.parser.getint('DEFAULT', key)


    def get_value(self, section, key):
        return self.parser.get(section,key)


    def set_default(self,key):
        if self.get_default(key) == None: # The key does not exist!
            return



