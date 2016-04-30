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
import traceback

def load_modules(api, updater):
    """
    Loads and runs HyphanBot's mods.
    """
    logger = logging.getLogger(__name__)
    # Get, load, and dispatch all mods found in the modules folder
    for i in get_mods(logger):
        # Check if mod is enabled in config. If so, call its dispatch().
        # It's enabled by default.
        modenabled = bool(api.config.config.getboolean(i['name'], "enabled", fallback="true"))
        if modenabled:
            # This does some weird shenanigans.
            try:
                mod = load_mod(i) # Load the mod
                logger.info("Mod %s has been loaded." % i['name'])
            except:
                logger.error("Cannot load mod %s." % i['name'])
                print(traceback.format_exc())

            if "dispatch" in dir(mod): # Check if the dispatch function exists in the mod
                modapi = api.Mod(api, mod.__name__)
                os.chdir(i['location'])
                mod.dispatch(modapi, updater)
                os.chdir(HYPHAN_DIR + "/core")
            elif "Dispatch" in dir(mod):
                modapi = api.Mod(api, mod.__name__)
                os.chdir(i['location'])
                mod.Dispatch(modapi, updater)
                os.chdir(HYPHAN_DIR + "/core")
            else:
                logger.warning("Cannot dispatch mod '%s': dispatch() is missing." % mod.__name__)

        else:
            logger.warning("Mod %s is disabled." % i['name'])
