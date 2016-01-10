from telegram import Updater, Update, Bot
from dispatcher import *
from api import *
import logging

# Log everything
logging.basicConfig(
	format='%(asctime)s - %(name)s [%(levelname)s]: %(message)s',
	level=logging.INFO)
logger = logging.getLogger(__name__)

def error(bot, update, error):
	logger.warn('Error occured in update, "%s": %s' % (update, error))

def start_bot():
	# TODO: Find a way to read a config file

	# TODO: Make sure these are configurable in the config file
	token 			= "136008664:AAE2zBk8l1A4OZPQ5ebYxH1h_pVDMCtvUFo"
	#botname 		= "Hyphanbot"
	#friendlyBotName = "Hyphan"

	updater = Updater(token)
	getBot  = updater.bot.getMe()

	api = HyphanAPI(updater)

	# Dispatch modules
	dp = updater.dispatcher
	loadModules(api, updater, logger)
	dp.addErrorHandler(error)

	# Start the bot
	updater.start_polling()
	logger.info("Initialized %s (%s)." % (getBot.first_name, getBot.username))
	updater.idle()

def main():
	start_bot()

if __name__ == '__main__':
	main()