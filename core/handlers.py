# This file is part of Hyphan.
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

from telegram import Update
from telegram.ext import Handler, InlineQueryHandler

"""
All of Telegram message/command handlers for HyphanBot go here
"""

class StartHandler(Handler):
    """
    Handler class to handle Telegram ``/start`` command parameters.

    Args:
        arg (str): The ``/start`` parameter this handler should listen for.
        callback (function): A function that takes ``bot, update`` as
            positional arguments. It will be called when the ``check_update``
            has determined that an update should be processed by this handler.
        pass_update_queue (optional[bool]): If the handler should be passed the
            update queue as a keyword argument called ``update_queue``. It can
            be used to insert updates. Default is ``False``
    """
    def __init__(self, arg, callback, pass_update_queue=False):
        super(StartHandler, self).__init__(callback, pass_update_queue)
        self.arg = arg

    def check_update(self, update):
        """ Checks if there has been an update

        :param update: The information to the latest Telegram message
        :returns: The message text or False
        :rtype: String or Boolean

        """
        if isinstance(update, Update) and update.message:
            msg = update.message
            return (msg.text and msg.text.startswith('/start')
                    and msg.text.split(' ')[1] == self.arg)
        else:
            return False

    def handle_update(self, update, dispatcher):
        optional_args = self.collect_optional_args(dispatcher)
        optional_args['args'] = update.message.text.split(' ')[2:]
        self.callback(dispatcher.bot, update, **optional_args)
