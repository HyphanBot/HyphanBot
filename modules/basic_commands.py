'''
This mod provides the basic commands that display possible information about the bot.
'''

def dispatch(api, updater):
        def help_cmd(bot, update, args):
                # TODO: Add easter egg and get help text and other settings from config
                bot.sendMessage(chat_id=update.message.chat_id, text=api.get_help(args))

        def about(bot, update):
                # TODO: Get text and other settings from config
                bot.sendMessage(chat_id=update.message.chat_id,
                                text="I am King %s, ruler of the northern part of the galaxy." % bot.getMe().first_name)

        def anti_nick(bot, update):
                msg = update.message.text.lower()

                if msg == "..":
                        bot.sendMessage(chat_id=update.message.chat_id, text="Three dots, Nick.")

        def noslash(bot, update):
                msg = update.message.text
                if msg == "help":
                        help_cmd(bot, update)
                elif msg == "about":
                        about(bot, update)

        dp = updater.dispatcher
        dp.addTelegramCommandHandler("help", help_cmd)
        dp.addTelegramCommandHandler("about", about)
        dp.addTelegramMessageHandler(noslash)
        dp.addTelegramMessageHandler(anti_nick)

        api.set_help("help", "Gets help for a specified command:\n/help [command name]")
        api.set_help("about", "A message of our great leader:\n/about")
