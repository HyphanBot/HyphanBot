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
