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
"""This module is used to manage the configuration file for Hyphan."""

from configparser import ConfigParser
from os import environ
from os.path import expanduser, join
from core.constants import HYPHAN_DIR

import pathlib
import sys
import logging

HOME = expanduser("~")
# Follow the XDG_BASE_DIR specification.
CONFIG_DIR = join(HOME, environ.get("XDG_CONFIG_HOME", join(HOME, ".config")))

CONFIG_PATHS = [
    # Checks in the XDG config place.
    CONFIG_DIR + "/hyphan/config.ini",
    CONFIG_DIR + "/hyphan/config",
    CONFIG_DIR + "/hyphanrc",

    # Check in the home directory
    HOME + ".hyphan/config.ini",
    HOME + ".hyphan/config",
    HOME + ".hyphanrc",

    # Revert back to the default configuration file.
    HYPHAN_DIR + "/config.ini"
]

class Configurator:
    """
    Manages the initialization and maintains HyphanBot's configuration file.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = self._init_config()

    def _init_config(self):
        """
        Attempts to find the configuration file at the pre-specified paths. If
        the file is not found, the method will start an interactive prompt to
        set up the base configuration file.
        """
        logger = self.logger
        config = ConfigParser()

        # Look in the CONFIG_PATHS for the config file
        for cfile in CONFIG_PATHS:
            if pathlib.Path(cfile).exists():
                logger.info("Configuration file has been found at: " + cfile)
                config.read(cfile)
                return config

        logger.error("No configuration file found.")
        sys.exit(2)  # File or folder not found

    def refresh_config(self):
        """
        Reloads the configuration file
        """
        self.config = self._init_config()

    def parse_general(self):
        """
        Parses the 'general' section of the configuration file
        """
        config = self.config
        return {
            "adminlist": config.get("general", "admins").split(" "),
            "adminstr": config.get("general", "admins"),
            "token": config.get("general", "token")
        }

    def access(self, section, key):
        """
        Mid-level access to config.
        Returns the specified key's value.

        Args:
        section (String): The config section the key is found at.
        key (String): The key to access.
        fallback [Optional] (String): The default value if the
        key-value pairs is unspecified.
        """
        return self.config.get(section, key)

    def append(self, section, data):
        """
        Low-level append to config. Appends the key-value data to a section in
        the config file.

        Args:
            section (String): The section to append to.
            data (Dictionary): The key-value data to append to the section.
        """
        if not section == "general":
            self.config[section] = data
            with open(self.config, 'w') as writefile:
                self.config.write(writefile)
        else:
            return False

    def get_sections(self):
        """
        Returns the sections found in the config file.
        """
        return self.config.sections()
