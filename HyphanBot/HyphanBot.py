# Import modules for use in hyphan
import sys
import os
import telegram
import time
import urllib
import duckduckgo
import pickle
import random
import bashquotes
import requests
import subprocess
import praw # Python Reddit API Wrapper
import xkcd
import urbandict

from uptime import uptime
from hackernews import HackerNews
from html.parser import HTMLParser

def main():
    # make the variables so they can be used in different functions then he one they got their
    # value assigned in
    global isRecovered
    global botName
    global latestUpdateId

    global nicknames
    global quotes
    global registry

    global announceTimer
    global announceStart

    global photocmd
    global popocmd

    # ed
    global ed
    global messagemode
    global foobar
    global editedtext
    global chatided

    # Pokeman
    global pokeman
    global hp
    global dexterity
    global enemy_hp
    global enemy_dexterity
    global nameChoice
    global attackChoice
    global battleMode
    global fightMode

    global r
    global oldtitle
    global oldchatid
    global oldmessage
    global doubledot
    global counter
    
    # foo
    oldtitle = ""
    oldchatid = ""
    oldmessage = ""
    doubledot = 0
    counter = 0
    
    # set the bot name
    botName = "Hyphan"

    # ed
    ed = False
    foobar = False
    message = ""
    
    # create an empty array for nicknames
    nicknames = {}

    # same but for quotes
    quotes = {}

    # Registry for chat IDs
    registry = {}

    # authenticate as hyphan to the telegram bot API
    bot = telegram.Bot(token='136008664:AAE2zBk8l1A4OZPQ5ebYxH1h_pVDMCtvUFo')

    # start the reddit module
    r = praw.Reddit(user_agent="HyphanBot")

    # print a message for debugging
    print("Initialized "+ botName +"Bot.")

    # Try to use the latest ID
    try:
        latestUpdateId = bot.getUpdates()[-1].update_id
    except IndexError:
        latestUpdateId = None

    # auto-restart from a crash
    if (len(sys.argv) > 1) and (str(sys.argv[1]) == "recover"):
        print("Recovered from a crash.")
        isRecovered = True
        #bot.sendMessage(chat_id=bot.getUpdates(offset=latestUpdateId)[-1].message.chat_id, text="I either recovered from a crash or just restarted, sorry if I crashed...")
    else:
        # in case this happens check if hell froze over.
        isRecovered = False

    # create the variables for the announce functiosn
    announceTimer = 0
    announceStart = False

    # create the variables for the photo functions (one specific to DBZ character)
    photocmd = False
    popocmd = False

    pokeman = False
    nameChoice = ""
    attackChoice = ""
    battleMode = False
    fightMode = False

    while True:
        getMsg(bot)
        time.sleep(1)

# get the command someone send to use
def cmd(command, message):
    global botName
    return (message.startswith((b'/' + command).decode('utf-8').lower().encode('utf-8'))) or (message.startswith((b'' + command).decode('utf-8').lower().encode('utf-8'))) or (message.startswith(b'@'+ botName.encode('utf-8') +b'Bot ' + command))

# set the various ways to interact with python
def cmdLen(command, message):
    # get the bot name
    global botName
    # a normal command
    if message.startswith(b'/' + command):
        return len("/" + command.decode('utf-8'))
    #  just plain text
    elif message.startswith(b'' + command):
        return len(command.decode('utf-8'))
    # in case you address him directly
    elif message.startswith(b'@HyphanBot ' + command):
        return len("@"+botName+"Bot " + command.decode('utf-8'))

# get the nicknames
def getNickname(firstname):
    global nicknames
    # load the nick name file
    with open("nicknames", 'rb') as nns:
        userNicknames = pickle.loads(nns.read())
        nicknames = userNicknames
    # if it's not the username return the nickname
    if not firstname in nicknames:
        return firstname
    # return the nickname
    return nicknames[firstname]

# remove a nickname
def delNickname(firstname):
    global nicknames
    del nicknames[firstname]
    with open("nicknames", 'wb') as nns:
        pickle.dump(nicknames, nns)

# set someone nickname
def setNickname(firstname, nickname):
    global nicknames
    # put the nickname into a file
    nicknames[firstname] = nickname
    with open("nicknames", 'wb') as nns:
        pickle.dump(nicknames, nns)

# get the chat id from the shortname
def getRegistry(shortname):
    global registry
    with open("database", 'rb') as db:
        databaseFile = pickle.loads(db.read())
        registry = databaseFile
    if not shortname in registry:
        return False
    return registry[shortname]

# get the shortname from the chat id
def getShortChatName(chatid):
    global registry
    if os.path.isfile("database"):
        with open("database", 'rb') as db:
            databaseFile = pickle.loads(db.read())
            registry = databaseFile
    returned = False
    for shortname, chatidIter in registry.items():
        if chatidIter == chatid:
            returned = shortname
    return returned

# add key to registry
def addRegKey(shortname, chatid):
    global registry
    if os.path.isfile("database"):
        with open("database", 'rb') as db:
            databaseFile = pickle.loads(db.read())
            registry = databaseFile
    if not shortname in registry:
        registry[shortname] = chatid
        with open("database", 'wb') as db:
            pickle.dump(registry, db)
        return True
    else:
        return False

# get a quote based on an identifier
def getQuote(quoteId):
    global quotes
    # open a file and read the quotes from it
    with open("quotes", 'rb') as qts:
        userquotes = pickle.loads(qts.read())
        quotes = userquotes
    # if you cannot find a quote with that ID return an error
    if not quoteId in quotes:
        return "Sorry, I cannot find the quote with id of '" + quoteId + "'. You can try creating it by typing: \n/quote add " + quoteId + " q=<QuoteText>"
    return '"'+quotes[quoteId]+'"'

# send a random quote
def randQuote():
    global quotes
    with open("quotes", 'rb') as qts:
        userquotes = pickle.loads(qts.read())
        quotes = userquotes
    # pick a random quote from the file
    randKey = random.choice(list(quotes.keys()))
    return '"'+quotes[randKey]+'" ('+randKey+')'

# add a quote
def setQuote(quoteId, quoteStr):
    global quotes
    # write a quote to the file
    quotes[quoteId] = quoteStr
    with open("quotes", 'wb') as qts:
        pickle.dump(quotes, qts)

