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
This mod operates the bot. It can quit or restart Hyphan.
'''
import os
import signal

from telegram.ext import CommandHandler, Filters

class Commands(object):
    """Define the program logic"""
    def quit(self, bot, update):
        """Quit hyphan"""
        if API.api.is_sender_admin(update): # Use the API to check if sender is admin
            bot.sendMessage(chat_id=update.message.chat_id, text="Goodbye!")
            os.kill(os.getpid(), signal.SIGTERM)
        else:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="Sorry, %s, I'm afraid I can't let you do that."
                            % update.message.from_user.first_name)

    def restart(self, bot, update):
        """Restart the bot if it's run using run.sh (most of the logic is a simple bash if)"""
        # This will only restart the bot if it was running from the launcher script
        if API.api.is_sender_admin(update): # Use the API to check if sender is admin
            bot.sendMessage(chat_id=update.message.chat_id, text="See ya!")
            os.kill(os.getpid(), signal.SIGKILL)
        else:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="Sorry, %s, I'm afraid I can't let you do that."
                            % update.message.from_user.first_name)

    def reload_config(self, bot, update):
        """Reload the configuration file."""
        if API.api.is_sender_admin(update):
            API.api.config.refresh_config()
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="Configuration file reloaded.")
        else:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="Sorry, %s, I'm afraid I can't let you do that."
                            % update.message.from_user.first_name)

    def noslash(self, bot, update):
        """Use strings or words instead of commands"""
        msg = update.message.text
        if msg == "quit":
            self.quit(bot, update)
        elif msg == "restart":
            self.restart(bot, update)
        elif msg == "reloadconf" or msg == "reconf":
            self.reload_config(bot, update)

class Dispatch(object):
    """Define the commands"""
    def __init__(self, api, updater):
        self.api = api
        self.updater = updater
        self.define_commands()
        self.set_api()

    def set_api(self):
        """Set the global variable API for use inside of the program logic as well."""
        global API
        API = self.api

    def define_commands(self):
        """Bind the commands"""
        dispr = self.updater.dispatcher
        cods = Commands()

        dispr.add_handler(CommandHandler("quit", cods.quit))
        dispr.add_handler(CommandHandler("restart", cods.restart))
        dispr.add_handler(CommandHandler("reloadconf", cods.reload_config))
        dispr.add_handler(CommandHandler("reconf", cods.reload_config))
        self.api.add_message_handler([Filters.text], cods.noslash)
