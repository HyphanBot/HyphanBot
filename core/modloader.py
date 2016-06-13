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

from importlib.machinery import SourceFileLoader
from os.path import expanduser
from constants import HYPHAN_DIR

import os
import sys
import pathlib

from pprint import pprint

def get_mods(logger):
    """
    Gets and loads mods from the modules directory.
    """
    home = expanduser("~")
    main_module = "main"
    mods = []
    paths = [
        HYPHAN_DIR + "/modules",
        HYPHAN_DIR + "/opt",
        home + "/.hyphan/mods",
        home + "/.config/hyphan/mods"]

    for path in paths:
        if not pathlib.Path(path).exists():
            continue

        possible_mods = os.listdir(path)

        for mod in possible_mods: # iterate through the list
            if mod == "__pycache__" or mod[-1] == "~": # ignore backup files
                continue

            main_module = "main" # Reset the variable to "main" for every loop
            mod_name = mod
            location = os.path.join(path, mod)

            # Check if the mod is not in its own directory and include it.
            if not os.path.isdir(location):
                if "." in location:
                    if location.endswith(".py"):
                        location = path
                        mod_name = mod.split(".")[0]
                        main_module = mod_name
                    else:
                        continue

            elif not main_module + ".py" in os.listdir(location):
                logger.warning("Not loading mod '%s': '%s.py' not found." % (mod, main_module))

            if not any(m["name"] == mod_name for m in mods):
                mods.append(
                    {"name": mod_name,
                     "location": location,
                     "path": location + "/" + main_module + ".py",
                     "main": main_module})

    return mods

def load_mod(mod):
    """ Loads the mod, basically importing it. """
    return SourceFileLoader(mod["name"], mod["path"]).load_module()
