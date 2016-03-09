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

def devChannel(bot, update, args):
    if api.api.is_sender_admin(update):
        channel = api.get_config("channel")
        bot.sendMessage(chat_id=channel, text=" ".join(args), parse_mode=ParseMode.MARKDOWN)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="*You're not admin.*",
                        parse_mode=ParseMode.MARKDOWN)

# Development commands
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
        dp.addTelegramCommandHandler("devpost", devChannel)

    def define_help(self, api):
        api.set_help('devpost', 'Send a message to the development channel.\n/devpost [message]')
