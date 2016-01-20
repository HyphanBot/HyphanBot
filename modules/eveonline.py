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
import eveapi

global eveMod
global eveApi

eveapi.set_user_agent("eveapi.py/1.3")

eveApi = eveapi.EVEAPIConnection()
# the following is a plugin which keeps tracks and reports when a EVE
# online character finishes training

def getalliances(bot, update, args):
    result = eveApi.eve.AllianceList()
    alliancelist = ""

    for alliance in result.alliances:
        if alliance.memberCount >= 2000:
            alliancelist = alliancelist + '\n' + "%s <%s> has %d members" %\
                           (alliance.name, alliance.shortName, alliance.memberCount)

    bot.sendMessage(chat_id=update.message.chat_id, text="{}".format(alliancelist))

def dispatch(mod, updater):
    global eveMod
    eveMod = mod

    if not eveMod.get_config():
        default_keys = {
            "enabled":   "yes",
            "character": "foo bar"
        }

        eveMod.set_config(default_keys)

    if eveMod.get_config("enabled") == "yes":
        dp = updater.dispatcher
        dp.addTelegramCommandHandler("eve", getalliances)
        
