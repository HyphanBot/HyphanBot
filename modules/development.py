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

# Development commands
def dispatch(api, updater):
        dp = updater.dispatcher

        def devChannel(bot, update, args):
                if api.api.is_sender_admin(update):
                        msg = " ".join(args)
                        channel = api.get_config("channel")
                        bot.sendMessage(chat_id=channel, text=msg, parse_mode=ParseMode.MARKDOWN)
                else:
                        bot.sendMessage(chat_id=update.message.chat_id, text="*You're not admin.*", parse_mode=ParseMode.MARKDOWN)

        dp.addTelegramCommandHandler("devpost", devChannel)
        api.set_help('devpost', 'Send a message to the development channel.\n/devpost [message]')
