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
from telegram import ParseMode
from telegram.ext import CommandHandler

def devchannel(bot, update, args):
    """Post to the Hyphan development channel"""
    if API.api.is_sender_admin(update):
        channel = API.get_config("channel")
        bot.sendMessage(chat_id=channel, text=" ".join(args), parse_mode=ParseMode.MARKDOWN)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="*You're not admin.*",
                        parse_mode=ParseMode.MARKDOWN)

# Development commands
class Dispatch(object):
    """Defines the metadata for hyphan"""
    def __init__(self, api, updater):
        self.api = api
        self.updater = updater
        self.define_commands()
        self.define_help()
        self.set_api()

    def set_api(self):
        """Set the api for use in the logic"""
        global API
        API = self.api

    def define_commands(self):
        """Bind the commands"""
        dispr = self.updater.dispatcher
        dispr.add_handler(CommandHandler("devpost", devchannel, pass_args=True))

    def define_help(self):
        """Set the help messages"""
        self.api.set_help('devpost', 'Send a message to the development channel.\n/devpost" \
        " [message]')
