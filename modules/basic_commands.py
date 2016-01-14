'''
This mod provides the basic commands that display possible information about the bot.
'''

def help_cmd(bot, update):
	# TODO: Add easter egg and get help text and other settings from config
	bot.sendMessage(chat_id=update.message.chat_id, text="?")

def about(bot, update):
	# TODO: Get text and other settings from config
	bot.sendMessage(chat_id=update.message.chat_id, 
		text="I am King %s, ruler of the northern part of the galaxy." % bot.getMe().first_name)

def noslash(bot, update):
	msg = update.message.text
	if msg == "help":
		help_cmd(bot, update)
	elif msg == "about":
		about(bot, update)

def dispatch(api, updater):
	dp = updater.dispatcher

	dp.addTelegramCommandHandler("help", help_cmd)
	dp.addTelegramCommandHandler("about", about)
	dp.addTelegramMessageHandler(noslash)
