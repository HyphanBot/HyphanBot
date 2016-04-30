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
'''
import xkcd

class Commands(object):
    """The program logic of the hyphan commands"""
    def get_comic(self, bot, update, args):
        """Fetch the comics"""
        if len(args) == 0:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text="Please specify which comic you want to read.")
            return None
        elif args[0].isdigit():
            comic = xkcd.getComic(int(args[0]))
        elif args[0] == "latest":
            comic = xkcd.getLatestComic()
        elif args[0] == "random":
            comic = xkcd.getRandomComic()

        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Title: {0}\nLink: {1}\nText: {2}".format(comic.getTitle(),
                                                                       comic.getImageLink(),
                                                                       comic.getAltText()))

    def random(self, bot, update):
        """Alias for fetching a random comic"""
        return self.get_comic(bot, update, ["random"])

    def latest(self, bot, update):
        """Same but for the latest comic"""
        return self.get_comic(bot, update, ["latest"])

class Dispatch(object):
    """Make Telegram accept the commands"""
    def __init__(self, api, updater):
        self.api = api
        self.updater = updater
        self.define_commands()
        self.define_help()

    def define_commands(self):
        """Define the commands"""
        dispr = self.updater.dispatcher
        cods = Commands()

        dispr.addTelegramCommandHandler("xkcd", cods.get_comic)
        dispr.addTelegramCommandHandler("xkcd_random", cods.random)
        dispr.addTelegramCommandHandler("xkcdr", cods.random)
        dispr.addTelegramCommandHandler("xkcd_latest", cods.latest)
        dispr.addTelegramCommandHandler("xkcdl", cods.latest)

    def define_help(self):
        """Define the help messages"""
        self.api.set_help("xkcd", "Gives you either a specified, random or the latest xkcd " \
                          "comic.\n`xkcd [random, latest, comicid]`")

        for alias in ["xkcdr", "xkcd_random"]:
            self.api.set_help(alias, "An alias for `/xkcd random`.")

        for alias in ["xkcdl", "xkcd_latest"]:
            self.api.set_help(alias, "An alias for `/xkcd latest`.")
