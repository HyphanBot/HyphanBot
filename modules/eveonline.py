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

def getalliances(bot, update):
    result = eveApi.eve.AllianceList()
    alliancelist = ""

    for alliance in result.alliances:
        if alliance.memberCount >= 2000:
            alliancelist = alliancelist + '\n' + "%s <%s> has %d members" %\
                           (alliance.name, alliance.shortName, alliance.memberCount)

    bot.sendMessage(chat_id=update.message.chat_id, text="{}".format(alliancelist))

def characters(bot, update):
    characters = eveMod.get_config("characters").split()
    character_dict = {}
    
    for character in characters:
        character_config = eveMod.get_config("character." + character)
        character_dict[character] = character_config

    return character_dict

def balance(bot, update, args):
    character_dict = characters(bot, update)

    if len(args) == 0:
        bot.sendMessage(chat_id=update.message.chat_id, text="Please specify a character of whom you want to check the balance of.")
    elif ''.join(args).lower() == "all":
        characterslist = eveMod.get_config("characters").split()

        for character in characterslist:
            balance(bot, update, character)
    else:
        character     = ''.join(args)
        characterinfo = character_dict[character].split()
        api_id        = characterinfo[:1]
        api_vcode     = characterinfo[1:2]

        auth   = eveApi.auth(keyID=api_id, vCode=api_vcode)
        result = auth.account.Characters()
    
        for character in result.characters:
            wallet = auth.char.AccountBalance(characterID=character.characterID)
            isk = wallet.accounts[0].balance
            bot.sendMessage(chat_id=update.message.chat_id, text="{0} has {1} ISK".format(character.name, '{0:,}'.format(isk)))
        
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
        dp.addTelegramCommandHandler("evealliance", getalliances)
        dp.addTelegramCommandHandler("evechar", characters)
        dp.addTelegramCommandHandler("evewallet", balance)
        
