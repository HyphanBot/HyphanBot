from modloader import *

import logging

global g_api
global g_updater
global g_modlist

global logger
logger = logging.getLogger(__name__)

def loadLoop(mlist, api, updater):
	for i in mlist:
		mod = loadMod(i) # Load the mod
		if "dispatch" in dir(mod): # Check if the dispatch function exists in the mod
			modapi = api.Mod(api, mod.__name__)
			mod.dispatch(modapi, updater)
		else:
			logger.warn("Cannot dispatch mod '%s': dispatch() is missing." % mod.__name__)

def loadModules(api, updater):
	global g_api
	global g_updater
	global g_modlist

	g_updater = updater
	g_api = api

	# Get, load, and dispatch all mods found in the modules folder
	g_modlist = getMods(logger)
	loadLoop(g_modlist, g_api, g_updater)

	dp = updater.dispatcher
	dp.addTelegramCommandHandler("reloadmods", reloadModules)
	dp.addTelegramCommandHandler("remod", reloadModules)

# Command for reloading the Mods
def reloadModules(bot, update):
	global g_modlist
	if g_api.is_sender_admin(update):
		new_modlist = getMods(logger)
		loadLoop(new_modlist, g_api, g_updater)
		g_modlist = new_modlist
		bot.sendMessage(chat_id=update.message.chat_id, text="Finished reloading mods.")
