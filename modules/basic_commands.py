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

def help_cmd(bot, update, args):
    bot.sendMessage(chat_id=update.message.chat_id, text=api.get_help(args), parse_mode=ParseMode.MARKDOWN)

def about(bot, update):
    # TODO: Get text and other settings from config
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="I am King %s, ruler of the northern part of the galaxy." % bot.getMe().first_name)

def anti_nick(bot, update):
    msg = update.message.text.lower()

    if msg[len(msg) - 2:] == ".." and msg[len(msg) - 3:] != "...":
        bot.sendMessage(chat_id=update.message.chat_id, text="Three dots, Nick.")

def noslash(bot, update):
    msg = update.message.text
    if msg == "help":
        help_cmd(bot, update)
    elif msg == "about":
        about(bot, update)

class dispatch(object):
    def __init__(self, api, updater):
        self.define_commands(updater)
        self.define_help(api)
        self.set_api(api)

    def set_api(self, temp):
        global api
        api = temp

    def define_commands(self, updater):
        dp = updater.dispatcher
        dp.addTelegramCommandHandler("help", help_cmd)
        dp.addTelegramCommandHandler("about", about)
        dp.addTelegramMessageHandler(noslash)
        dp.addTelegramMessageHandler(anti_nick)

    def define_help(self, api):
        api.set_help("help", "Gets help for a specified command:\n/help [command name]")
        api.set_help("about", "A message of our great leader:\n/about")
