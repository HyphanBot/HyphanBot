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
# ...
import logging
from telegram.ext import MessageHandler, Filters

class MessageLog(object):
    def msg_h(self, bot, update):
        print("[%s] %s (@%s): %s" % (
            update.message.chat_id,
            update.message.from_user.first_name,
            update.message.from_user.username,
            update.message.text
        ))

def dispatch(mod, updater):
    """
    A test to check and inform that mods can be loaded and dispatched
    """
    logger = logging.getLogger(__name__)
    logger.info("Module loading initialized.")

    msglog = MessageLog()
    mod.add_message_handler([Filters.text], msglog.msg_h)
