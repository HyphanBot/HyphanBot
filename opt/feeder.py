import hashlib
import threading
import time

from telegram.ext import CommandHandler
from telegram import ParseMode
import feedparser

class Feeder(object):
    """docstring for Feeder"""
    def __init__(self):
        self.feeds = []
        self.update_interval = 5
        self.notify_chatids = []

    def get_new_feed(self, parsed_feed):
        new_feed = feedparser.parse(parsed_feed.href, etag=parsed_feed.etag)
        if new_feed.status == 304:
            return False
        return new_feed

    def add_feed(self, bot, update, arg):
        chat_id = update.message.chat_id
        feed_url = arg
        for i, feed in enumerate(self.feeds):
            if feedparser.parse(feed_url).href in feed["url"]:
                if chat_id not in feed["chat_ids"]:
                    self.feeds[i]["chat_ids"].append(chat_id)
                    bot.sendMessage(chat_id, text="Feed added to this chat.")
                    return
                else:
                    bot.sendMessage(chat_id, text="Feed already added.")
                    return
        self.feeds.append({"url":feed_url, "chat_ids":[chat_id]})
        bot.sendMessage(chat_id, text="Added feed.")

    def rem_feed(self, bot, update, arg):
        chat_id = update.message.chat_id
        feed_url = arg
        removed = False
        for i, feed in enumerate(self.feeds):
            if feed["url"] == feed_url:
                if chat_id in feed["chat_ids"]:
                    while chat_id in feed["chat_ids"]:
                        self.feeds[i]["chat_ids"].remove(chat_id)
                    if len(self.feeds[i]["chat_ids"]) == 0:
                        self.feeds.remove(feed)
                    removed = True
                else:
                    bot.sendMessage(chat_id, text="No such feed in this chat.")
        if removed:
            bot.sendMessage(chat_id, text="Removed feed from this chat.")
        else:
            bot.sendMessage(chat_id, text="Feed not found.")

    def list_feeds(self, bot, update):
        bot.sendMessage(update.message.chat_id, text=self.feeds)

    '''
    def check_new_entries(self, bot):
        for i, feed in enumerate(self.feeds):
            new_feed = self.get_new_feed(feedparser.parse(feed["url"]))
            if new_feed is not False:
                self.feeds[i]["url"] = new_feed.href
                for chatid in feed["chat_ids"]:
                    self.post_entry(bot, new_feed.entries[0], chatid)
    '''

    def check_new_entries(self, bot, oldfeeds, chatid):
        for oldfeed in oldfeeds:
            new_feed = self.get_new_feed(oldfeed)
            print(new_feed)
            if new_feed is not False:
                self.post_entry(bot, new_feed.entries[0], chatid)

    def post_entry(self, bot, entry, chatid):
        bot.sendMessage(chat_id=chatid, text=entry.title+"\n"+entry.link)

    def update_loop(self, bot, chatid):
        while chatid in self.notify_chatids:
            oldfeeds = []
            for feed in self.feeds:
                oldfeeds.append(feedparser.parse(feed["url"]))
            time.sleep(self.update_interval)
            self.check_new_entries(bot, oldfeeds, chatid)

    def start_notify(self, bot, update):
        chat_id = update.message.chat_id
        if chat_id not in self.notify_chatids:
            self.notify_chatids.append(chat_id)
            timerthread = threading.Thread(target=self.update_loop, args=(bot, chat_id))
            timerthread.daemon = True
            timerthread.start()
        else:
            bot.sendMessage(chat_id, text="RSS notifications are already enabled for this chat.")
            return
        bot.sendMessage(chat_id, text="RSS notifications are now enabled for this chat.")

    def stop_notify(self, bot, update):
        chat_id = update.message.chat_id
        if chat_id not in self.notify_chatids:
            bot.sendMessage(chat_id, text="RSS notifications are already disabled for this chat.")
            return
        while chat_id in self.notify_chatids: self.notify_chatids.remove(chat_id)
        bot.sendMessage(chat_id, text="RSS notifications are now disabled for this chat.")

    def cmd_handle(self, bot, update, args):
        if len(args) == 1:
            if args[0] == "list":
                self.list_feeds(bot, update)
            else:
                bot.sendMessage(update.message.chat_id, text="Invalid argument.")
        elif len(args) == 2:
            if args[0] == "add":
                self.add_feed(bot, update, args[1])
            elif args[0] == "remove" or args[0] == "rem":
                self.rem_feed(bot, update, args[1])
            elif args[0] == "notify":
                if args[1] == "start" or args[1] == "on":
                    self.start_notify(bot, update)
                elif args[1] == "stop" or args[1] == "off":
                    self.stop_notify(bot, update)
                else:
                    bot.sendMessage(update.message.chat_id, text="Invalid arguments.")
            else:
                bot.sendMessage(update.message.chat_id, text="Invalid arguments.")
        elif len(args) == 0:
            bot.sendMessage(update.message.chat_id,
                    text="/feed command. Reads RSS and Atom feeds.\nType `/help feed` for more information",
                    parse_mode=ParseMode.MARKDOWN)
        else:
            bot.sendMessage(update.message.chat_id,
                    text="Invalid number of arguments. Type `/help feed` for help on how to use this command",
                    parse_mode=ParseMode.MARKDOWN)

class Dispatch(object):
    """docstring for Dispatch"""
    def __init__(self, api, updater):
        feeder = Feeder()
        dispr = updater.dispatcher
        dispr.addHandler(CommandHandler("feed", feeder.cmd_handle, pass_args=True))
        api.set_help("feed", """`/feed` command *[WORK IN PROGRESS]*
Reads RSS and Atom feeds and can notify on new updates.
`/feed add` - Adds a new feed for the current chat
`/feed remove` - Removes a feed for the current chat
`/feed list` - Lists feeds
`/feed notify on` - Enables notifications for current chat
`/feed notify off` - Disables notification for current chat
""")
