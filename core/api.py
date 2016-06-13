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

import main
import logging

from telegram.ext import MessageHandler

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
            inline_engine (InlineEngine): The InlineEngine object.
    """
    def __init__(self, updater, config, inline_engine):
        self.updater = updater
        self.main = main
        self.config = config
        self.inline_engine = inline_engine
        self.helptext = {}
        self.logger = logging.getLogger(__name__)

    def get_admins(self):
        """ Returns the specified list of bot admins from the config file """
        return self.config.parse_general()['adminlist']

    def is_admin(self, username):
        """
        Returns True if the given username is found in the admin list

        Args:
            username (String): The Telegram username of the user.
        """
        return username in self.get_admins()

    def is_sender_admin(self, update):
        """
        Returns True if the message sender's username is a bot admin

        Args:
            update (telegram.Update): The bot's update object.
        """
        return self.is_admin(update.message.from_user.username)

    def get_updater(self):
        """ Returns the active Updater object """
        return self.updater

    class Mod:
        """
        This class identifies the actual mod.

        Args:
                mod_id (int): A unique incremented identifier of the loaded mod.
                api  (HyphanAPI): The base api object the mod will use.
                name (string): The name of the mod.
        """
        def __init__(self, mod_id, api, name):
            self.mod_id = mod_id
            self.api = api
            self.name = name
            self.logger = logging.getLogger(__name__)

        def section_exists(self):
            """ Returns True if the mod's section exists in the config file """
            return self.name in self.api.config.get_sections()

        def get_config(self, key=None, fallback=None):
            """
            Returns the key value from the config file if specified,
            otherwise returns whether the mod's section exists in the
            config file.

            Args:
                key (String): The key to get from the config file.
                fallback (String): The default value if the key is not specified
                    in the config file.
            """
            if self.name not in self.api.config.get_sections():
                self.logger.warning("Missing config section for mod '%s'" % self.name)
                if key != None:
                    return self.api.config.access(self.name, key, fallback)
                else:
                    return False
            else:
                if key != None:
                    return self.api.config.access(self.name, key, fallback)
                else:
                    return True

        def set_config(self, data):
            """
            Sets and returns key data to append to the configuration file.

            Args:
                data (Dictionary): Dictionary object that contains key-value
                    data to append to the config file.
            """
            return self.api.config.append(self.name, data)

        def set_help(self, module, text):
            """
            Sets and stores the help text for a mod.

            Args:
                module (String): The mod's name.
                text (String): The help text.
            """
            self.api.helptext[str(module)] = text

        def get_help(self, module):
            """
            Retrieves and returns the mod's help text if it exists.

            Args:
                module (String): The mod's name.
            """
            module = ''.join(module)
            if module in self.api.helptext:
                return self.api.helptext[module]
            else:
                return "Help isn't coming..."

        def add_message_handler(self, filters, handler, pass_update_queue=False):
            """
            Workaround for MessageHandler's grouping issue present in the 4.0
            update of the python-telegram-bot library.
            This method, however, may only be used once per mod as each mod
            would belong to only one group and only one MessageHandler runs per
            group.
            """
            return self.api.updater.dispatcher.add_handler(
                MessageHandler(filters, handler, pass_update_queue), group=self.mod_id)

        def add_inline_query(self, name, callback):
            """
            Registers an Inline Bot feature to HyphanBot.

            Args:
                name (string): A unique identifiable name for the feature.
                callback (function): A function that takes ``bot, update`` as
                    positional arguments and is used to handle inline queries.
                    It will be called whenever the user activates the feature
                    from the Inline Bot settings.
            """
            if not self.api.inline_engine.is_feature(name):
                self.api.inline_engine.add_feature(name, callback)
