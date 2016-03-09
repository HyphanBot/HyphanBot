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
----
This is an example of how a Hyphan mod is structured.

A "Mod" is basically a plugin or extention that extends Hyphan by adding
extra features and abilities to the bot.
The reason why they're called 'Mods' instead of 'modules' is to not
confuse them with Python modules, since Hyphan is written in Python.

The following code and comments describes the basic structure of how
command mods work.
'''

# Function that defines your mod. This will be called when the command
# is executed.
# In this example, the message will be provided from the configuration file.
def hello(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="{}".format(api.get_config("message")))

# A mod can also dispatch more than one command.
# The following is an example of a function that gets called when another
# command is executed.
def goodbye(bot, update, args):
    if len(args) != 0:
        bot.sendMessage(chat_id=update.message.chat_id, text="Goodbye {}!".format(''.join(args)))
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Goodbye!")

# The following functions handle regular messages. These examples define
# commands that are executed without slashes at the beginning.
def stupid(bot, update):
    msg = update.message.text.lower()

    if msg == "stupid bot" or msg == "stupid bot!" or msg == "stupid bot.":
        bot.sendMessage(chat_id=update.message.chat_id, text="Stupid human.")

def noslash(bot, update, args):
    # get the message
    msg = update.message.text.lower()

    if msg == "hello":
        hello(bot, update)
    elif msg.startswith("goodbye"):
        goodbye(bot, update, args)

# Dispatch class. This is the core of every mod.
# This is what Hyphan calls to initialize the mod.
class dispatch(object):
    # run definitions on launch
    def __init__(self, api, updater):
        self.set_api(api)
        self.set_config(api)
        self.define_help(api)
        self.define_commands(updater)

    # set the global api variable
    def set_api(self, temp):
        global api
        api = temp

    ## Dispatching! ##
    # Check and set the config with default keys.
    # This will be under your mod's section (identified by your mod's filename
    # (without the extention), in this case 'test')
    def set_config(self, api):
        if not api.get_config():
            default_keys = {
                "enabled": "yes",
                "message": "Hello!"
            }
            api.set_config(default_keys)

    # Assign commands to the defs
    def define_commands(self, updater):
        # Get dispatcher
        dp = updater.dispatcher

        # This listens for the command "/goodbye" and calls the goodbye() function if the
        # command is executed
        dp.addTelegramCommandHandler("goodbye", goodbye)

        # You can also handle the same functionaltiy for multiple commands:
        dp.addTelegramCommandHandler("hello", hello)
        dp.addTelegramCommandHandler("morning", hello)
        dp.addTelegramCommandHandler("hi", hello)

        # A command that will execute will no slash
        dp.addTelegramMessageHandler(stupid)
        dp.addTelegramMessageHandler(noslash)

    # Assigns help messages to the commands
    def define_help(self, api):
        # Adds help text to the commands
        api.set_help('goodbye', "Says goodbye to you when you ask for it.")
        api.set_help('hello', 'Hello world!')
