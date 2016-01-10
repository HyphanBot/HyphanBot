'''
This file is part of Hyphan.
Hyphan is free software: you can redistribute it and/or modify
it under the terms of the GNU Afferno General Public License as published 
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Hyphan is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Afferno General Public License for more details.

You should have received a copy of the GNU Afferno General Public 
License along with Hyphan.  If not, see 
https://www.gnu.org/licenses/agpl-3.0.html>.
'''
"""
This module contains the HyphanAPI class which intends to provide api 
for Hyphan's mods.
"""
from os import mkdir
from os.path import expanduser
from configparser import SafeConfigParser

import pathlib
import main

class HyphanAPI:
        """
        This class provides API for making Hyphan mods communicate better 
        with the internal core of Hyphan and the Telegram bot module.

        Args:
                updater (telegram.Updater): The updater object that could be 
                        used in mods.
        """
        def __init__(self, updater):
                self.updater = updater
                self.main    = main

        ''' fucking broken piece of shit...
        def restart_bot(self):
                self.updater.stop()
                time.sleep(1)
                main.start_bot()
        '''

        def get_admins(self):
                return self.config("general", "admins").split()
                
        def get_updater(self):
                return self.updater

        def config(self, section, key):
                HOME            = expanduser("~")
                XDG_CONFIG      = HOME + '/.config/hyphan/config.ini'
                CONFIG_FALLBACK = HOME + '~/.hyphan/config.ini'
                LAST_HOPE       = HOME + '~/.hyphanrc'

                safeconfig = SafeConfigParser()
                
                if pathlib.Path(XDG_CONFIG).exists():
                        safeconfig.read(XDG_CONFIG)
                elif pathlib.Path(CONFIG_FALLBACK).exists():
                        safeconfig.read(CONFIG_FALLBACK)
                elif pathlib.Path(LAST_HOPE).exists():
                        safeconfig.read(LAST_HOPE)

                try:
                        safeconfig.get(section, key)
                except Exception:
                        print("Hyphan couldn't find that value!\n")
                else:
                        return safeconfig.get(section, key)

                


