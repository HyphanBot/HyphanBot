from modloader import *

def loadModules(api, updater, logger):
	# Get, load, and dispatch all mods found in the modules folder
	for i in getMods(logger):
		mod = loadMod(i) # Load the mod
		if "dispatch" in dir(mod): # Check if the dispatch function exists in the mod
			mod.dispatch(api, updater, logger)
		else:
			logger.warn("Cannot dispatch mod '%s': dispatch() is missing." % mod.__name__)