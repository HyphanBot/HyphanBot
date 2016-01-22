from modloader import *

import logging

global logger
logger = logging.getLogger(__name__)

def loadModules(api, updater):
	# Get, load, and dispatch all mods found in the modules folder
	for i in getMods(logger):
		# Check if mod is enabled in config. If so, call its dispatch(). It's enabled by default.
		modenabled = api.config.config.getboolean(i['name'], "enabled", fallback="true")
		if modenabled:
			# This does some weird shinanagins.
			mod = loadMod(i) # Load the mod
			if "dispatch" in dir(mod): # Check if the dispatch function exists in the mod
				modapi = api.Mod(api, mod.__name__)
				mod.dispatch(modapi, updater)
			else:
				logger.warn("Cannot dispatch mod '%s': dispatch() is missing." % mod.__name__)

	''' Useless...
	dp = updater.dispatcher
	dp.addTelegramCommandHandler("reloadmods", reloadModules)
	dp.addTelegramCommandHandler("remod", reloadModules)
	'''

''' Stupid useless shit that doesn't work...
# Command for reloading the Mods
def reloadModules(bot, update):
	global g_modlist
	if g_api.is_sender_admin(update):
		new_modlist = getMods(logger)
		loadLoop(new_modlist, g_api, g_updater, True)
		g_modlist = new_modlist
		bot.sendMessage(chat_id=update.message.chat_id, text="Finished reloading mods.")
'''