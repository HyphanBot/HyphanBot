# Development commands

def dispatch(mod, updater):
	dp = updater.dispatcher

	def devChannel(bot, update, args):
		if mod.api.is_sender_admin(update):
			msg = " ".join(args)
			channel = mod.get_config("channel")
			bot.sendMessage(chat_id=channel, text=msg)
		else:
			bot.sendMessage(chat_id=update.message.chat_id, text="You're not admin.")

	dp.addTelegramCommandHandler("devpost", devChannel)