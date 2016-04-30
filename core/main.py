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

import telegram

# project specific
import configurator
import dispatcher
import api

import logging
import os
import sys

## Get Hyphan's root directory from the environment variable (exported in run.sh)
#HYPHAN_DIR = os.getenv('HYPHAN_DIR', os.path.dirname(os.getcwd()))

# Log everything
# filter for the stupid shit python-telegram-bot reports
class Filter(logging.Filter):
    def filter(self, record):
        message = record.getMessage()
        if message == "No new updates found.":
            return False
        elif message.endswith("webhook"):
            return False
        else:
            return True

logging.basicConfig(
    format='%(asctime)s - %(name)s [%(levelname)s]: %(message)s',
    level=logging.INFO) # change this to logging.INFO to enable verbose mode

logger      = logging.getLogger(__name__)
mainlog     = logging.getLogger("__main__")
telegramlog = logging.getLogger("telegram.bot")
telegramlog.addFilter(Filter())
mainlog.addFilter(Filter())

def error(bot, update, error):
    logger.warn('Error occured in update, "%s": %s' % (update, error))
    try:
        notify2.Notification("Error occured in update '%s': '%s'" % (update, error))
    except:
        pass # Who cares?

def start_bot():
    # Initialize config
    config = configurator.Configurator()
    generalconfig = config.parse_general()

    updater = telegram.Updater(generalconfig['token'], workers=10)
    getBot  = updater.bot.getMe()

    hyphan_api = api.HyphanAPI(updater, config)

    # Dispatch modules
    dp = updater.dispatcher
    dispatcher.loadModules(hyphan_api, updater)
    dp.addErrorHandler(error)

    # Start the bot
    updater.start_polling()

    # Notify that the bot started
    try:
        import notify2
        notify2.init(getBot.username)
        notify2.Notification("Initialized {}".format(getBot.first_name),
                             "{} has started".format(getBot.username),
                             "notification-message-im").show()
    except ImportError:
        logger.warning("Unable to import 'notify2' module")
    except:
        logger.error("X11 or Dbus isn't running")

    logger.info("Initialized %s (%s)." % (getBot.first_name, getBot.username))

    updater.idle()

if __name__ == '__main__':
    start_bot()
