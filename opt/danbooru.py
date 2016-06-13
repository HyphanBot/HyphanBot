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

----------------------

This Hyphan module can access and display images from the Danbooru and Konachan image boards.
Requires the installation of Pybooru.

'''
import logging
import random

from telegram.ext import CommandHandler, Filters

try:
    from pybooru import Pybooru
    import pyshorteners
except ImportError:
    LOGGER = logging.getLogger(__name__)
    LOGGER.info("Cannot load this module since one or multiple modules cannot be imported.")

class Commands(object):
    """Define the program logic of the module"""
    def send_picture(self, bot, chat_id, site, url, short_url, author, postid, tags):
        """Send the picture and the post information"""
        bot.sendPhoto(chat_id=chat_id, photo=url)
        bot.sendMessage(chat_id=chat_id,
                        text="Download Link: {0}\nAuthor: {1}\nLink: {2}/post/show/{3}\nTags: {4}"
                        .format(short_url, author, site, postid, tags),\
                        disable_web_page_preview=True)

    def random_post(self, bot, update, args):#, site, safe_mode=True, tag=None):
        """Get a random post from a danbooru, or like, site"""
        site = args[0]
        split_args = args[1:][0].split("=")
        tags = []

        if split_args[0] == "rating":
            tags += ["rating:{}".format(split_args[1][0])]
            tags += args[2:]
        else:
            tags += ["rating:s"]
            tags += args[1:]

        tags = ' '.join(tags)

        client = Pybooru(site)
        posts = client.posts_list(tags, 100)
        shortener = pyshorteners.Shortener('Isgd')

        if len(posts) <= 0:
            bot.sendMessage(chat_id=update.message.chat_id, text="No posts found.")
        else:
            random_number = random.randint(0, len(posts) - 1)
            random_post = posts[random_number]

            if client.get_api_type() == "dan2":
                self.send_picture(bot, update.message.chat_id,
                                  client.site_url,
                                  client.site_url + random_post['file_url'],
                                  shortener.short(client.site_url+random_post['large_file_url']),
                                  random_post['uploader_name'],
                                  random_post['id'],
                                  random_post['tag_string'])
            else:
                self.send_picture(bot, update.message.chat_id,
                                  client.site_url,
                                  random_post['sample_url'],
                                  shortener.short(random_post['file_url']),
                                  random_post['author'],
                                  random_post['id'],
                                  random_post['tags'])


class Dispatch(object):
    """Register the module to the bot"""
    def __init__(self, api, updater):
        self.api = api
        self.updater = updater
        self.define_commands()

        api.set_help("booru", "Fetches a picture from a danbooru or moebooru like site." +
                     "Currently only yandere and konachan are supported.\n\n" +
                     "/booru [site] rating=[rating] [tags]")

    def define_commands(self):
        """Bind the commands to the functions"""
        dispr = self.updater.dispatcher
        cods = Commands()
        dispr.add_handler(CommandHandler("booru", cods.random_post, pass_args=True))
