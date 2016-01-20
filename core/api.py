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

from os import mkdir
from os.path import expanduser

import pathlib
import main
import logging

"""
This module contains the HyphanAPI class which intends to provide api 
for Hyphan's mods.
"""

class HyphanAPI:
        """
        This class provides API for making Hyphan mods communicate better 
        with the internal core of Hyphan and the Telegram bot module.

        Args:
                updater (telegram.Updater): The updater object that could be 
                        used in mods.
                config  (Configurator): The configuration object that is
                        used to parse and access the configuration file.
        """
        def __init__(self, updater, config):
                self.updater = updater
                self.main    = main
                self.config  = config
                self.logger  = logging.getLogger(__name__)

        ''' fucking broken piece of shit...
        def restart_bot(self):
                self.updater.stop()
                time.sleep(1)
                main.start_bot()
        '''

        def get_admins(self):
                return self.config.parse_general()['adminlist']

        def is_admin(self, username):
                return username in self.get_admins()

        def is_sender_admin(self, update):
                return self.is_admin(update.message.from_user.username)
                
        def get_updater(self):
                return self.updater

        class Mod:
                """
                This class identifies the actual mod.

                Args:
                        api  (HyphanAPI): The base api the mod will use.
                        name    (string): The name of the mod.
                """
                def __init__(self, api, name):
                        self.api  = api
                        self.name = name
                        self.logger  = logging.getLogger(__name__)

                def section_exists(self):
                        if self.name in self.api.config.get_sections():
                                return True
                        else:
                                return False

                def get_config(self, key=None, fallback=None):
                        if self.name not in self.api.config.get_sections():
                                self.logger.warn("Missing config section for mod '%s'" % self.name)
                                return False
                        else:
                                if not key == None:
                                        return self.api.config.access(self.name, key, fallback)
                                else:
                                        return True

                def set_config(self, data):
                        return self.api.config.append(self.name, data)
