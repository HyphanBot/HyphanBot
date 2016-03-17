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
    def get_comic(self, bot, update, args):
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
        return self.get_comic(bot, update, ["random"])

    def latest(self, bot, update):
        return self.get_comic(bot, update, ["latest"])

class dispatch(object):
    def __init__(self, api, updater):
        self.define_commands(updater)
        self.define_help(api)

    def define_commands(self, updater):
        dp = updater.dispatcher
        c = Commands()

        dp.addTelegramCommandHandler("xkcd", c.get_comic)
        dp.addTelegramCommandHandler("xkcd_random", c.random)
        dp.addTelegramCommandHandler("xkcdr", c.random)
        dp.addTelegramCommandHandler("xkcd_latest", c.latest)
        dp.addTelegramCommandHandler("xkcdl", c.latest)

    def define_help(self, api):
        api.set_help("xkcd", "Gives you either a specified, random or the latest xkcd comic.\n/`xkcd [random, latest, comicid]`")

        for alias in ["xkcdr", "xkcd_random"]:
            api.set_help(alias, "An alias for `/xkcd random`.")

        for alias in ["xkcdl", "xkcd_latest"]:
            api.set_help(alias, "An alias for `/xkcd latest`.")
