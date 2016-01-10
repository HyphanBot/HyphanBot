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

import main

"""
This module contains the HyphanAPI class which intends to provide api 
for Hyphan's mods.
"""

class HyphanAPI:
	"""
	This class provides API for making Hyphan mods communicate better 
	with the internal core of Hyphan and the Telegram bot module.

	Args:
		updater (telegram.Updater): The updater object that could be 
			used in mods.
	"""
	def __init__(self, updater):
		self.updater = updater
		self.main    = main

	''' fucking broken piece of shit...
	def restart_bot(self):
		self.updater.stop()
		time.sleep(1)
		main.start_bot()
	'''

	def get_admins(self):
		# TODO: Get this from config.
		return ["NerdyBuzz", "Faalentijn"]
		
	def get_updater(self):
		return self.updater