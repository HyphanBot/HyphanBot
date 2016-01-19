from nltk.corpus import words
from telegram import ParseMode
import threading
import random
import time

'''
Hyphan experimant: Shiritori/Word_Chain game module

TODO: Implement score system based on https://shiritorigame.com
	- Score starts at 100
	- Subtract the length of the word from the score in each turn
	- Optional: Subtract the remaining time from the score in each turn (Speed bonus)
	- The first player to get their score down to 0 wins the game
'''

global helptext

helptext = """
*Shiritori*, also known as *Word Chain*, is a game in which the players say a word that begins with the last letter of the previous word.
_Shiritori_ originated in Japan. The word "Shiritori" literally means "taking the end" according to [Wikipedia](https://en.wikipedia.org/wiki/Shiritori) (See also: [Word Chain](https://en.wikipedia.org/wiki/Word_chain)).

I can play this game. I'm currently hard to beat and I might use really long words, but I was just taught to not be fair... Sorry.
To start a match with me, type:
	`/shiritori start` or `/wordchain start`
"""

def dispatch(mod, updater):
	global started
	global timer
	global limit
	global lastword
	global used_words
	global uturn

	dp = updater.dispatcher

	timer = 30 # in seconds; remaining time.
	limit = 30 # in seconds; timer will always be set to this after the turn is over.
	started = False
	lastword = None
	used_words = []
	uturn = False # determines if it's the user's turn.

	def set_timer(bot, update):
		global started
		global uturn
		global timer
		global limit

		while started:
			if uturn:
				if not timer <= 0:
					timer = timer-1
					time.sleep(1)
				else:
					bot.sendMessage(chat_id=update.message.chat_id, text="Time's up! Game over.")
					started = False
			else:
				timer = limit
				time.sleep(0.1)

	def start_game(bot, update, args):
		global started
		global timer
		global limit

		if len(args) is 1 and args[0] == "start":
			started = True
			timer = limit
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

		uturn = False
		if word == None:
			# If there is no given user word (if the game was just started), choose a random word.
			response = random.choice(words.words())
		else:
			# Choose a random word that starts with the last letter of the user's word
			chosen_word = random.choice(list(filter(lambda x: x[0] == word[-1:], words.words())))
			while chosen_word in used_words:
				# As long as the word is used, keep chosing another word.
				# This prevents Hyphan from losing.
				chosen_word = random.choice(list(filter(lambda x: x[0] == word[-1:], words.words())))
			response = chosen_word
		lastword = response
		used_words.append(lastword)
		bot.sendMessage(chat_id=update.message.chat_id, text=response)
		uturn = True

	def shiritori(bot, update):
		global started
		global uturn
		global used_words
		global lastword

		message = update.message.text.lower()
		response = None

		if started and uturn:
			if message in words.words():
				if message.startswith(lastword[-1:]):
					if message not in used_words:
						used_words.append(message)
						pc_turn(bot, update, message)
					else:
						response = "'%s' was already used! Try again!" % message
				else:
					response = "'%s' does not start with '%s'. Try again!" % (message, lastword[-1:])
			else:
				response = "'%s' is not found in my word list! Try again!" % message

			if response is not None:
				bot.sendMessage(chat_id=update.message.chat_id, text=response)

	dp.addTelegramCommandHandler("shiritori", start_game)
	dp.addTelegramCommandHandler("wordchain", start_game)
	dp.addTelegramMessageHandler(shiritori)