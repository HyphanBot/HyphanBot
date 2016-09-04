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
-----
This mod provides the basic commands that display possible information about the bot.
'''

from telegram import ParseMode
from telegram.ext import CommandHandler, Filters


class Commands(object):
    """Define the program logic for the module"""
    def __init__(self, api):
        self.api = api

    def help_cmd(self, bot, update, args):
        """Return the a help message for the command in ARGS"""
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=self.api.get_help(args),
                        parse_mode=ParseMode.MARKDOWN)

    def about(self, bot, update):
        """Return an about me message"""
        # TODO: Get text and other settings from config
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="I am King %s, ruler of the northern part of the galaxy."
                        % bot.getMe().first_name)

    def anti_nick(self, bot, update):
        """Fix a common mistake Nick makes.."""
        msg = update.message.text.lower()

        if msg[len(msg) - 2:] == ".." and msg[len(msg) - 3:] != "...":
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="Three dots, Nick.")

    def noslash(self, bot, update):
        """Run a commands based on a string or word instead of a command"""
        msg = update.message.text
        if msg == "help":
            self.help_cmd(bot, update, args)
        elif msg == "about":
            self.about(bot, update)

    def handle_msgs(self, bot, update):
        """Handles messages"""
        self.noslash(bot, update)
        self.anti_nick(bot, update)


class Dispatch(object):
    """Bind the commands"""
    def __init__(self, api, updater):
        self.api = api
        self.updater = updater
        self.define_commands()
        self.define_help()

    def define_commands(self):
        """Bind the commands"""
        dispr = self.updater.dispatcher
        cods = Commands(self.api)

        dispr.add_handler(CommandHandler("help", cods.help_cmd, pass_args=True))
        dispr.add_handler(CommandHandler("about", cods.about))
        self.api.add_message_handler([Filters.text], cods.handle_msgs)

    def define_help(self):
        """Define the help messages"""
        self.api.set_help("help", "Gets help for a specified command:\n/help"
                          " [command name]")
        self.api.set_help("about", "A message of our great leader:\n/about")
