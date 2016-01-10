from telegram import Update, Bot, Updater
from dispatcher import *
from api import *
from configparser import SafeConfigParser
from os import mkdir
from os.path import expanduser

import logging
import pathlib
import notify2

# Log everything
logging.basicConfig(
        format='%(asctime)s - %(name)s [%(levelname)s]: %(message)s',
        level=logging.INFO)
logger = logging.getLogger(__name__)

def error(bot, update, error):
        logger.warn('Error occured in update, "%s": %s' % (update, error))
        notify2.Notification("Error occured in update '%s': '%s'" % (update, error)) 

def init_config():
        HOME            = expanduser("~")
        XDG_CONFIG      = HOME + '/.config/hyphan/config.ini'
        CONFIG_FALLBACK = HOME + '~/.hyphan/config.ini'
        LAST_HOPE       = HOME + '~/.hyphanrc'

        config = SafeConfigParser()
        
        if pathlib.Path(XDG_CONFIG).exists():
           config.read(XDG_CONFIG)
        elif pathlib.Path(CONFIG_FALLBACK).exists():
           config.read(CONFIG_FALLBACK)
        elif pathlib.Path(LAST_HOPE).exists():
           config.read(LAST_HOPE)
        else:
           print("No configuration file has been found")
           answer = input("Do you want me to copy the standard boiler plate to ~/.config/hyphan/config.ini? [Y/n] ")
           if not answer.lower() == "n" or answer.lower() == "no":
                answer = input("Do you want to enter the info interactively? [Y/n] ")
                if not answer.lower() == "n":
                        mkdir(HOME + '/.config/hyphan')
                        writefile = open(XDG_CONFIG, "w")
                        botname   = input("What is the official botname? ")
                        friendly  = input("What is a friendly name for the bot? ")
                        token     = input("What is the Telegram token? ")
                        admins    = input("Who are the admins? ")
                        writefile.write(str("[general]\nBotname         = {0}\nfriendlyBotName = {1}\ntoken           = {2}\nadmins          = {3}".format(botname, friendly, token, admins)))
                        writefile.close()
                else:
                        mkdir(HOME + '/.config/hyphan')
                        writefile = open(XDG_CONFIG, "w")
                        writefile.write(str(
"""[general]
Botname         = foo
friendlyBotName = bar
token           = baz
admins          = foobarbaz"""))
                        writefile.close()
                        print("Don't forget to edit the file before you start the program again!")
           quit()
        return config

def start_bot():
        config          = init_config()
        token           = config.get("general", "token")
        botname         = config.get("general", "botname")
        friendlyBotName = config.get("general", "friendlybotname")

        token           = config.get("general", "token")
        botname         = config.get("general", "botname")
        friendlyBotName = config.get("general", "friendlybotname")

        updater = Updater(token)
        getBot  = updater.bot.getMe()

        api = HyphanAPI(updater)

        # Notify that the bot started
        notify2.init(friendlyBotName)
        notify2.Notification("Initialized {}".format(friendlyBotName),
                             "{} has started".format(friendlyBotName),
                             "notification-message-im").show()
        # Dispatch modules
        dp = updater.dispatcher
        loadModules(api, updater, logger)
        dp.addErrorHandler(error)

        # Start the bot
        updater.start_polling()
        logger.info("Initialized %s (%s)." % (getBot.first_name, getBot.username))
        updater.idle()

def main():
        start_bot()

if __name__ == '__main__':
        main()
