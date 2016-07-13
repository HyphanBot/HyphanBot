# This file is part of Hyphan.
# 
# Hyphan is free software: you can redistribute it and/or modify
# it under the terms of the GNU Afferno General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Hyphan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Afferno General Public License for more details.
# 
# You should have received a copy of the GNU Afferno General Public
# License along with Hyphan.  If not, see
# https://www.gnu.org/licenses/agpl-3.0.html>.
import logging
import uuid

import core.handlers

from telegram.ext import InlineQueryHandler, CallbackQueryHandler
from telegram import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ParseMode,
    Emoji
)

"""
Processes inline queries from various mods.
"""

INLINE_SETTINGS_INTRO = """
*Inline Bot Settings*
From here, you can change {0}'s Inline Bot behavior.
{0} was set up with a number of Inline Bot features that can be activated from the feature list.
The current activated Inline Bot feature is "{1}".
"""

INLINE_SETTINGS_LIST = """
*Inline Feature List*
The current activated Inline Bot feature is "{}".
To change it, select another feature from the button list below.
"""

INLINE_FEATURE_ACTIVATED = """
Activated feature: {}
"""

class InlineEngine(object):
    """
    The InlineEngine handles all of HyphanBot's inline bot features. It manages,
    adds, and activates inline mods for use with Hyphan. This class also
    includes Hyphan's default inline bot feature which turns the user's query
    text bold and in all caps.

    Args:
        updater (telegram.ext.Updater): The Updater object used to communicate
            with Telegram's Bot API.
    """
    def __init__(self, updater):
        self.updater = updater
        self.last_handler = None
        self.inline_features = list()
        self.active_feature = "default"
        self.logger = logging.getLogger(__name__)
        self.return_inline = InlineKeyboardButton("Start using the inline feature!", switch_inline_query="")

        self.add_feature("default", self.default_inline_query, True)
        updater.dispatcher.add_handler(core.handlers.StartHandler("inline", self.engine_settings))
        updater.dispatcher.add_handler(CallbackQueryHandler(self.handle_keyboard_query))

    def default_inline_query(self, bot, update):
        query = update.inline_query.query
        results = [
            InlineQueryResultArticle(
                id=uuid.uuid4(),
                title="BOLD CAPS!" or query.upper(),
                description="*"+(query.upper() or "BOLD CAPS!")+"*",
                input_message_content=InputTextMessageContent("*%s*" % (query.upper() or "BOLD CAPS!"), parse_mode=ParseMode.MARKDOWN)
            )
        ]
        self.show_results(update.inline_query.id, results)

    def show_results(self, qid, res):
        self.updater.bot.answerInlineQuery(qid, res, cache_time=0, switch_pm_text="Change Settings", switch_pm_parameter="inline")

    def add_feature(self, name, callback, default=False):
        self.inline_features.append({
                "name": name,
                "btn": InlineKeyboardButton(name, callback_data="feature_"+name),
                "call": callback
        })

        if default:
            self.last_handler = InlineQueryHandler(callback)
            self.updater.dispatcher.add_handler(self.last_handler)

    def is_feature(self, name):
        return any(feat["name"] == name for feat in self.inline_features)

    def change_feature(self, feature_name):
        self.updater.dispatcher.remove_handler(self.last_handler)

        self.active_feature = feature_name

        self.last_handler = InlineQueryHandler(
            next((f for f in self.inline_features if f["name"] == feature_name))["call"])
        self.updater.dispatcher.add_handler(self.last_handler)

    def engine_settings(self, bot, update, args, query=None):
        list_features = InlineKeyboardButton("List available inline features", callback_data="list")
        inline_btns = [
            [list_features],
            [self.return_inline]
        ]
        if query is not None:
            bot.editMessageText(text=INLINE_SETTINGS_INTRO.format(bot.getMe().first_name, self.active_feature),
                                reply_markup=InlineKeyboardMarkup(inline_btns),
                                message_id=query.message.message_id,
                                chat_id=query.message.chat_id,
                                parse_mode=ParseMode.MARKDOWN)
        else:
            bot.sendMessage(text=INLINE_SETTINGS_INTRO.format(bot.getMe().first_name, self.active_feature),
                            parse_mode=ParseMode.MARKDOWN,
                            chat_id=update.message.chat_id,
                            reply_markup=InlineKeyboardMarkup(inline_btns))

    def handle_keyboard_query(self, bot, update):
        query = update.callback_query
        chat_id = query.message.chat_id
        user_id = query.from_user.id
        text = query.data
        return_intro = InlineKeyboardButton("Back", callback_data="intro")
        #bot.answerCallbackQuery(query.id, text="Loading...")
        if text == "list":
            inline_btns = list()
            for feature in self.inline_features:
                inline_btns.append([feature['btn']])
            inline_btns += [
                [return_intro],
                [self.return_inline]
            ]
            bot.editMessageText(text=INLINE_SETTINGS_LIST.format(self.active_feature),
                                reply_markup=InlineKeyboardMarkup(inline_btns),
                                message_id=query.message.message_id,
                                parse_mode=ParseMode.MARKDOWN,
                                chat_id=chat_id)
        elif text == "intro":
            self.engine_settings(bot, update, [], query)
        elif text.startswith("feature_"):
            feature_name = text.split("_")[1]

            self.change_feature(feature_name)

            bot.answerCallbackQuery(query.id, text=INLINE_FEATURE_ACTIVATED.format(feature_name))
            self.engine_settings(bot, update, [], query)
