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

from constants import HYPHAN_DIR
from modloader import *

import logging

global logger
logger = logging.getLogger(__name__)

def loadModules(api, updater):
        # Get, load, and dispatch all mods found in the modules folder
        for i in getMods(logger):
                # Check if mod is enabled in config. If so, call its dispatch(). It's enabled by default.
                modenabled = bool(api.config.config.getboolean(i['name'], "enabled", fallback="true"))
                if modenabled:
                        logger.info("Mod %s has been loaded." % i['name'])
                        # This does some weird shinanagins.
                        mod = loadMod(i) # Load the mod
                        if "dispatch" in dir(mod): # Check if the dispatch function exists in the mod
                                modapi = api.Mod(api, mod.__name__)
                                os.chdir(i['location'])
                                mod.dispatch(modapi, updater)
                                os.chdir(HYPHAN_DIR+"/core")
                        else:
                                logger.warn("Cannot dispatch mod '%s': dispatch() is missing." % mod.__name__)

                else:
                        logger.warn("Mod %s is disabled." % i['name'])
