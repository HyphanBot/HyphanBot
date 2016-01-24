from telegram import Update, Bot, Updater
from configurator import *
from dispatcher import *
from api import *

import logging
import notify2
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
        notify2.Notification("Error occured in update '%s': '%s'" % (update, error)) 

def start_bot():
        # Initialize config
        config = Configurator()
        generalconfig = config.parse_general()

        updater = Updater(generalconfig['token'], workers=10)
        getBot  = updater.bot.getMe()

        api = HyphanAPI(updater, config)

        # Dispatch modules
        dp = updater.dispatcher
        loadModules(api, updater)
        dp.addErrorHandler(error)

        # Start the 
        updater.start_polling()

        # Notify that the bot started
        notify2.init(getBot.username)
        notify2.Notification("Initialized {}".format(getBot.first_name),
            "{} has started".format(getBot.username), "notification-message-im").show()
        logger.info("Initialized %s (%s)." % (getBot.first_name, getBot.username))

        updater.idle()

if __name__ == '__main__':
        start_bot()
