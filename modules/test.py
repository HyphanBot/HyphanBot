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
The reason why they are called 'Mods' instead of 'modules' is to not
confuse them with Python modules, since Hyphan is written in Python.

The following code and comments describes the basic structure of how
command mods work.
'''

from telegram.ext import CommandHandler, Filters

# Create a class where you can define the commands
class Commands(object):
    """Define the program logic of the module. Only used as a namespace to enforce a, slightly,
    more sensible layout for the program"""
    # Function that defines your mod. This will be called when the command
    # is executed.
    # In this example, the message will be provided from the configuration file.
    def hello(self, bot, update):
        """Return the string that is defined in the configuration file"""
        bot.sendMessage(chat_id=update.message.chat_id, text="{}".format(API.get_config("message")))

    # A mod can also dispatch more than one command.
    # The following is an example of a function that gets called when another
    # command is executed.
    def goodbye(self, bot, update, args):
        """Return the string Goodbye ARGS!"""
        if len(args) != 0:
            bot.sendMessage(chat_id=update.message.chat_id, text="Goodbye {}!" \
                            .format(' '.join(args)))
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text="Goodbye!")

    # The following functions handle regular messages. These examples define
    # commands that are executed without slashes at the beginning.
    def stupid(self, bot, update):
        """stupid human!"""
        msg = update.message.text.lower()

        if msg == "stupid bot" or msg == "stupid bot!" or msg == "stupid bot.":
            bot.sendMessage(chat_id=update.message.chat_id, text="Stupid human.")

    def noslash(self, bot, update):
        """Bind the commands using words or sentences instead of purely commands"""
        # get the message
        msg = update.message.text.lower()
        args = msg.split(" ")

        if msg == "hello":
            self.hello(bot, update)
        elif msg.startswith("goodbye"):
            self.goodbye(bot, update, args[1])

    def handle_msgs(self, bot, update):
        """Handle messages"""
        self.noslash(bot, update)
        self.stupid(bot, update)

# Dispatch class. This is the core of every mod.
# This is what Hyphan calls to initialize the mod.
class Dispatch(object):
    """Deals with the various metadata that Hyphan requires including help messages and the like"""
    # run definitions on launch
    def __init__(self, api, updater):
        global API
        API = api

        self.api = api
        self.updater = updater
        self.set_config()
        self.define_help()
        self.define_commands()

    ## Dispatching! ##
    # Check and set the config with default keys.
    # This will be under your mod's section (identified by your mod's filename
    # (without the extention), in this case 'test')
    def set_config(self):
        """Set the configuration values if they do not exist yet"""
        if not self.api.get_config():
            default_keys = {
                "enabled": "yes",
                "message": "Hello!"
            }
            self.api.set_config(default_keys)

    # Assign commands to the defs
    def define_commands(self):
        """Bind the commands to the functions"""
        # Get dispatcher
        dispr = self.updater.dispatcher

        # Get the commands
        commands = Commands()

        # This listens for the command "/goodbye" and calls the goodbye() function if the
        # command is executed
        dispr.addHandler(CommandHandler("goodbye", commands.goodbye, pass_args=True))

        # You can also handle the same functionaltiy for multiple commands:
        dispr.addHandler(CommandHandler("hello", commands.hello))
        dispr.addHandler(CommandHandler("morning", commands.hello))
        dispr.addHandler(CommandHandler("hi", commands.hello))

        # A command that will execute with no slash
        self.api.add_message_handler([Filters.text], commands.handle_msgs)

    # Assigns help messages to the commands
    def define_help(self):
        """Adds help messages to the commands"""
        # Adds help text to the commands
        self.api.set_help('goodbye', "Says goodbye to you when you ask for it.")
        self.api.set_help('hello', 'Hello world!')
