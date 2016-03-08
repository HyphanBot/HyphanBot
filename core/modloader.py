from importlib.machinery import *
from os.path import expanduser
import importlib
import sys
import os
import pathlib

# Gets and loads mods from the modules directory.
def getMods(logger):
        home       = expanduser("~")
        mainModule = "main"
        mods       = []
        paths      = ["../modules", home + "/.hyphan/mods", home + "/.config/hyphan/mods"]

        for path in paths:
                if not pathlib.Path(path).exists():
                        continue
                possibleMods = os.listdir(path)

                for mod in possibleMods: # iterate through the list
                        if mod == "__pycache__" or mod[-1] == "~": # ignore backup files
                                continue

                        mainModule = "main" # Reset the variable to "main" for every loop
                        modName = mod
                        location = os.path.join(path, mod)

                        # Check if the mod is not in its own directory and include it.
                        if not os.path.isdir(location):
                                if location.endswith(".py"):
                                        location = path
                                        modName = mod.split(".")[0]
                                        mainModule = modName
                                elif not mainModule+".py" in os.listdir(location): # If main.py is not found in the mod directory...
                                        logger.warn("Not loading mod '%s': Entry point '%s.py' not found." % (mod, mainModule))
                                        continue
                                mods.append({ "name": modName, "location": location, "path": location+"/"+mainModule+".py", "main": mainModule })
                                logger.info("Found mod '%s'." % modName)
        return mods

def loadMod(mod):
        # load the mod. This basically imports it.
        return SourceFileLoader(mod["name"], mod["path"]).load_module()
