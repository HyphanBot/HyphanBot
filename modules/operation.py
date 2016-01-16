'''
This mod operates the bot. It can quit or restart Hyphan.
'''

import os, signal

global operMod

def quit(bot, update):
        if operMod.api.is_sender_admin(update): # Use the API to check if sender is admin
                bot.sendMessage(chat_id=update.message.chat_id, 
                        text="Goodbye!")
                os.kill(os.getpid(), signal.SIGTERM)
        else:
                bot.sendMessage(chat_id=update.message.chat_id, 
                        text="Sorry, %s, I'm afraid I can't let you do that." % update.message.from_user.first_name)

def restart(bot, update):
        # This will only restart the bot if it was running from the launcher script (currently run.sh)
        if operMod.api.is_sender_admin(update): # Use the API to check if sender is admin
                bot.sendMessage(chat_id=update.message.chat_id, 
                        text="See ya!")
                os.kill(os.getpid(), signal.SIGKILL)
        else:
                bot.sendMessage(chat_id=update.message.chat_id, 
                        text="Sorry, %s, I'm afraid I can't let you do that." % update.message.from_user.first_name)

def reload_config(bot, update):
        if operMod.api.is_sender_admin(update):
                operMod.api.config.refresh_config()
                bot.sendMessage(chat_id=update.message.chat_id, 
                        text="Configuration file reloaded.")
        else:
                bot.sendMessage(chat_id=update.message.chat_id, 
                        text="Sorry, %s, I'm afraid I can't let you do that." % update.message.from_user.first_name)

def noslash(bot, update):
        msg = update.message.text
        if msg == "quit":
                quit(bot, update)
        elif msg == "restart":
                restart(bot, update)
        elif msg == "reloadconf" or msg == "reconf":
                reload_config(bot, update)

def dispatch(mod, updater):
        global operMod

        operMod = mod
        dp = updater.dispatcher

        dp.addTelegramCommandHandler("quit", quit)
        dp.addTelegramCommandHandler("restart", restart)

        dp.addTelegramCommandHandler("reloadconf", reload_config)
        dp.addTelegramCommandHandler("reconf", reload_config)

        dp.addTelegramMessageHandler(noslash)
