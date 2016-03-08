'''
This is an example of how a Hyphan mod is structured.

A "Mod" is basically a plugin or extention that extends Hyphan by adding
extra features and abilities to the bot.
The reason why they're called 'Mods' instead of 'modules' is to not
confuse them with Python modules, since Hyphan is written in Python.

The following code and comments describes the basic structure of how
command mods work.
'''
global helloMod

# Dispatch function. This is the core of every mod.
# This is what Hyphan calls to initialize the mod.
def dispatch(mod, updater):

        # Function that defines your mod. This will be called when the command
        # is executed.
        # In this example, the message will be provided from the configuration file.
        def hello(bot, update):
                bot.sendMessage(chat_id=update.message.chat_id, text="{}".format(mod.get_config("message")))

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
        def stupid(bot, update, args):
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

        ## Dispatching! ##

        # Check and set the config with default keys.
        # This will be under your mod's section (identified by your mod's filename
        # (without the extention), in this case 'test')
        if not mod.get_config():
                default_keys = {
                        "enabled": "yes",
                        "message": "Hello!"
                }

                mod.set_config(default_keys)

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

        # Adds help text to the commands
        mod.set_help('goodbye', "Says goodbye to you when you ask for it.")
        mod.set_help('hello', 'Hello world!')
