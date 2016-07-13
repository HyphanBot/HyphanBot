# This file is part of Hyphan.
# Hyphan is free software: you can redistribute it and/or modify
# it under the terms of the GNU Afferno General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hyphan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Afferno General Public License for more details.
#
# You should have received a copy of the GNU Afferno General Public
# License along with Hyphan.  If not, see
# https://www.gnu.org/licenses/agpl-3.0.html>.
"""
This file has the mod specific api.
"""
import logging
from telegram.ext import MessageHandler


class Mod(object):
    """ This class identifies the actual mod.

    :param mod_id (int): A unique incremented identifier of the loaded mod.
    :param api (HyphanAPI): The base api object the mod will use.
    :param name (string): The name of the mod.
    """
    def __init__(self, updater, inline_engine):
        self.mod_id = None
        self.name = None
        self.helptext = {}
        self.inline_engine = inline_engine
        self.updater = updater

    def set_help(self, module, text):
        """ Sets and stores the help text for a mod.

        :param module (String): The mod's name.
        :param text (String): The help text.
        """
        self.helptext[str(module)] = text

    def get_help(self, module):
        """ Retrieves and returns the mod's help text if it exists.

        :param module (String): The mod's name.
        """
        module = ''.join(module)
        if module in self.helptext:
            return self.helptext[module]
        else:
            return "Help isn't coming..."

    def add_message_handler(self, filters, handler, pass_update_queue=False):
        """ Workaround for MessageHandler's grouping issue present in the 4.0
        update of the python-telegram-bot library.
        This method, however, may only be used once per mod as each mod
        would belong to only one group and only one MessageHandler runs per
        group.
        """
        return self.updater.dispatcher.add_handler(
            MessageHandler(filters, handler, pass_update_queue),
            group=self.mod_id)

    def add_inline_query(self, name, callback):
        """ Registers an Inline Bot feature to HyphanBot.

        :param name (string): A unique identifiable name for the feature.
        :param callback (function): A function that takes ``bot, update`` as
               positional arguments and is used to handle inline queries.
               It will be called whenever the user activates the feature
               from the Inline Bot settings.
        """
        # currently broken
        pass
#        if not self.inline_engine.is_feature(name):
#            self.inline_engine.add_feature(name, callback)
