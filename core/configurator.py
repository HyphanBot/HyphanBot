from configparser import SafeConfigParser
from os import mkdir
from os.path import expanduser
from main import HYPHAN_DIR

import pathlib
import sys
import logging

'''
This module is used to manage the configuration file for Hyphan.
'''

HOME         = expanduser("~")
CONFIG_PATHS = [
    # Checks if there is the config file in Hyphan's root directory (by default there shouldn't be).
    HYPHAN_DIR + "/config.ini",

    # Checks in the user's home directory.
    HOME + '/.config/hyphan/config.ini', # This will be created by default.
    HOME + '/.hyphan/config.ini',
    HOME + '/.hyphanrc'
]

class Configurator:
    """docstring for Configurator"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = self.__init_config()

    def __init_config(self):
            logger = self.logger
            config = SafeConfigParser()

            # Look in the CONFIG_PATHS for the config file
            for cfile in CONFIG_PATHS:
                if pathlib.Path(cfile).exists():
                    logger.info("Configuration file has been found at: " + cfile)
                    config.read(cfile)
                    self.workingconfig = cfile
                    return config

            # Default config path
            XDG_CONFIG = HOME + '/.config/hyphan/config.ini'

            logger.warn("No configuration file has been found. Starting interactive prompt...")
            print()
            answer = input("Do you want me to copy the standard boiler plate to ~/.config/hyphan/config.ini? [Y/n] ")
            if not (answer.lower() == "n" or answer.lower() == "no"):
                answer = input("Do you want to enter the info interactively? [Y/n] ")
                if not (answer.lower() == "n" or answer.lower() == "no"):
                        mkdir(HOME + '/.config/hyphan')
                        writefile = open(XDG_CONFIG, "w")
                        token     = input("Telegram bot token: ")
                        admins    = input("Bot administrators (Telegram usernames seperated by space): ")
                        writefile.write(str(
"""[general]
token   = %s
admins  = %s""" % (token, admins)))
                        writefile.close()
                else:
                        mkdir(HOME + '/.config/hyphan')
                        writefile = open(XDG_CONFIG, "w")
                        writefile.write(str(
"""[general]
token   = TOKEN
admins  = admin1 admin2"""))
                        writefile.close()
                        print("Don't forget to edit the file before you start the program again!")
            sys.exit(2) # No such file or directory.

    def refresh_config(self):
        self.config = None
        self.config = self.__init_config()

    def parse_general(self):
        config = self.config
        return {
            "token"     : config.get("general", "token"),
            "adminstr"  : config.get("general", "admins"),
            "adminlist" : config.get("general", "admins").split(" ")
        }

    def access(self, section, key):
        return self.config.get(section, key)

    def append(self, section, data):
        if not section == "general":
            self.config[section] = data
            with open(self.workingconfig, 'w') as writefile:
                self.config.write(writefile)
        else:
            return False

    def get_sections(self):
        return self.config.sections()
