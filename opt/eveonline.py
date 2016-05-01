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
from telegram.ext import CommandHandler

class Commands(object):
    """The logic of the hyphan commands"""
    eveapi.set_user_agent("eveapi.py/1.3")
    eveAPI = eveapi.EVEAPIConnection()
    # the following is a plugin which keeps tracks and reports when a EVE
    # online character finishes training

    def getalliances(self, bot, update):
        """Get a list of the top alliances"""
        result = self.eveAPI.eve.AllianceList()
        alliancelist = ""

        for alliance in result.alliances:
            if alliance.memberCount >= 2000:
                alliancelist = alliancelist + '\n' + "%s <%s> has %d members" %\
                               (alliance.name, alliance.shortName, alliance.memberCount)

        bot.sendMessage(chat_id=update.message.chat_id, text="{}".format(alliancelist))

    def characters(self):
        """Returns a dict with the characters defined in the configuration file"""
        characters = API.get_config("characters").split()
        character_dict = {}

        for character in characters:
            character_config = API.get_config("character." + character)
            character_dict[character] = character_config

        return character_dict

    def balance(self, bot, update, args):
        """Get the balance of the characters"""
        character_dict = self.characters()

        if len(args) == 0:
            bot.sendMessage(chat_id=update.message.chat_id, text="Please specify a character " \
                            "of whom you want to check the balance of.")
        elif ''.join(args).lower() == "all":
            characterslist = API.get_config("characters").split()

            for character in characterslist:
                self.balance(bot, update, character)
        else:
            character = ''.join(args)
            characterinfo = character_dict[character].split()
            api_id = characterinfo[:1]
            api_vcode = characterinfo[1:2]

            auth = self.eveAPI.auth(keyID=api_id, vCode=api_vcode)
            result = auth.account.Characters()

            for character in result.characters:
                wallet = auth.char.AccountBalance(characterID=character.characterID)
                isk = wallet.accounts[0].balance
                bot.sendMessage(chat_id=update.message.chat_id, text="{0} has {1} ISK"\
                                .format(character.name, '{0:,}'.format(isk)))

class Dispatch(object):
    """Set the metadata for the hyphan commands"""

    def __init__(self, updater):
        self.updater = updater
        self.set_config()
        self.define_commands()
        self.define_help()
        self.set_api(self.api)

    def set_api(self, temp):
        """A simple function to avoid using arcane variable names"""
        global API
        API = temp
        self.api = API


    def set_config(self):
        """Set values when they are not found in the configuration file"""
        if not self.api.get_config():
            default_keys = {
                "enabled": "yes",
                "character": "foo bar"
            }

            self.api.set_config(default_keys)

    def define_commands(self):
        """Bind the commands"""
        dispr = self.updater.dispatcher
        cods = Commands()

        dispr.addHandler(CommandHandler("evealliance", cods.getalliances))
        dispr.addHandler(CommandHandler("evechar", cods.characters))
        dispr.addHandler(CommandHandler("evecharacters", cods.characters))
        dispr.addHandler(CommandHandler("evewallet", cods.balance, pass_args=True))

    def define_help(self):
        """Define the help messages"""
        self.api.set_help("evealliance", "A list of the top EVE alliances.```/evealliance```")
        self.api.set_help("evewallet", "Give the amount of ISK owned by a character." \
                          "\n`/evewallet [character]`\n`/evewallet all`")

        for command in ["evechar", "evecharacters"]:
            self.api.set_help(command, "Return a list of the defined EVE characters.```/{}```" \
                              .format(command))
