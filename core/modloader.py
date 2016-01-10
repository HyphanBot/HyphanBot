from importlib.machinery import *
import os

# Gets and loads mods from the modules directory.

def getMods(logger):
	modDir     = "../modules"
	mainModule = "main"

	mods = []
	possibleMods = os.listdir(modDir) # List the contents of the mod directory
	for mod in possibleMods: # iterate through the list
		mainModule = "main" # Reset the variable to "main" for every loop
		modName = mod
		location = os.path.join(modDir, mod)

		# Check if the mod is not in its own directory and include it.
		if not os.path.isdir(location):
			if location.endswith(".py"):
				location = modDir
				modName = mod.split(".")[0]
				mainModule = modName
		elif not mainModule+".py" in os.listdir(location): # If main.py is not found in the mod directory...
			logger.warn("Not loading mod '%s': Entry point '%s.py' not found." % (mod, mainModule))
			continue
		mods.append({ "name": modName, "path": location+"/"+mainModule+".py" })
		logger.info("Found mod '%s'." % modName)
	return mods

def loadMod(mod):
	# load the mod. This basically imports it.
	return SourceFileLoader(mod["name"], mod["path"]).load_module()