# This file is part of Hyphan.
# Hyphan is free software: you can redistribute it and/or modify
# it under the terms of the GNU Afferno General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hyphan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Afferno General Public License for more details.
#
# You should have received a copy of the GNU Afferno General Public
# License along with Hyphan.  If not, see
# https://www.gnu.org/licenses/agpl-3.0.html>.

from core.modloader import get_mods, load_mod
import logging
import traceback


def load_modules(api, updater, tracestack=False):
    """ Loads and runs HyphanBot's mods. 

    :param api: The Hyphan api.
    :param updater: The information from the last message.
    :param tracestack: Debugging information
    """
    logger = logging.getLogger(__name__)
    # Get, load, and dispatch all mods found in the modules folder
    mod_id = 0
    for i in get_mods(logger, api):
        # Check if mod is enabled in config. If so, call its dispatch().
        # It's enabled by default.
        # This does some weird shenanigans.
        try:
            api.mod_id = mod_id
            api.name = __name__
            value = api.in_config(value="yes", key="enabled",
                                  section=i['name'])

            mod = load_mod(i)
            logger.info("Mod {mod} has been loaded.".format(mod=i['name']))

            function = (mod.Dispatch if "Dispatch" in dir(mod) else
                        mod.dispatch)
            function(api, updater) if value else None
        except KeyError:
            logger.warning("Mod {mod} is disabled.".format(mod=i['name']))
        except TypeError:
            logger.error("Can't find the value for %s in the config."
                         % i['name'])
        except ImportError as e:
            logger.error("ImportError in mod '%s': %s" % (i['name'], str(e)))
        except Exception as e:
            logger.error("Error in mod '%s': %s" % (i['name'], str(e)))
        except AttributeError:
            logger.error("Error in mod '%s': dispatch not found" % str(e))
        except:
            logger.error("Cannot load mod %s." % i['name'])
        finally:
            if tracestack:
                print(traceback.format_exc())
