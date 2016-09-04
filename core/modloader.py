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

from importlib.machinery import SourceFileLoader


def get_set(section, api):
    mods = []

    try:
        path = api.get_value("path", section)

        for mod in api.get_value("mods", section).split():
            mod_name = mod
#            location = os.path.join(path, mod)

            if not any(m["name"] == mod_name for m in mods):
                mods.append(
                    {"name": mod_name,
                     "location": path,
                     "path": path + "/" + mod_name + ".py",
                     "main": mod_name})
    except:
        pass
    finally:
        return mods


def get_mods(logger, api):
    """
    Gets and loads mods from the modules directory.
    """
    sections = ["modules", "opt"]
    mods = []

    for section in sections:
        mods += get_set(section, api)

    return mods
    # home = expanduser("~")
    # main_module = "main"
    # mods = []
    # paths = [
    #     hyphan_dir + "/modules",
    #     hyphan_dir + "/opt",
    #     home + "/.hyphan/mods",
    #     home + "/.config/hyphan/mods"
    # ]

    # for path in paths:
    #     if not pathlib.Path(path).exists():
    #         continue

    #     possible_mods = os.listdir(path)

    #     for mod in possible_mods:  # iterate through the list
    #         # ignore backup files
    #         if mod == "__pycache__" or mod[-1] == "~" or mod == "__init__":
    #             continue

    #         main_module = "main"  # Reset the variable to "main" for every loop
    #         mod_name = mod
    #         location = os.path.join(path, mod)

    #         # Check if the mod is not in its own directory and include it.
    #         if not os.path.isdir(location):
    #             if "." in location:
    #                 if location.endswith(".py"):
    #                     location = path
    #                     mod_name = mod.split(".")[0]
    #                     main_module = mod_name
    #                 else:
    #                     continue

    #         elif not main_module + ".py" in os.listdir(location):
    #             logger.warning("Not loading mod '%s': '%s.py' not found." % (mod, main_module))

    #         if not any(m["name"] == mod_name for m in mods):
    #             mods.append(
    #                 {"name": mod_name,
    #                  "location": location,
    #                  "path": location + "/" + main_module + ".py",
    #                  "main": main_module})

    # return mods


def load_mod(mod):
    """ Loads the mod, basically importing it. """
    return SourceFileLoader(mod["name"], mod["path"]).load_module()
