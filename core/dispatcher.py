from modloader import *

import logging

def loadModules(api, updater):
	logger = logging.getLogger(__name__)

	# Get, load, and dispatch all mods found in the modules folder
	for i in getMods(logger):
		mod = loadMod(i) # Load the mod
		if "dispatch" in dir(mod): # Check if the dispatch function exists in the mod
			modapi = api.Mod(api, mod.__name__)
			mod.dispatch(modapi, updater)
		else:
			logger.warn("Cannot dispatch mod '%s': dispatch() is missing." % mod.__name__)