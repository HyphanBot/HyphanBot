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

import logging
import uuid

from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler

class SecretMsgs(object):
    """
    Encodes/Decodes messages by decrementng/incrementing the ASCII code of each
    character in the message respectively.

    Args:
        inline_engine (core.inline_engine.InlineEngine): The InlineEngine object
            used to process Inline Bot queries.
    """
    def __init__(self, inline_engine):
        self.inline_engine = inline_engine

    def inline_handle(self, bot, update):
        query = update.inline_query.query
        results = [
            InlineQueryResultArticle(
                id=uuid.uuid4(),
                title="Encode message",
                description=self.encode_msg(query) or "Nothing to encode.",
                input_message_content=InputTextMessageContent(self.encode_msg(query) or "Nothing to encode.")
            ),
            InlineQueryResultArticle(
                id=uuid.uuid4(),
                title="Decode message",
                description=self.decode_msg(query) or "Nothing to decode.",
                input_message_content=InputTextMessageContent(self.decode_msg(query) or "Nothing to decode.")
            )
        ]
        self.inline_engine.show_results(update.inline_query.id, results)

    def encode_msg(self, msg):
        newstr = ""
        for code in msg.encode('ascii'):
            newstr += chr(code-1)
        return newstr

    def decode_msg(self, msg):
        newstr = ""
        for code in msg.encode('ascii'):
            newstr += chr(code+1)
        return newstr

class Dispatch(object):
    """
    Dispatchs commands and queries to Telegram.

    Args:
        mod (core.api.HyphanAPI.Mod): The Mod object used to access HyphanBot's
            API methods.
        updater (telegram.ext.Updater): The Updater object used to dispatch the
            commands and other handlers.
    """
    def __init__(self, mod, updater):
        self.mod = mod
        self.updater = updater
        self.inline_engine = self.mod.api.inline_engine

        smsgs = SecretMsgs(self.inline_engine)

        disp = self.updater.dispatcher
        # TODO: Add traditional command processing

        mod.add_inline_query("Secret Messages", smsgs.inline_handle)
