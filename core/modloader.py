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

from importlib.machinery import *
from os.path import expanduser
from constants import HYPHAN_DIR
import importlib
import sys
import os
import pathlib

# Gets and loads mods from the modules directory.
def getMods(logger):
    home       = expanduser("~")
    mainModule = "main"
    mods       = []
    paths      = [
         HYPHAN_DIR + "/modules",
         HYPHAN_DIR + "/opt",
         home + "/.hyphan/mods",
         home + "/.config/hyphan/mods"]

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
                if "." in location:
                    if location.endswith(".py"):
                        location = path
                        modName = mod.split(".")[0]
                        mainModule = modName
                    else:
                        continue

            elif not mainModule + ".py" in os.listdir(location):
                logger.warn("Not loading mod '%s': Entry point '%s.py' not found." % (mod, mainModule))

            mods.append({ "name": modName, "location": location, "path": location + "/" + mainModule + ".py", "main": mainModule })
            logger.info("Found mod '%s'." % modName)

    return mods

def loadMod(mod):
    # load the mod. This basically imports it.
    return SourceFileLoader(mod["name"], mod["path"]).load_module()
