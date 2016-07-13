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
"""
This file contains the api to access and modify the configuration file.
"""
from configparser import NoOptionError, NoSectionError

class Configuration(object):
    """ This class contains the API to access and modify the configuration file.

    :param config (Configurator) The configuration file.
    """
    def __init__(self, config):
        self.config = config
        
    def _assert(self, boolean, message):
        """ A wrapper around the assert function.

        :param boolean: The outcome of the test you just performed
        :param message: Message you want to return
        :returns: True or False
        :rtype: Boolean
        """
        try:
            assert boolean
        except AssertionError:
            raise TypeError(message)

    def section_exists(self, section):
        """ Checks if a section exists in the configuration file.

        :param section: The section you want to lookup
        :returns: True or False
        :rtype: Boolean
        """
        self._assert(type(section) == str, "Invalid value for key")
        return section in self.api.config.get_sections()

    def get_value(self, key, section):
        """Returns the key value from the config if specified, otherwise
        returns whether the mod's section exists in the config file.

        :param key: The key to look up in the configuration file.
        :param section: The section you want to look in
        :returns: The value associated with the key in value or raises an error.
        :rtype: String
        """
        if self._assert(type(key) == str, "Invalid value for key"):
            return False

        try:
            return self.config.access(section, key)
        except (KeyError, NoOptionError, NoSectionError) as e:
            self.logger.warning("Value not found. {}".format(str(e)))
            raise KeyError("Cannot find the value.")

    def in_config(self, value, key, section):
        """ Looks if a value is inside the configuration file.

        :param value: The value you want to look up
        :param key: The part of the configuration you want to look up.
        :param section: The section of the configuration file you want to search.
        :returns: True or False
        :rtype: Boolean
        """
        for argument in [value, key, section]:
            self._assert(type(argument) == str, "Invalid value for {}."
                         .format(argument))

        try:
            return value in self.get_value(key, section)
        except KeyError:
            raise

    def set_config(self, data):
        """ Sets and returns key data to append to the configuration file.

        :param data: Dictionary that contains the key-value to append to config file.
        :returns: Data
        :rtype: Dictionary

        """
        return self.api.config.append(self.name, data)
