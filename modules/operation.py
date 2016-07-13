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
    def __init__(self, hyphan_api):
        """Define the program logic

        :param hyphan_api: Hyphan's api
        """
        self.hyphan_api = hyphan_api

    def _sender_is_admin(self, update):
        try:
            return self.hyphan_api.in_config(update.message.from_user['username'],
                                             "admins", "general")
        except TypeError:
            raise
        except KeyError:
            return False

    def quit(self, bot, update):
        """Quit hyphan"""
        # Use the API to check if sender is admin
        self.logger.info("Called /quit")

        if self._sender_is_admin(update):
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="Affermative, %s. I read you."
                            % update.message.from_user.first_name)
            os.kill(os.getpid(), signal.SIGTERM)
        else:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="I'm sorry, %s, I'm afraid I can't do that."
                            % update.message.from_user.first_name)

    def restart(self, bot, update):
        """Restart the bot if it's run using run.sh (most of the logic is a simple bash if)"""
        # This will only restart the bot if it was running from the launcher script
        if self._sender_is_admin(update):  # Use the API to check if sender is admin
            bot.sendMessage(chat_id=update.message.chat_id, text="See ya!")
            os.kill(os.getpid(), signal.SIGKILL)
        else:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="Sorry, %s, I'm afraid I can't let you do that."
                            % update.message.from_user.first_name)

    def reload_config(self, bot, update):
        """Reload the configuration file."""
        if self._sender_is_admin(update):
            self.hyphanrefresh_config()
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
    def __init__(self, hyphan_api, updater):
        self.hyphan_api = hyphan_api
        self.updater = updater
        self.define_commands()

    def define_commands(self):
        """Bind the commands"""
        dispr = self.updater.dispatcher
        cods = Commands(self.hyphan_api)

        dispr.add_handler(CommandHandler("quit", cods.quit))
        dispr.add_handler(CommandHandler("restart", cods.restart))
        dispr.add_handler(CommandHandler("reloadconf", cods.reload_config))
        dispr.add_handler(CommandHandler("reconf", cods.reload_config))
        self.hyphan_api.add_message_handler([Filters.text], cods.noslash)
