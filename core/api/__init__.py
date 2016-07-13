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
import logging

from subprocess import Popen, PIPE
from telegram.ext import MessageHandler
from core.api.mod import *
from core.api.config import *

"""
This module contains the HyphanAPI class which intends to provide api for Hyphan's mods.
"""

class HyphanAPI(Mod, Configuration):
    """ This class provides API for making Hyphan mods communicate better
    with the internal core of Hyphan and the Telegram bot module.

    :param updater (telegram.Updater): The updater object that could be
                    used in mods.
    :param config  (Configurator): The configuration object that is
                    used to parse and access the configuration file.
    :param inline_engine (InlineEngine): The InlineEngine object.
    """
    def __init__(self, updater, inline_engine, config):
        Mod.__init__(self, updater, inline_engine)
        Configuration.__init__(self, config)
        self.logger = logging.getLogger(__name__)
        self.hyphan_directory = self.run_command("pwd")
#        super().__init__(updater=updater, inline_engine=inline_engine, config=config)
        self.updater = updater

    def get_updater(self):
        """ Returns the active Updater object """
        return self.updater

    # decide whether this should be a helper function or a real one
    def run_command(self, command):
        """ Run a command and return a string with the output.

        :param command: The command you want to return.
        :returns: the output of the command.
        :rtype: string.
        """
        return Popen(command, stdout=PIPE).communicate()[0].decode("utf-8")\
                                                           .strip("\n")
