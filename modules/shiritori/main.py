from nltk.corpus import words
from telegram import ParseMode
from tqdm import tqdm # Progress bar module. Install: pip install tqdm
from os import path
import threading
import random
import time
import requests
import logging

'''
Hyphan experimant: Shiritori/Word_Chain game module

TODO: Implement score system based on https://shiritorigame.com
	- Optional: Subtract the remaining time from the score in each turn (Speed bonus)
'''
global logger
global helptext

helptext = """
*Shiritori*, also known as *Word Chain*, is a game in which the players say a word that begins with the last letter of the previous word.
_Shiritori_ originated in Japan. The word "Shiritori" literally means "taking the end" according to [Wikipedia](https://en.wikipedia.org/wiki/Shiritori) (See also: [Word Chain](https://en.wikipedia.org/wiki/Word_chain)).

I can only play this game in English. I'm currently hard to beat and I might use really long words, but I was just taught to not be fair... Sorry.
To start a match with me, type:
	`/shiritori start` or `/wordchain start`
"""

logger = logging.getLogger(__name__)

def get_wordlist(url, filename="shiritori_wordlist.txt"):
	if not path.exists(filename):
		logger.info("Wordlist for shiritori not found; downloading new list. This can take a while...")
		r = requests.get(url, stream=True)
		filesize = len(r.content)
		with open(filename, 'wb') as filehandle:
			content_progress = tqdm(r.iter_content(), total=filesize)
			for chunk in content_progress:
				content_progress.set_description("Downloading wordlist")
				filehandle.write(chunk) # Download them words
		logger.info("New wordlist saved to 'shiritori/%s'" % filename)
	with open(filename, 'r') as filehandle:
		wordlist = [word.strip().lower() for word in filehandle] # Make them words go naked and bend over
	wordlist = list(filter(lambda x: "'s" not in x, wordlist)) # Filter out all them damned 's
	wordlist = list(filter(lambda x: len(x) < 30, wordlist)) # Filter them ugly fat words longer than 30 characters, if any
	return wordlist # Bring 'em to me!!

def dispatch(mod, updater):
	global started
	global timer
	global limit
	global lastword
	global used_words
	global uturn
	global score
	global pc_score
	global startscore
	global minlen
	global winmsg
	global losemsg
	global wordlist
	global gamechat

	dp = updater.dispatcher

	limit = mod.get_config("timelimit", 30) # The constant time limit for each turn in seconds (default: 30)
	timer = limit # Remaining time in seconds

	startscore = mod.get_config("startscore", 100) # The score at the beginning of the game (default: 100)
	score      = startscore # The user's score
	pc_score   = startscore # Hyphan's score

	minlen = mod.get_config("minimumlength", 3) # The minimum number of characters allowed (default: 3)

	# Message if user wins (default: "Senpai, tell me your secrets!")
	winmsg  = mod.get_config("winmessage", "Senpai, tell me your secrets!")

	# Message if user loses (default: "This was so predictable, hehe.")
	losemsg = mod.get_config("losemessage", "This was so predictable, hehe.")

	# Gets and downloads the wordlist if not already downloaded
	wordlist = get_wordlist(mod.get_config("wlurl", "http://nerdyserv.no-ip.org/hyphan/SCOWL-wl/words.txt"),
		mod.get_config("wlsavename", "shiritori_wordlist.txt"))

	started    = False
	lastword   = None
	used_words = []
	uturn      = False # determines if it's the user's turn.

	def set_timer(bot, update):
		global started
		global uturn
		global timer
		global limit
		global score
		global pc_score
		global gamechat

		while started:
			if uturn:
				if not timer <= 0:
					timer = timer-1
					time.sleep(1)
				else:
					comment = ""
					if pc_score < score:
						comment = "You knew I was gonna win, didn't you? You still lost, though."
					elif score < pc_score:
						comment = "You could've won, ya know."
					elif pc_score == score:
						comment = "Looks like was a tie, but you lost anyway."
					response = """
Time's up! Game over.
=======Scores=======
    Player: %s
    %s: %s
%s
""" % (score, bot.getMe().first_name, pc_score, comment)
					bot.sendMessage(chat_id=gamechat, text=response)
					started = False
			else:
				timer = limit
				time.sleep(0.1)

	def start_game(bot, update, args):
		global started
		global timer
		global limit
		global score
		global pc_score
		global startscore
		global gamechat

		if len(args) is 1 and args[0] == "start":
			started = True
			timer = limit
			score = startscore
			pc_score = startscore
			used_words = []
			gamechat = update.message.chat_id
			timerthread = threading.Thread(target=set_timer, args=(bot, update))
			timerthread.daemon = True
			timerthread.start()
			pc_turn(bot, update)
		else:
			bot.sendMessage(chat_id=update.message.chat_id, text=helptext, parse_mode=ParseMode.MARKDOWN)

	def pc_turn(bot, update, word=None):
		global uturn
		global used_words
		global lastword
		global pc_score
		global score
		global minlen
		global losemsg
		global started
		global gamechat

		uturn = False
		if word == None:
			# If there is no given user word (if the game was just started), choose a random word.
			response = random.choice(wordlist)
		else:
			# Choose a random word that starts with the last letter of the user's word
			chosen_word = random.choice(list(filter(lambda x: x[0] == word[-1:], wordlist)))
			while (chosen_word in used_words) or (len(chosen_word) == 1):
				# As long as the word is used or is one letter, keep chosing another word.
				# This prevents Hyphan from losing.
				chosen_word = random.choice(list(filter(lambda x: x[0] == word[-1:], wordlist)))
			pc_score = pc_score - (len(chosen_word) - minlen)
			response = chosen_word
		lastword = response
		used_words.append(lastword)
		bot.sendMessage(chat_id=gamechat, text=response)
		if pc_score <= 0:
			started = False
			response = """
I win!!! You lost.
======Scores======
    Player: %s
    %s: 0 (real score: %s)
%s
""" % (score, bot.getMe().first_name, pc_score, losemsg)
			bot.sendMessage(chat_id=gamechat, text=response)
		else:
			uturn = True

	def shiritori(bot, update):
		global started
		global uturn
		global used_words
		global lastword
		global minlen
		global pc_score
		global score
		global winmsg
		global gamechat

		currentchat = update.message.chat_id
		message = update.message.text.lower()
		response = None

		if (started and uturn) and gamechat == currentchat:
			valid_word = True

			if message not in wordlist:
				response = "'%s' is not found in my word list! Try again!" % message
				valid_word = False
			if not message.startswith(lastword[-1:]):
				response = "'%s' does not start with '%s'. Try again!" % (message, lastword[-1:])
				valid_word = False
			if len(message) == 1:
				response = "Cannot be a letter, has to be a word. Try again!"
				valid_word = False
			if message in used_words:
				response = "'%s' was already used! Try again!" % message
				valid_word = False

			if valid_word:
				used_words.append(message)
				score = score - (len(message) - minlen)
				pc_turn(bot, update, message)

			if score <= 0:
				started = False
				response = """
You win!!!
==Scores==
 Player: 0 (real score: %s)
 %s: %s
%s
""" % (score, bot.getMe().first_name, pc_score, winmsg)

			if response is not None:
				bot.sendMessage(chat_id=gamechat, text=response)

	dp.addTelegramCommandHandler("shiritori", start_game)
	dp.addTelegramCommandHandler("wordchain", start_game)
	dp.addTelegramMessageHandler(shiritori)
