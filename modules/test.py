'''
This is an example of how a Hyphan mod is structured.

A "Mod" is basically a plugin or extention that extends Hyphan by adding
extra features and abilities to the bot.
The reason why they're called 'Mods' instead of 'modules' is to not
confuse them with Python modules, since Hyphan is written in Python.

The following code and comments describes the basic structure of how
command mods work.
'''

# Function that defines your mod. This will be called by your dispatch()
# function when the command is executed.
def test(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Tested!!")

# A mod can also dispatch more than one command.
# The following is an example of a function that gets called when another
# command is executed.
def testTwo(bot, update, args):
	args = ', '.join(args)
	bot.sendMessage(chat_id=update.message.chat_id, text="Tested for args: "+args)

# The following handles commands that are executed without slashes at the
# beginning.
def noslashtest(bot, update, args):
	msg = update.message.text
	if msg == "test":
		test(bot, update)
	elif msg == "test2" or msg == "testtwo" or msg == "testsecond":
		testTwo(bot, update, args)

# Dispatch function. This is required by every mod as it is called by the
# dispatcher in Hyphan's core.
def dispatch(api, updater, logger):
	# Get dispatcher
	dp = updater.dispatcher

	# This listens for the command "/test" and calls the test() function if
	# the command is executed
	dp.addTelegramCommandHandler("test", test)

	# This one executes for all messages
	dp.addTelegramMessageHandler(noslashtest)

	# You can also handle the same functionaltiy for multiple commands:
	dp.addTelegramCommandHandler("test2", testTwo)
	dp.addTelegramCommandHandler("testtwo", testTwo)
	dp.addTelegramCommandHandler("secondtest", testTwo)