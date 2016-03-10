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
import os, signal, sys

class Commands(object):
    def quit(self, bot, update):
        if api.api.is_sender_admin(update): # Use the API to check if sender is admin
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="Goodbye!")
            os.kill(os.getpid(), signal.SIGTERM)
        else:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="Sorry, %s, I'm afraid I can't let you do that."
                            % update.message.from_user.first_name)

    def restart(self, bot, update):
        # This will only restart the bot if it was running from the launcher script
        if api.api.is_sender_admin(update): # Use the API to check if sender is admin
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="See ya!")
            print(__file__)
            os.kill(os.getpid(), signal.SIGKILL)
        else:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="Sorry, %s, I'm afraid I can't let you do that."
                            % update.message.from_user.first_name)

    def reload_config(self, bot, update):
        if api.api.is_sender_admin(update):
            api.api.config.refresh_config()
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="Configuration file reloaded.")
        else:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="Sorry, %s, I'm afraid I can't let you do that."
                            % update.message.from_user.first_name)

    def noslash(self, bot, update):
        msg = update.message.text
        if msg == "quit":
            quit(bot, update)
        elif msg == "restart":
            restart(bot, update)
        elif msg == "reloadconf" or msg == "reconf":
            reload_config(bot, update)

class Dispatch(object):
    def __init__(self, api, updater):
        self.define_commands(updater)
        self.set_api(api)

    def set_api(self, temp):
        global api
        api = temp

    def define_commands(self, updater):
        dp = updater.dispatcher
        c = Commands()

        dp.addTelegramCommandHandler("quit", c.quit)
        dp.addTelegramCommandHandler("restart", c.restart)
        dp.addTelegramCommandHandler("reloadconf", c.reload_config)
        dp.addTelegramCommandHandler("reconf", c.reload_config)
        dp.addTelegramMessageHandler(c.noslash)
