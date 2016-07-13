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

from os import path
import threading
import logging
import random
import time

import requests
from telegram import ParseMode
from telegram.ext import CommandHandler, Filters
#from tdqm import tdqm # Progress bar module. Install: pip install tqdm

'''
Hyphan experiment: Shiritori/Word_Chain game module

TODO: Implement score system based on https://shiritorigame.com
        - Optional: Subtract the remaining time from the score in each turn (Speed bonus)
'''


class Shiritori(object):
    """
    Shiritori game.

    Args:
        mod (core.HyphanAPI.Mod): Mod's local API
    """
    def _config_or_fallback(self, item, fallback):
        try:
            return self.api.get_value(item, __name__)
        except TypeError:
            raise
        except KeyError:
            return fallback

    def __init__(self, api):
        self.logger = logging.getLogger(__name__)
        self.api = api
        
        self.helptext = """
*Shiritori*, also known as *Word Chain*, is a game in which the players say a word that begins with the last letter of the previous word.
_Shiritori_ originated in Japan. The word "Shiritori" literally means "taking the end" according to [Wikipedia](https://en.wikipedia.org/wiki/Shiritori) (See also: [Word Chain](https://en.wikipedia.org/wiki/Word_chain)).

I can only play this game in English. I'm currently hard to beat and I might use really long words, but I was just taught to not be fair... Sorry.
To start a match with me, type:
    `/shiritori start` or `/wordchain start`
"""

        # The constant time limit for each turn in seconds (default: 30)
        self.limit = self._config_or_fallback("timelimit", 30)
        self.timer = self.limit  # Remaining time in seconds

        # The score at the beginning of the game (default: 100)
        self.startscore = self._config_or_fallback("startscore", 100)
        self.score = self.startscore  # The user's score
        self.pc_score = self.startscore  # Hyphan's score

        # The minimum number of characters allowed (default: 3)
        self.minlen = self._config_or_fallback("minimumlength", 3)

        # Message if user wins (default: "Senpai, tell me your secrets!")
        self.winmsg = self._config_or_fallback("winmessage",
                                               "Senpai, tell me your secrets!")

        # Message if user loses (default: "This was so predictable, hehe.")
        self.losemsg = self._config_or_fallback("losemessage",
                                                "This was so predictable, hehe.")

        # Gets and downloads the wordlist if not already downloaded
        self.wordlist = self.get_wordlist(
            self._config_or_fallback("wlurl",
                                     "https://techisized.com/hyphanbot/SCOWL-wl/words.txt"),
            self._config_or_fallback("wlsavename",
                                     "shiritori_wordlist.txt"))

        self.started = False
        self.lastword = None
        self.used_words = []
        self.uturn = False # determines if it's the user's turn.

    def set_timer(self, bot, update):
        """
        Timer thread method. This will run on the user's turn each time.
        """
        while self.started:
            if self.uturn:
                if not self.timer <= 0:
                    self.timer = self.timer-1
                    time.sleep(1)
                else:
                    comment = ""
                    if self.pc_score < self.score:
                        comment = "You knew I was gonna win, didn't you? You still lost, though."
                    elif self.score < self.pc_score:
                        comment = "You could've won, ya know."
                    elif self.pc_score == self.score:
                        comment = "Looks like it would've been a tie. Too bad you lost, though."
                        response = """
Time's up! Game over.
=======Scores=======
Player: %s
%s: %s
%s
""" % (self.score, bot.getMe().first_name, self.pc_score, comment)
                        bot.sendMessage(chat_id=self.gamechat, text=response)
                        self.started = False
            else:
                self.timer = self.limit
                time.sleep(0.1)

    def start_game(self, bot, update, args):
        """
        Initiates a game of shiritori. Called on command.
        """
        if len(args) is 1 and args[0] == "start":
            self.started = True
            self.timer = self.limit
            self.score = self.startscore
            self.pc_score = self.startscore
            self.used_words = []
            self.gamechat = update.message.chat_id
            timerthread = threading.Thread(target=self.set_timer, args=(bot, update))
            timerthread.daemon = True
            timerthread.start()
            self.pc_turn(bot, update)
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text=self.helptext,
                            parse_mode=ParseMode.MARKDOWN)

    def pc_turn(self, bot, update, word=None):
        """
        Picks a random word from the wordlist based on the user's last word. This
        method is called on Hyphan's turn each time.
        """
        self.uturn = False
        if word is None:
            # If there is no given user word (if the game was just started), choose a random word.
            response = random.choice(self.wordlist)
        else:
            # Choose a random word that starts with the last letter of the user's word
            chosen_word = random.choice(list(filter(lambda x: x[0] == word[-1:], self.wordlist)))
            while (chosen_word in self.used_words) or (len(chosen_word) == 1):
                # As long as the word is used or is one letter, keep chosing another word.
                # This prevents Hyphan from losing.
                chosen_word = random.choice(
                    list(filter(lambda x: x[0] == word[-1:], self.wordlist)))
            self.pc_score = self.pc_score - (len(chosen_word) - self.minlen)
            response = chosen_word
        self.lastword = response
        self.used_words.append(self.lastword)
        bot.sendMessage(chat_id=self.gamechat, text=response)
        if self.pc_score <= 0:
            self.started = False
            response = """
I win!!! You lost.
======Scores======
Player: %s
%s: 0 (real score: %s)
%s
""" % (self.score, bot.getMe().first_name, self.pc_score, self.losemsg)
            bot.sendMessage(chat_id=self.gamechat, text=response)
        else:
            self.uturn = True

    def shiritori(self, bot, update):
        """
        Message handler. Handles the user's messages during gameplay.
        """
        currentchat = update.message.chat_id
        message = update.message.text.lower()
        response = None

        if (self.started and self.uturn) and self.gamechat == currentchat:
            valid_word = True

            if message not in self.wordlist:
                response = "'%s' is not found in my word list! Try again!" % message
                valid_word = False
            if not message.startswith(self.lastword[-1:]):
                response = "'%s' does not start with '%s'. Try again!" % (
                    message, self.lastword[-1:])
                valid_word = False
            if len(message) == 1:
                response = "Cannot be a letter, has to be a word. Try again!"
                valid_word = False
            if message in self.used_words:
                response = "'%s' was already used! Try again!" % message
                valid_word = False

            if valid_word:
                self.used_words.append(message)
                self.score = self.score - (len(message) - self.minlen)
                self.pc_turn(bot, update, message)

            if self.score <= 0:
                self.started = False
                response = """
You win!!!
==Scores==
Player: 0 (real score: %s)
%s: %s
%s
""" % (self.score, bot.getMe().first_name, self.pc_score, self.winmsg)

            if response is not None:
                bot.sendMessage(chat_id=self.gamechat, text=response)

    def get_wordlist(self, url, filename="shiritori_wordlist.txt"):
        """
        Retrieves and downloads the wordlist on initializaton for use in the game.
        """
        if not path.exists(filename):
            self.logger.info("Wordlist not found; downloading new list. This can take a while.")
            r = requests.get(url, stream=True)
            filesize = len(r.content)
            with open(filename, 'wb') as filehandle:
                try:
                    # Progress bar module. Install: pip install tqdm
                    from tqdm import tqdm
                    content_progress = tqdm(r.iter_content(), total=filesize)
                    for chunk in content_progress:
                        content_progress.set_description("Downloading wordlist")
                        filehandle.write(chunk) # Download them words
                except ImportError:
                    self.logger.info("'tdqm' failed to import; not showing progressbar.")
                    self.logger.info("Downloading wordlist...")
                    for chunk in r.iter_content():
                        filehandle.write(chunk) # Download them words
                self.logger.info("New wordlist saved to 'shiritori/%s'" % filename)
        with open(filename, 'r') as filehandle:
            # Make them words go naked and bend over
            wordlist = [word.strip().lower() for word in filehandle]

        # Filter out all them damned 's
        wordlist = list(filter(lambda x: "'s" not in x, wordlist))

        # Filter them ugly fat words longer than 30 characters, if any
        wordlist = list(filter(lambda x: len(x) < 30, wordlist))

        return wordlist # Bring 'em to me!!

class Dispatch(object):
    """ Adds the required Telegram handlers to run the game """
    def __init__(self, mod, updater):
        dp = updater.dispatcher

        shiritori_game = Shiritori(mod)
        dp.add_handler(CommandHandler("shiritori", shiritori_game.start_game, pass_args=True))
        dp.add_handler(CommandHandler("wordchain", shiritori_game.start_game, pass_args=True))
        mod.add_message_handler([Filters.text], shiritori_game.shiritori)

        mod.set_help("shiritori", shiritori_game.helptext)
