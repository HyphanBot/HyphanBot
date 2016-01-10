'''
This is an example of how a Hyphan mod is structured.

A "Mod" is basically a plugin or extention that extends Hyphan by adding
extra features and abilities to the bot.
The reason why they're called 'Mods' instead of 'modules' is to not
confuse them with Python modules, since Hyphan is written in Python.

The following code and comments describes the basic structure of how
command mods work.
'''
global botApi

# Function that defines your mod. This will be called by your dispatch()
# function when the command is executed. The message will come from the
# configuration file.
def hello(bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="{}".format(botApi.config("hello", "message")))

# A mod can also dispatch more than one command.
# The following is an example of a function that gets called when another
# command is executed.
def goodbye(bot, update, args):
        bot.sendMessage(chat_id=update.message.chat_id, text="Goodbye {}!".format(''.join(args)))

# The following handles commands that are executed without slashes at the
# beginning.
def stupid(bot, update, args):
        msg = update.message.text.lower()

        if msg == "stupid bot" or msg == "stupid bot!" or msg == "stupid bot.":
                bot.sendMessage(chat_id=update.message.chat_id, text="Stupid human.")

def noslash(bot, update, args):
        # get the message
        msg = update.message.text.lower()
        
        if msg == "hello":
                hello(bot, update)
        elif msg == "goodbye":
                goodbye(bot, update, args)
        
# Dispatch function. This is required by every mod as it is called by the
# dispatcher in Hyphan's core.
def dispatch(api, updater, logger):
        # make the api usable in the entire file
        global botApi
        botApi = api

        # check if the module is enabled
        if api.config("hello", "enabled") == "yes":
                # Get dispatcher
                dp = updater.dispatcher
                
                # This listens for the command "/test" and calls the test() function if
                # the command is executed
                dp.addTelegramCommandHandler("goodbye", goodbye)
                dp.addTelegramCommandHandler("stupid bot", stupid)
                
                # A command that will execute will no slash
                dp.addTelegramMessageHandler(stupid)
                dp.addTelegramMessageHandler(noslash)

                # You can also handle the same functionaltiy for multiple commands:
                dp.addTelegramCommandHandler("hello", hello)
                dp.addTelegramCommandHandler("morning", hello)
                dp.addTelegramCommandHandler("hi", hello)