# remove a quote
def delQuote(quoteId):
    global quotes
    del quotes[quoteId]
    with open("quotes", 'wb') as qts:
        pickle.dump(quotes, qts)

# create a random person
def getRandomUser(field='name'):
    # a link to site that generates the user
    url = "http://nerdyserv.no-ip.org/random-backend.php?for=usr"
    genseed = requests.get(url+"&prop=seed").text

    # get the name of the person from the generated seed
    content = requests.get(url+"&prop="+field+"&filter=seed-"+genseed).text

    # generate the site with further, random, information on the user
    seedurl = "http://nerdyserv.no-ip.org/random.html?for=usr&filter=seed-"+genseed+""
    print(content)
    print(seedurl)
    return "" + content + "\n" + seedurl

def getMsg(bot):
    global isRecovered
    global botName
    global latestUpdateId
    
    global announceToChatId
    global announceTime
    global announceTimer
    global announceStr
    global announceStart

    global photoToChatId
    global photocmd

    global popocmd

    # ed
    global ed
    global messagemode
    global foobar
    global editedtext
    global chatided
    
    global nameChoice
    global attackChoice
    global battleMode
    global fightMode

    global r
    global oldtitle
    global oldchatid
    global oldmessage
    global doubledot
    global counter
    
    # a simple recursive function to repeats a message X amounts of time.
    if announceStart:
        if announceTimer == 0:
            bot.sendMessage(chat_id=announceToChatId, text="{}".format(announceStr))
            print("Announced ", announceStr)
            announceTimer = announceTime
        announceTimer = announceTimer - 1

    for update in bot.getUpdates(offset=latestUpdateId):
        if latestUpdateId < update.update_id:
            # use the id of the last use chat. This usually means the chat hyphan got
            # called from
            chatId = update.message.chat_id
            
            # make the msg readable
            msg = update.message.text.encode('utf-8')
            message = msg.decode("utf-8")

            print(update)
            if oldtitle != update.message.chat.title and len(oldtitle) != 0 and chatId == oldchatid:
                bot.sendMessage(chat_id=chatId, text="Why did you change the name to {}, eh.".format(update.message.chat.title))

            oldtitle = update.message.chat.title
            oldchatid = chatId
            
            # sillyness
            foo = len(message) - 3
            bar = len(message) - 2
            if message[foo:] != "..." and message[bar:] == ".." and len(message) > 2 and oldmessage != message and doubledot < 3:
                bot.sendMessage(chat_id=chatId, text="Three dots Nick")
                global doubledot
                doubledot += 1

            if counter == 100:
                counter = 0
                doubledot = 0
            else:
                counter += 1
            
            print(doubledot)
            oldmessage = message
            # get the name, firstname and nickname of the user
            user = update.message.from_user.username
            firstname = update.message.from_user.first_name
            nickname = getNickname(firstname)

            # if photocmd is set either send a photo or sticker
            if photocmd:
                if update.message.photo:
                    print(update.message.photo)
                    bot.sendPhoto(chat_id=photoToChatId, photo=update.message.photo[-1].file_id)
                    photocmd = False
                    
                elif update.message.sticker:
                    print(update.message.sticker)
                    bot.sendSticker(chat_id=photoToChatId, sticker=update.message.sticker.file_id)
                    photocmd = False

            if (msg):
                debug = "[{0}] {1} ({2}, {3}): {4}".format(chatId, firstname, nickname, user, message)
                print(debug)
               # darude sandstorm
                darude = random.randint(1, 1000)
                if darude == 743:
                    bot.sendMessage(chat_id=chatId, text="https://www.youtube.com/watch?v=y6120QOlsfU")

                # An easter egg for long uptime
                calculation = uptime() / 60 / 60 / 24

                if int(str(calculation)[:1]) == 7:
                    bot.sendMessage(chat_id=chatId, text="https://www.youtube.com/watch?v=SYRlTISvjww")
                
                # if the command is popo send a photo
                if ("popo" in msg.decode('utf-8').lower()):
                    bot.sendPhoto(chat_id=chatId, photo="http://img08.deviantart.net/e3f9/i/2010/254/f/1/mr__popo__s_deadly_eyes_by_khmaivietboi-d2yjspi.jpg")
                    bot.sendMessage(chat_id=chatId, text="HIII!!")
                    popocmd = True

                # Error handler
                if ("syntax error" in msg.decode('utf-8').lower()):
                    bot.sendMessage(chat_id=chatId, text="Syntax error")

                # return nothing
                if cmd(b'help', msg):
                    global pokeman
                    global chatided
                    global battleMode
                    global hp
                    global dexterity
                    global enemy_hp
                    global enemy_dexterity
                    
                    if not popocmd:
                        egg = 42
                        if egg == 42:
                            pokeman = True
                            chatided = chatId
                            battleMode = True
                            hp = 20
                            dexterity = 40
                            enemy_hp = 25
                            enemy_dexterity = 30

                            randNames = ["HYPHAN", "PIKACHU", "NERD", "BOT"]
                            nameChoiceNum = random.randint(0, len(randNames) - 1)
                            nameChoice = randNames[nameChoiceNum]
                            bot.sendMessage(chat_id=chatId, text="Wild {} appeared!".format(nameChoice))
                            bot.sendMessage(chat_id=chatId, text="Go, {}!".format(firstname.upper()))
                            bot.sendMessage(chat_id=chatId, text="What will {} do?\n /FIGHT /PKMN\n /ITEMS /RUN".format(firstname.upper()))
                        else:
                            bot.sendMessage(chat_id=chatId, text="?")
                    popocmd = False

                if pokeman == True and chatId == chatided:
                    global run
                    run = True
                    lowmessage = message.lower()
                    if fightMode == True:
                        if len(lowmessage.split()) != 1:
                            bot.sendMessage(chat_id=chatId, text="That is not a valid command")
                            run = False
                            
                        elif lowmessage == "scratch":
                            result = random.randint(0,5)
                            dexterity = dexterity - 3
                            
                            if result == 5:
                                effectiveness = "It was super effective!"
                            elif result >= 4:
                                effectiveness = "Critical hit!"
                            elif result <= 1:
                                effectiveness = "It's not very effective..."
                            else:
                                effectiveness = "It's mediocre, just like your mom"
                                
                        elif lowmessage == "punch" or lowmessage == "pnch":
                            result = random.randint(0,10)
                            dexterity = dexterity - 6

                            if result == 10:
                                effectiveness = "It was super effective!"
                            elif result >= 8:
                                effectiveness = "Critical hit!"
                            elif result <= 2:
                                effectiveness = "It's not very effective..."
                            else:
                                effectiveness = "It's mediocre, just like your mom"

                        elif lowmessage == "kick":
                            result = random.randint(7,10)
                            dexterity = dexterity - 10
                            
                            if result == 12:
                                effectiveness = "It was super effective!"
                            elif result >= 10:
                                effectiveness = "Critical hit!"
                            else:
                                effectiveness = "It's mediocre, just like your mom"

                        elif lowmessage == "jump":
                            result = 0
                            dexterity = dexterity - 1
                            effectiveness = "Not at all"

                        else:
                            bot.sendMessage(chat_id=chatId, text="Your pokemon doesn't know that move!")
                            run = False
                            
                        if run == True:
                            bot.sendMessage(chat_id=chatId, text="{0} used {1}!".format(firstname.upper(), lowmessage.upper()))
                            bot.sendMessage(chat_id=chatId, text=effectiveness)
                        
                            enemy_hp = enemy_hp - result
                            bot.sendMessage(chat_id=chatId, text="{0} took {1} HP damage! He has {2} HP left!".format(nameChoice.upper(), result, enemy_hp))

                            if enemy_hp <= 0:
                                bot.sendMessage(chat_id=chatId, text="{} fainted!".format(nameChoice.upper()))
                                fightMode = False
                                pokeman = False
                            else:
                                bot.sendMessage(chat_id=chatId, text="This is going to do something!")
                                randAttacks = ["scratch", "watercannon", "harden", "tackle"]
                                randChoose = random.randint(0, len(randAttacks) - 1)
                                
                                if randAttacks[randChoose] == "scratch":
                                    result = random.randint(0,5)
                                    enemy_dexterity = enemy_dexterity - 3

                                    if result == 5:
                                        effectiveness = "it was super effextive!"
                                    elif result >= 4:
                                        effectiveness = "Critical hit!"
                                    elif result <= 1:
                                        effectiveness = "It's not very effective..."
                                    else:
                                        effectiveness = "It's mediocre, just like your mom"
                                        
                                elif randAttacks[randChoose] == "watercannon":
                                    result = random.randint(7,15)
                                    enemy_dexterity = enemy_dexterity - 15
                                    
                                    if result == 12:
                                        effectiveness = "It was super effective!"
                                    elif result == 11:
                                        effectiveness = "Critical hit!"
                                    elif result <= 8:
                                        effectiveness = "It's not very effective"
                                    else:
                                        effectiveness = "It's mediocre, just like your mom"

                                elif randAttacks[randChoose] == "harden":
                                    result = 0
                                    enemy_dexterity = enemy_dexterity - 1

                                    effectiveness = "Honestly what did you expect to happen?"

                                elif randAttacks[randChoose] == "tackle":
                                    result = random.randint(0,10)
                                    enemy_dexterity = enemy_dexterity - 6

                                    if result == 10:
                                        effectiveness = "It was super effective!"
                                    elif result >= 8:
                                        effectiveness = "Critical hit!"
                                    elif result <= 2:
                                        effectiveness = "It's not very effective..."
                                    else:
                                        effectiveness = "It's mediocre, just like your mom"
                                else:
                                    bot.sendMessage(chat_id=chatId, text="Something went horribly wrong...")

                                    bot.sendMessage(chat_id=chatId, text="{0} used {1}!".format(nameChoice, randAttacks[randChoose].upper()))
                                    bot.sendMessage(chat_id=chatId, text=effectiveness)
                                    
                                    hp = hp - result
                                    bot.sendMessage(chat_id=chatId, text="{0} took {1} HP damage! He has {2} HP left!".format(firstname.upper(), result, hp))

                                    if hp <= 0:
                                        bot.sendMessage(chat_id=chatId, text="Game over!")
                                        fightMode = False
                                        pokeman = False
                                
                    elif lowmessage == "fight":
                        bot.sendMessage(chat_id=chatId, text="SCRATCH\nPNCH\nKICK\nJUMP")
                        fightMode = True

                    elif lowmessage == "run":
                        bot.sendMessage(chat_id=chatId, text="Got away safely!")
                        pokeman = False

                    elif lowmessage == "items":
                        bot.sendMessage(chat_id=chatId, text="You have no items")

                    elif lowmessage == "pkmn" or lowmessage == "pokemon":
                        bot.sendMessage(chat_id=chatId, text="You don't have any other pokemans")

                    else:
                        bot.sendMessage(chat_id=chatId, text="*BEEP*")
                        
                # enable ed mode and initialize the various ed modes
                elif cmd(b'ed', msg):
                    global editedtext
                    global messagemode
                    global foobar
                    global chatided
                    global ed

                    # make sure that ed only is ed in one chat
                    chatided = chatId
                    editedtext = ""
                    messagemode = False
                    foobar = False
                    ed = True

                elif ed == True and chatId == chatided:
                    # enter into command mode
                    if message == "P":
                        foobar = True
                        if chatId == chatided:
                            bot.sendMessage(chat_id=chatided, text="*")
                        
                    elif messagemode == True:
                        # stop the text input
                        if message == ".":
                            messagemode = False
                        else:
                            editedtext = editedtext + '\n' + message
                            
                    elif foobar == True:
                        # quit ed
                        if message == "q":
                            foobar = False
                            ed = False
                            
                        elif message == "p" or message == ".p":
                            temp = ""
                            # split the text into lines
                            splittext = editedtext.split('\n')

                            for x in splittext:
                                # show the last line
                                if len(splittext) == len(temp) - 1:
                                    temp = temp + x
                                else:
                                    lastline = x
                                    
                            if chatId == chatided:
                                bot.sendMessage(chat_id=chatided, text=lastline)

                        elif message == "1,$p" or message == ",p":
                            if chatId == chatided:
                                bot.sendMessage(chat_id=chatided, text=editedtext)

                        elif message[1:2] == "p" and message[:1].isdigit():
                            splittext = editedtext.split('\n')
                            temp = ""
                            
                            for x in splittext:
                                if temp == "":
                                    temp = x
                                    line = x

                                # adjust for the difference in counting
                                elif len(temp.split('\n')) == int(message[:1]) - 1:
                                    line = x
                                    temp = temp + '\n' + x
                                    
                                else:
                                    temp = x + '\n' + temp

                            # if the line number higher is then possible respond with ?
                            if int(message[:1]) + 1 > len(splittext):
                                line = "?"

                            if chatId == chatided:
                                bot.sendMessage(chat_id=chatided, text=line)

                        # enable messagemode
                        elif message[:1] == "i":
                            messagemode = True

                        else:
                            if chatId == chatided:
                                bot.sendMessage(chat_id=chatided, text="?")

                    else:
                        if chatId == chatided:
                            bot.sendMessage(chat_id=chatided, text="?")
                    
                # send an about message if someone ask for it
                elif cmd(b'about', msg):
                    if not popocmd:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        time.sleep(1)
                        bot.sendMessage(chat_id=chatId, text="I am King "+botName+", ruler of the northern part of the galaxy.")
                    popocmd = False

                # send a duckduckgo search with a specified keyword
                elif cmd(b'ddg', msg):
                    arg1 = msg[cmdLen(b'ddg', msg)+1:].decode("utf-8")
                    args = arg1.split()
                    
                    bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                    
                    if len(args) == 0 or len(args) == 1:
                        bot.sendMessage(chat_id=chatId, text="For zero click info use '/ddg zci <keyword>'\nAnd for a link use '/ddg search <keyword>'\nOr to ask a question use '/ddg ask <question>'")
                    
                    elif args[0] == "search":
                        # split the arguments into a list with spaces using the special web character for space
                        arguments = '%20'.join(args[1:])
                        bot.sendMessage(chat_id=chatId, text="Here you go {0}: https://duckduckgo.com/?q={1}".format(nickname, arguments))
                    
                    elif args[0] == "zci":
                        arguments = ' '.join(args[1:])
                        # get the search result from duckduckgo using Zero Click Info
                        searchResult = duckduckgo.get_zci(arguments)
                        bot.sendMessage(chat_id=chatId, text="{0}, here is what I can gather about {1}:\n\n{2}".format(nickname, arguments, searchResult))

                    elif args[0] == "ask":
                        arguments = ' '.join(args[1:])
                        # get the answer from duckduckgo
                        searchResult = duckduckgo.query(arguments)

                        if len(searchResult.answer.text) == 0:
                            bot.sendMessage(chat_id=chatId, text="Sorry {}, I don't know how to answer that...".format(nickname))
                        else:
                            bot.sendMessage(chat_id=chatId, text="{0}, here is what I can find out about {1}:\n{2}".format(nickname, arguments, searchResult.answer.text))
                            
                    else:
                        bot.sendMessage(chat_id=chatId, text="{} is no space station, it's an unvalid command!".format(args[0]))
            
                # Registers a chat id with a username or, if used in a group chat, a short name.
                elif cmd(b'register', msg):
                    popocmd = False
                    arg1 = msg[cmdLen(b'register', msg)+1:].decode("utf-8")

                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        if chatId < 0: # If the chat ID is less than 0 (aka negative number), it's a group chat, otherwise it's not.
                            if getShortChatName(chatId):
                                message = "This group chat is already registered under {}. You could register another group chat, or even yourself, by using the following commands:\n For other group chats: /register <shortname>\n For private chat (with me): /register".format(getShortChatName(chatId))
                                bot.sendMessage(chat_id=chatId, text=message)
                            else:
                                bot.sendMessage(chat_id=chatId, text="This is a group chat. What name do you want me to register it under? No spaces please! Format:\n /register <shortname>")
                        else:
                            if addRegKey(user, chatId):
                                bot.sendMessage(chat_id=chatId, text="Registered chat with '"+user+"' (your username).")
                            else:
                                bot.sendMessage(chat_id=chatId, text="This chat is already registered with your username ("+user+").")
                    else:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        if chatId < 0:
                            args = arg1.split(" ") # To insure that no spaces will be registered
                            if not getShortChatName(chatId) and addRegKey(args[0], chatId):
                                message = "Registered group chat with {}.".format(args[0])
                                bot.sendMessage(chat_id=chatId, text=message)
                            else:
                                if not getShortChatName(chatId):
                                    message = "This shortname {} is already registered to another chat".format(args[0])
                                    bot.sendMessage(chat_id=chatId, text=message)
                                else:
                                    message = "This group chat is already registered as {}.".format(getShortChatName(chatId))
                                    bot.sendMessage(chat_id=chatId, text=message)
                    
                # To test the register command.
                elif cmd(b'chatid', msg):
                    popocmd = False
                    arg1 = msg[cmdLen(b'chatid', msg)+1:].decode("utf-8")
                    
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        # This is more of an informational message than an error.
                        bot.sendMessage(chat_id=chatId, text="The ID for this chat is: "+str(chatId)+"\nWhich chat ID do you want me to look up? Format:\n/chatid <shortname>")
                    else:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        requestedChatId = getRegistry(arg1)
                        if requestedChatId:
                            bot.sendMessage(chat_id=chatId, text="The registered chat ID for '"+arg1+"' is: "+str(requestedChatId))
                        else:
                            bot.sendMessage(chat_id=chatId, text="There is no registered chat ID assosiated with this name.\nTo register a chat with me under this name, use one of the folowing commands:\nIn private chat: /register\nIn group chats: /register "+arg1)

                # Send a private message to someone through Hyphan.
                elif cmd(b'pm', msg):
                    popocmd = False
                    arg1 = msg[cmdLen(b'pm', msg)+1:].decode("utf-8")
                    
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="Who do you want me to send a message to? Format:\n/pm <username> <message>")
                    else:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        args = arg1.split(" ")
                        if len(args) == 1:
                            if getRegistry(args[0]):
                                bot.sendMessage(chat_id=chatId, text="What message do you want me to send to "+args[0]+"? Format:\n/pm "+args[0]+" <message>")
                            else:
                                bot.sendMessage(chat_id=chatId, text="Sorry to tell you this, but the user you're trying to send a message to is not registered with me.\nWho else do you want me to send a message to? Format:\n/pm <username> <message>")
                        else:
                            recipientId = getRegistry(args[0])
                            if recipientId:
                                if recipientId > 0:
                                    unsorted = args[1:]
                                    pmsg = ""
                                    for x in unsorted:
                                        pmsg = pmsg + " " + x
                                    bot.sendMessage(chat_id=recipientId, text="PM from "+update.message.from_user.first_name+" ("+user+"):\n" + pmsg + "\n[To reply to this message, use: /pm "+user+" <your reply> ]")
                                else:
                                    bot.sendMessage(chat_id=chatId, text="Sorry, I can't send a private message to a group.")
                            else:
                                bot.sendMessage(chat_id=chatId, text="Sorry to tell you this, but the user you're trying to send a message to is not registered with me.")

                elif cmd(b'nickname', msg):
                    arg1 = msg[cmdLen(b'nickname', msg)+1:].decode("utf-8")
                    args = arg1.split()

                    bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)

                    message = """
                    This is Hyphan's nickname function! The following things are possible
                    callme <nickname> | give yourself a new nickname
                    nonick            | remove the nickname
                    whoami            | check which nickname you have"""
                    
                    if len(args) == 0:
                        bot.sendMessage(chat_id=chatId, text=message)

                    elif args[0] == "callme":
                        if len(args) == 1:
                            bot.sendMessage(chat_id=chatId, text="What do you want me to call you, {}".format(nickname))
                        else:
                            # turn the arguments in to a string with spaces inbetween
                            name = ' '.join(args[1:])
                            
                            # set the nickname
                            setNickname(firstname, name)
                            
                            # get the nickname from their first name.
                            nickname = getNickname(firstname)
                            
                            bot.sendMessage(chat_id=chatId, text="From now on, I'll start calling you {}.".format(nickname))

                    # tell them their name
                    elif args[0] == "whoami":
                            bot.sendMessage(chat_id=chatId, text="Your name is {}.".format(nickname))
                    
                    elif args[0] == "nonick":
                        if nickname == firstname:
                            # send a message if no nickname is set
                            bot.sendMessage(chat_id=chatId, text="I'm already using your real name aren't I?\nYou could give me another thing to call you with the '/nickname callme <nickname>' command.")
                        else:
                            # remove their nickname
                            delNickname(firstname)
                            
                            bot.sendMessage(chat_id=chatId, text="You've returned back to your first name, {}.".format(firstname))
                            
                    else:
                        bot.sendMessage(chat_id=chatId, text="{} is not a valid command".format(args[0]))

                # scoobie, oobie, doobie, scoobie, doobie melody
                elif cmd(b'scat', msg) or cmd(b'scatman', msg):
                    message = "Hyphan is the scatman!\nhttps://www.youtube.com/watch?v=y6oXW_YiV6g"
                    bot.sendMessage(chat_id=chatId, text=message)

                # Return a random shitty song made by Europeans
                elif cmd(b'eurodance', msg):
                    # make a database of songs
                    eurodance = ["https://www.youtube.com/watch?v=y6oXW_YiV6g", "https://www.youtube.com/watch?v=zA52uNzx7Y4", "https://www.youtube.com/watch?v=s9YbICd43Mc", "https://www.youtube.com/watch?v=boNRVXR7bqg", "https://www.youtube.com/watch?v=ZyhrYis509A", "https://www.youtube.com/watch?v=VcDy8HEg1QY"]

                    euroReply = random.randint(0, len(eurodance) - 1)

                    bot.sendMessage(chat_id=chatId, text=eurodance[euroReply])

                # create a magical 8-ball 
                elif cmd(b'magic8', msg) or cmd(b'8', msg):
                    # run the command both if someone uses /magic8 or /8
                    if cmd(b'magic8', msg):
                        arg1 = msg[cmdLen(b'magic8', msg)+1:].decode("utf-8")
                    else:
                        arg1 = msg[cmdLen(b'8', msg)+1:].decode("utf-8")

                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="Ask anything and I shall answer.")
                    else:
                        if not popocmd:
                            # reject the command if it's from someone who cannot be trusted
                            if user == "DeadManDying":
                                bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                                bot.sendMessage(chat_id=chatId, text="Go suck a duck, Maxi.")
                            else:
                                bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                                # make a database of the possible answers
                                magicMsgs = ["It is certain"," It is decidedly so","Without a doubt","Yes definitely","You may rely on it","As I see it yes","Most likely","Outlook good","Yes","Signs point to yes","Reply hazy try again","Ask again later","Better not tell you now","Cannot predict now","Concentrate and ask again","Don't count on it","My reply is no","God says no","Very doubtful","Outlook not so good"]

                                # pick a random answer from the list
                                magicReply = random.randint(0,len(magicMsgs) - 1)

                                # send the answers
                                bot.sendMessage(chat_id=chatId, text=magicMsgs[magicReply])
                    popocmd = False

                # wait for 5 seconds and repeat a string
                elif cmd(b'wait5andsay', msg):
                    arg1 = msg[cmdLen(b'wait5andsay', msg)+1:].decode("utf-8")
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="What do you want me to say after 5 seconds?")
                    elif user == "DeadManDying":
                        bot.sendChatAction(chat_id=ChatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="Bad Maxi bad!")
                    else:
                        if not popocmd:
                            # wait for five seconds
                            time.sleep(5)
                            bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                            bot.sendMessage(chat_id=chatId, text="" + arg1 + "")
                    popocmd = False

                # repeat a string in the chat every 20 seconds
                elif cmd(b'announce', msg):
                    arg1 = msg[cmdLen(b'announce', msg)+1:].decode("utf-8")
                    args = arg1.split()
                    
                    if len(args) == 0:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="What do you want me to announce? Format:\n /announce <timeInSeconds> <announcement>")
                        
                    elif args[0] == "stop":
                        # disable the announcing
                        announceStart = False
                        bot.sendMessage(chat_id=chatId, text="Will stop announcing {} in this chat.".format(announceStr))
                        
                    elif user == "DeadManDying":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="Bad Maxi bad!")
                    else:
                        announceToChatId = chatId # ensure that it will always be set to the same chat

                        # if the first argument is a digit use it as time between each message
                        if args[0].isdigit():
                            announceTime = int(args[0])
                            announceStr = ' '.join(args[1:]) # make list into a string with spaces

                        else:
                            announceTime = 20
                            announceStr = ' '.join(args[0:])

                        # set the announcing
                        announceStart = True
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)

                        bot.sendMessage(chat_id=chatId, text="Will announce {0} in this chat every {1} seconds.".format(announceStr, str(announceTime)))
                    popocmd = False

                # pick one of a list of choices
                elif cmd(b'choose', msg):
                    arg1 = msg[cmdLen(b'choose', msg)+1:].decode("utf-8")

                    # split the argument in multiple words
                    args = arg1.split(" ")
                    # if either the first or the third word is empty or the second word
                    # isn't or return an error.
                    if args[0] == "" or args[1] != "or" or args[2] == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="What do you want me to choose? The format is like this:\n/choose <thing1> or <thing2>")
                    else:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        possibilities = []
                        for x in range(0, len(args)):
                            if x % 2 == 0:
                                possibilities.append(args[x])
                        choice = random.randint(0,len(possibilities) - 1)
                        if not popocmd:
                            bot.sendMessage(chat_id=chatId, text=""+possibilities[choice]+"")
                        else:
                            bot.sendMessage(chat_id=chatId, text="Lord Popo.")
                    popocmd = False

                # find a quote in the database
                elif cmd(b'quote', msg):
                    arg1 = msg[cmdLen(b'quote', msg)+1:].decode("utf-8")
                    arg2 = msg[cmdLen(b'quote', msg)+1+len(arg1)+1:].decode("utf-8")
                    arg3 = msg[cmdLen(b'quote', msg)+1+len(arg1)+1+len(arg2)+1:].decode("utf-8")

                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="What quote do you want me to find or add? Possible formats:\n/quote <QuoteIdentifier>\n/quote add <QuoteIdentifier> q=<QuoteText>\n/quote random")
                    # try to add one if the keyword add is added
                    elif arg1.startswith("add"):
                    	if arg1[4:] == "":
                    		bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                    		bot.sendMessage(chat_id=chatId, text="What quote do you want me to add? Format:\n/quote add <QuoteIdentifier> q=<QuoteText>")
                    	else:
                                # split the word starting with q= from they command
                    		addargs = arg1[4:].split(" q=")
                    		if not addargs[1]:
                    			bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                    			bot.sendMessage(chat_id=chatId, text="What quote do you want me to add? Format:\n/quote add "+arg2+" q=<QuoteText>")
                    		else:
                                        # if q= exists, run the setQuote on the id and the actual quote. 
                    			setQuote(addargs[0], addargs[1])
                    			bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                    			bot.sendMessage(chat_id=chatId, text="Added quote with id of '"+addargs[0]+"'.")

                    # if the keyword random is giving return a random quote

                    elif arg1.startswith("random"):
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text=randQuote())
                        
                    else:
                        # if none of the above are true return the quote with the it
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text=getQuote(arg1))
                    popocmd = False
                    
                # get xkcd comic!!
                elif cmd(b'xkcd', msg):
                    arg1 = msg[cmdLen(b'xkcd', msg)+1:].decode("utf-8")
                    args = arg1.split(" ")
                    bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                    helpMsg = "What xkcd comic do you want me to display? Formats:\n /xkcd <comicNumber>\n /xkcd latest\n /xkcd random\n /xkcd explain <comicNumber/latest/random>"
                    message = "Weird error."
                    comic = None
                    showComic = True
                    if len(args) == 0:
                        message = helpMsg
                    elif len(args) == 1:
                        if args[0].isdigit():
                            comic = xkcd.getComic(int(args[0]))
                        elif args[0] == "latest":
                            comic = xkcd.getLatestComic()
                        elif args[0] == "random":
                            comic = xkcd.getRandomComic()
                        else:
                            showComic = False
                        message = ("{0}\n {1}\n '{2}'".format(comic.getTitle(), comic.getImageLink(), comic.getAltText())) if showComic else (helpMsg)
                    elif len(args) == 2:
                        if args[0] == "explain":
                            if args[1].isdigit():
                                comic = xkcd.getComic(int(args[1]))
                            elif args[1] == "latest":
                                comic = xkcd.getLatestComic()
                            elif args[1] == "random":
                                comic = xkcd.getRandomComic()
                            else:
                                showComic = False
                        else:
                            showComic = False
                        message = ("Here is the explanation for the '{0}' comic:\n {1}".format(comic.getTitle(), comic.getExplanation())) if showComic else ("Invalid argument.\n {}".format(helpMsg))
                    bot.sendMessage(chat_id=chatId, text=message)
                    popocmd = False

                # fetch a quote from the IRC quote site bash.
                elif cmd(b'bashorg', msg) or cmd(b'bashquote', msg) or cmd(b'bquote', msg):
                    bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                    # get one random quote from bash.
                    bot.sendMessage(chat_id=chatId, text="" + bashquotes.print_quotes(option='r', num_quotes=1) + "")
                    popocmd = False

                # Fetch us stuff
                elif cmd(b'get', msg):
                    arg1 = msg[cmdLen(b'get', msg)+1:].decode("utf-8")
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="Get? What do you want me to 'get'?")
                    elif user == "DeadManDying":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="You get nothing Maxi! NOTHING!!!")
                    elif ("lemonade" in arg1) and ("not" not in arg1) and ("don't" not in arg1):
                        if not popocmd:
                            bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                            bot.sendMessage(chat_id=chatId, text="Sorry, I don't have any lemonade. Go ask THBot to get you some... Oh wait, he's dead..")
                    elif ("lemonade" in arg1) and (("not" in arg1) or ("don't" in arg1)):
                        if not popocmd:
                            bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                            bot.sendMessage(chat_id=chatId, text="Um... Ok.")
                    elif ("bitches" in arg1):
                        if not popocmd:
                            bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                            bot.sendMessage(chat_id=chatId, text="Searching for for bitches...")
                            time.sleep(4)
                            bot.sendMessage(chat_id=chatId, text="Searching...")
                            time.sleep(4)
                            bot.sendMessage(chat_id=chatId, text="Searching......")
                            time.sleep(4)
                            bot.sendMessage(chat_id=chatId, text="Searching.........")
                            time.sleep(4)
                            bot.sendMessage(chat_id=chatId, text="ERROR: 'bitches' not found.")
                    else:
                        if not popocmd:
                            bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                            bot.sendMessage(chat_id=chatId, text="I don't know how to get that...")
                    popocmd = False

                # say something in the chat.
                elif cmd(b'sayinchat', msg):
                    arg1 = msg[cmdLen(b'sayinchat', msg)+1:].decode("utf-8")
                    args = arg1.split()

                    # create the variable number which contains the first argument
                    number = args[0]

                    # check if number is a digit or that number minus the first letter is a digit
                    # this is to account for the minus symbol  which would case it to return false.
                    if number.isdigit() or number[1:].isdigit():
                        number_check = True
                    else:
                        number_check = False
                    
                    if len(args) == 0:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="What do you want me to say and in what chat? The format is like this:\n/sayinchat <chat_id> msg: <message>")
                    # check if number_check is false say it in the last used chat
                    elif not number_check:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        # this piece of code is to have it act like normal sayinchat except with it
                        # replying in the last used chat. If you want to enable this behaviour
                        # uncomment these few lines of code and comment out the unsorted = args line
                        #bot.sendMessage(chat_id=chatId, text="Since you didn't specify a chat to put in we will use the last used chat")
                        #time.sleep(2)
                        ## select everything except the first word
                        #unsorted = args[1:]

                        # select everything
                        unsorted = args
                        
                        # create an empty variable for use later
                        reply = ""

                        # make a reply with every item plus a space
                        for x in unsorted:
                            reply = reply + " " + x
                            
                        bot.sendMessage(chat_id=chatId, text=reply)
                    else:
                        unsorted = args[1:]
                        reply = ""

                        for x in unsorted:
                            reply = reply + " " + x
                        
                        bot.sendChatAction(chat_id=args[0], action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=args[0], text=reply)
                    popocmd = False

                # send a photo to the chat
                elif cmd(b'photoinchat', msg):
                    arg1 = msg[cmdLen(b'photoinchat', msg)+1:].decode("utf-8")
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="What photo do you want me to send and in what chat? The format is like this:\n/photoinchat <chat_id>\n Then you send me the photo or sticker that you want me to send to the given chat.")
                    else:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        photoToChatId = arg1
                        photocmd = True
                        bot.sendMessage(chat_id=chatId, text="Okay, now send me the photo so I can send it to the specified chat.")
                    popocmd = False

                # [comment removed due to it being a spoiler]
                elif cmd(b'spoil', msg):
                    arg1 = msg[cmdLen(b'spoil', msg)+1:].decode("utf-8")

                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="What do you want me to spoil for you? The format is like this:\n/spoil <story_title>")
                    else:
                        if not popocmd:
                            bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                            bot.sendMessage(chat_id=chatId, text="Everybody dies at the end.")
                    popocmd = False

                # create a random person and post the link into the chat
                elif cmd(b'randomuser', msg):
                    arg1 = msg[cmdLen(b'randomuser', msg) + 1:].decode("utf-8")
                    command = "Got command 'randomuser' with the argument '{}'".format(arg1)
                    print(command)

                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text=getRandomUser())
                    else:
                        if not popocmd:
                            bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                            bot.sendMessage(chat_id=chatId, text=getRandomUser(arg1))
                        popocmd = False

                # run some lisp code
                elif cmd(b'eval', msg):
                    args = msg[cmdLen(b'eval', msg)+1:].decode("utf-8")
                    arg1 = args
                    arg2 = ""
                    if b' /in ' in msg:
                        args = args.split(" /in ")
                        arg1 = args[0]
                        arg2 = args[1]

                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="What do you want me to evaluate for you? The format is like this:\n/eval <common_lisp>")
                    else:
                        # reply differently if hyphan is pretending to be Popo again
                        if popocmd:
                            bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                            bot.sendMessage(chat_id=chatId, text="Here is your result, maggot.")
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        # only do the command if it's not stream or with-open-file
                        if ("with-open-file" not in arg1) or ("stream" not in arg1):
                            lispProc = subprocess.Popen(["clisp", "-modern", "-q", "-q", "-q", "-q", "-i", "lispfuncs", "-x", arg1], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(arg2)
                            #lispProc = subprocess.Popen(["clisp", "-modern", "-q", "-i", "lispfuncs", "-x", arg1], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(arg2)
                            lispOutput = lispProc[0].decode('utf-8')
                            if len(lispOutput) == 0:
                                lispOutput = lispProc[1].decode('utf-8').replace("*** - ", "Error: ")
                                if len(lispOutput) == 0:
                                    if arg1 == "(exit)":
                                        lispOutput = "To exit this bot, type /quit"
                                    else:
                                        lispOutput = "Nothing returned."
                            bot.sendMessage(chat_id=chatId, text=lispOutput)
                        else:
                            bot.sendMessage(chat_id=chatId, text="I'm sorry, "+getNickname(update.message.from_user.first_name)+", I can't let you do that.")
                    popocmd = False

                # just some dumb function
                elif cmd(b'fuck', msg):
                    arg1 = msg[cmdLen(b'fuck', msg)+1:].decode("utf-8")

                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="Who do you want me to bone? And for how much?")
                    elif arg1 == "Deadmandying" or arg1 == "deadmandying" or arg1 == "Maxi" or arg1 == "maxi" or arg1 == "DeadManDying" or arg1 == "Maximilian":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="Eww... no. Absolutely disgusting.")
                        
                    elif arg1 == "Vaal" or arg1 == "vaal" or arg1 == "valentijn" or arg1 == "Valentijn" or arg1 == "Faalentijn" or arg1 == "faalentijn" or arg1 == "faal" or arg1 == "Faal":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="Umm... I've standards you know?")
                        
                    elif arg1 == "Bernie" or arg1 == "bernie" or arg1 == "sanders" or arg1 == "Sanders":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="No!!! I don't want to feel the bern!")
                        
                    elif arg1 == "Nick" or arg1 == "nick" or arg1 == "Mohamed" or arg1 == "mohamed" or arg1 == "mo" or arg1 == "Mo" or arg1 == "NerdyBuzz" or arg1 == "nerdybuzz":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="I don't think that is exactly legal seeing the power dynamic and all...")
                        
                    else:
                        if not popocmd:
                            bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                            bot.sendMessage(chat_id=chatId, text="Well, fuck you too.")
                    popocmd = False

                elif cmd(b'reddit', msg):
                     arg1 = msg[cmdLen(b'reddit', msg)+1:].decode("utf-8")
                     args = arg1.split()

                     if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="What subreddit do you want me to check out? (Default amount: 5) Formats:\n/reddit <subreddit>\n /reddit <subreddit> <top/new>\n/reddit <subreddit> <amount>\n/reddit <subreddit> <top/new> <amount>\n/reddit <subreddit> <amount> <top/new>\n/reddit <karma> <user>")

                    # check the karma of a redditor
                     elif args[0] == "karma":
                        # get the redditor
                        redditor  = r.get_redditor(args[1])
                        bot.sendMessage(chat_id=chatId, text=args[1] + " has " + str(redditor.link_karma) + " link karma and " + str(redditor.comment_karma) + " comment karma.")

                     else:

                        # Grab some submissions from reddit
                        if len(args) == 2:
                            number = 5

                            if args[1] == "top":
                                submissions = r.get_subreddit(args[0]).get_top(limit=5)
                            elif args[1] == "new":
                                submissions = r.get_subreddit(args[0]).get_new(limit=5)
                            elif args[1].isdigit():
                                number = int(args[1])
                                submissions = r.get_subreddit(args[0]).get_hot(limit=number)
                            else:
                                submissions = r.get_subreddit(args[0]).get_hot(limit=5)

                        elif len(args) == 3:
                            if args[2].isdigit():
                                number = int(args[2])
                            else:
                                number = int(args[1])
                                
                            if args[1] == "top":
                                submissions = r.get_subreddit(args[0]).get_top(limit=number)
                            elif args[1] == "new":
                                submissions = r.get_subreddit(args[0]).get_top(limit=number)
                            elif args[2] == "top":
                                submissions = r.get_subreddit(args[0]).get_top(limit=number)
                            elif args[2] == "new":
                                submissions = r.get_subreddit(args[0]).get_top(limit=number)                                
                            else:
                                submissions = r.get_subreddit(args[0]).get_hot(limit=number)
                        else:
                            submissions = r.get_subreddit(arg1).get_hot(limit=5)
                            number = 5
                            
                        # grab the titles from the submissions
                        submission = [x for x in submissions]
                        titles = [str(x) for x in submission]
                        urls = [str(x.url) for x in submission]                        

                        while 5 >= number > 0:
                            number = number - 1
                            title = titles.pop(number)
                            url = urls.pop(number)
                            story = title + ": \n" + url
                            bot.sendMessage(chat_id=chatId, text=story)

                        if number > 5:
                            bot.sendMessage(chat_id=chatId, text="My post limit is 5 or lower.")

                # hackernews posts
                elif cmd(b'hackernews', msg):
                    arg1 = msg[cmdLen(b'hackernews', msg)+1:].decode("utf-8")
                    args = arg1.split()

                    # Load the hackernews stories
                    hn = HackerNews()
                    stories = hn.top_stories()

                    if len(args) == 1:
                        number = args[0]
                        number_check = number.isdigit()
                        number = int(number)
                        
                    else:
                        number_check = False

                    if not number_check:
                        number = 5

                    while 5 >= number > 0:
                        number  = number - 1
                        storys = hn.item(stories.pop(number))
                        story = storys.title + ": \n" + storys.url
                        bot.sendMessage(chat_id=chatId, text=story)

                    if number > 5:
                        bot.sendMessage(chat_id=chatId, text="My post limit is 5 or lower.")

                # Provides acurate definitions of a word or phrase
                elif cmd(b'define', msg):
                    arg1 = msg[cmdLen(b'define', msg)+1:].decode("utf-8")
                    bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                    message = "Weird error!"
                    if arg1 == "":
                        message = "What do you want me to define? Format:\n /define <term>"
                    else:
                        defined = urbandict.define(arg1)
                        randIndex = random.randint(0,len(defined)-1)
                        word = defined[randIndex]["word"].strip()
                        definition = defined[randIndex]["def"]
                        example = defined[randIndex]["example"]
                        #url = ("\nhttp://urbandictionary.com" if ("¯\\_(ツ)_/¯" in word) and ("¯\\_(ツ)_/¯" not in arg1) else "\nhttp://urbandictionary.com/define.php?term="+word)
                        deftext = definition
                        if ("¯\\_(ツ)_/¯" in word) and ("¯\\_(ツ)_/¯" not in arg1):
                            url = "\nhttp://urbandictionary.com"
                        else:
                            deftext = "\nDefinition:" + definition
                            url = "\nhttp://urbandictionary.com/define.php?term="+word
                        if example == "":
                            message = word + "\n" + deftext + url
                        else:
                            message = word + "\n" + deftext + "\nExamples:" + example + url
                    bot.sendMessage(chat_id=chatId, text=message)
                                        
                # quit the bot. 
                elif cmd(b'quit', msg):
                    if user == "NerdyBuzz" or user == "Faalentijn":
                        if not popocmd:
                            bot.sendMessage(chat_id=chatId, text="Goodbye!")
                        else:
                            bot.sendMessage(chat_id=chatId, text="NOW BYYYEE!!!")
                        sys.exit(0)
                    else:
                        if not popocmd:
                            bot.sendMessage(chat_id=chatId, text="Bitch, you don't tell me what to do!")
                    popocmd = False

                # restart the bot
                elif cmd(b'restart', msg):
                    if user == "NerdyBuzz" or user == "Faalentijn":
                        if not popocmd:
                            bot.sendMessage(chat_id=chatId, text="See ya!")
                        else:
                            bot.sendMessage(chat_id=chatId, text="NOW BYYYEE!!!")
                        sys.exit(1)
                    else:
                        if not popocmd:
                            bot.sendMessage(chat_id=chatId, text="Bitch, you don't tell me what to do!")
                    popocmd = False

                # random function
                elif cmd(b'/', msg):
                    if (b'This is' in msg) and (b'fucking' in msg) and (b'comment' in msg):
                        if not popocmd:
                            bot.sendMessage(chat_id=chatId, text="Your mom is a fucking comment.")
                        else:
                            bot.sendMessage(chat_id=chatId, text="Popo will be doing your mommy now.")
                    elif (b"This is" in msg) and (b"comment" in msg):
                        if not popocmd:
                            message = "And this is your mom, {}.".format(user)
                            bot.sendMessage(chat_id=chatId, text=message)
                        else:
                            bot.sendMessage(chat_id=chatId, text="Guess who came in last night.")
                            time.sleep(1)
                            bot.sendMessage(chat_id=chatId, text="Your mom.")
                    else:
                        popocmd = False

                elif msg.startswith((b'@HyphanBot test')):
                    bot.sendMessage(chat_id=chatId, text="Tested.")
                    
                else:
                    #print("Got unknown command")
                    popocmd = False
            
                latestUpdateId = update.update_id

if __name__ == '__main__':
    main()
