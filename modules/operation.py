'''
This mod operates the bot. It can quit or restart Hyphan.
'''

import os, signal

botController = None
botApi = None

def quit(bot, update):
        global botController
        global botApi
        
        terminate = False
        for admin in botApi.api.get_admins(): # Get a list of admins from the API
                print(admin)
                # If the username is in the admin list, quit the bot
                if update.message.from_user.username == admin:
                        bot.sendMessage(chat_id=update.message.chat_id, 
                                text="Goodbye!")
                        terminate = True
                        break

        if terminate:
                os.kill(os.getpid(), signal.SIGTERM)

def restart(bot, update):
        global botApi

        for admin in botApi.api.get_admins():
                # If the username is in the admin list, restart the bot
                # Will only restart if the bot is running from the launcher script.
                if update.message.from_user.username == admin:
                        bot.sendMessage(chat_id=update.message.chat_id, 
                                text="See ya!")
                        os.kill(os.getpid(), signal.SIGKILL)
                else:
                        bot.sendMessage(chat_id=update.message.chat_id, 
                                text="Sorry, %s, I'm afraid I can't let you do that." % update.message.from_user.first_name)

def noslash(bot, update):
        msg = update.message.text
        if msg == "quit":
                quit(bot, update)
        elif msg == "restart":
                restart(bot, update)

def dispatch(api, updater):
        global botController
        global botApi

        botController = updater
        botApi = api
        dp = updater.dispatcher

        dp.addTelegramCommandHandler("quit", quit)
        dp.addTelegramCommandHandler("restart", restart)
        dp.addTelegramMessageHandler(noslash)
