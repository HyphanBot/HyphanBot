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

----------------------

This Hyphan mod adds captions to provided images and sends them to chat as a
photo or file.
This will support the inline bot feature.

'''

import logging
import uuid

from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler

class ImageCaptions(object):
    """
    Embeds captions to images.

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
                title="Coming soon!",
                input_message_content=InputTextMessageContent("ImageCaptions are coming soon!")
            )
        ]
        self.inline_engine.show_results(update.inline_query.id, results)


class Dispatch(object):
    """
    Dispatchs commands and queries to Telegram.

    Args:
        mod (core.api.HyphanAPI.Mod): The Mod object used to access HyphanBot's
            API methods.
        updater (telegram.ext.Updater): The Updater object used to dispatch the
            commands and other handlers.
    """
    def __init__(self, api, updater):
        updater = updater
        inline_engine = api.inline_engine

        img_cap = ImageCaptions(inline_engine)

        disp = updater.dispatcher
        # TODO: Add traditional command processing
        # TODO: Add custom image commands
        # TODO: Add online image search abilities

        api.add_inline_query("ImageCaptions", img_cap.inline_handle)
