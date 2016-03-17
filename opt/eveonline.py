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

class Commands(object):
    global eveAPI
    eveapi.set_user_agent("eveapi.py/1.3")
    eveAPI = eveapi.EVEAPIConnection()
    # the following is a plugin which keeps tracks and reports when a EVE
    # online character finishes training

    def getalliances(self, bot, update):
        result = eveAPI.eve.AllianceList()
        alliancelist = ""

        for alliance in result.alliances:
            if alliance.memberCount >= 2000:
                alliancelist = alliancelist + '\n' + "%s <%s> has %d members" %\
                               (alliance.name, alliance.shortName, alliance.memberCount)

        bot.sendMessage(chat_id=update.message.chat_id, text="{}".format(alliancelist))

    def characters(self, bot, update):
        characters = api.get_config("characters").split()
        character_dict = {}

        for character in characters:
            character_config = api.get_config("character." + character)
            character_dict[character] = character_config

        return character_dict

    def balance(self, bot, update, args):
        character_dict = self.characters(bot, update)

        if len(args) == 0:
            bot.sendMessage(chat_id=update.message.chat_id, text="Please specify a character of whom you want to check the balance of.")
        elif ''.join(args).lower() == "all":
            characterslist = api.get_config("characters").split()

            for character in characterslist:
                self.balance(bot, update, character)
        else:
            character     = ''.join(args)
            characterinfo = character_dict[character].split()
            api_id        = characterinfo[:1]
            api_vcode     = characterinfo[1:2]

            auth   = eveAPI.auth(keyID=api_id, vCode=api_vcode)
            result = auth.account.Characters()

            for character in result.characters:
                wallet = auth.char.AccountBalance(characterID=character.characterID)
                isk = wallet.accounts[0].balance
                bot.sendMessage(chat_id=update.message.chat_id, text="{0} has {1} ISK".format(character.name, '{0:,}'.format(isk)))

class dispatch(object):
    def __init__(self, api, updater):
        self.set_config(api)
        self.set_api(api)
        self.define_commands(updater)
        self.define_help(api)

    def set_api(self, temp):
        global api
        api = temp

    def set_config(self, api):
        if not api.get_config():
            default_keys = {
                "enabled": "yes",
                "character": "foo bar"
            }

            api.set_config(default_keys)

    def define_commands(self, updater):
        dp = updater.dispatcher
        c = Commands()

        dp.addTelegramCommandHandler("evealliance", c.getalliances)
        dp.addTelegramCommandHandler("evechar", c.characters)
        dp.addTelegramCommandHandler("evecharacters", c.characters)
        dp.addTelegramCommandHandler("evewallet", c.balance)

    def define_help(self, api):
        api.set_help("evealliance", "Give a list of the top EVE alliances.```/evealliance```")
        api.set_help("evewallet", "Give the amount of ISK owned by a character.\n`/evewallet [character]`\n`/evewallet all`")

        for command in ["evechar", "evecharacters"]:
            api.set_help(command, "Return a list of the defined EVE characters.```/{}```".format(command))
