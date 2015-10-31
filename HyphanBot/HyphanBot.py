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

    global r

    # set the bot name
    botName = "Hyphan"

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
    # a normal commande
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

    global r

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

            # print an error if hyphan crashed
            if isRecovered:
                print("I just recovered from a crash, sorry about that...")

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
                # print the command hyphan received
                print("Recieved '", msg, "' in chat", chatId)

                # if the command is popo send a photo
                if ("popo" in msg.decode('utf-8').lower()):
                    bot.sendPhoto(chat_id=chatId, photo="http://img08.deviantart.net/e3f9/i/2010/254/f/1/mr__popo__s_deadly_eyes_by_khmaivietboi-d2yjspi.jpg")
                    bot.sendMessage(chat_id=chatId, text="HIII!!")
                    popocmd = True

                # return nothing
                elif cmd(b'help', msg):
                    print("Got command '/help'")
                    if not popocmd:
                        bot.sendMessage(chat_id=chatId, text="?")
                    popocmd = False

                # send an about message if someone ask for it
                elif cmd(b'about', msg):
                    print("Got command '/about'")
                    if not popocmd:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        time.sleep(1)
                        bot.sendMessage(chat_id=chatId, text="I am King "+botName+", ruler of the northern part of the galaxy.")
                    popocmd = False

                # send a duckduckgo search with a specified keyword
                elif cmd(b'duckgo', msg):
                    arg1 = urllib.parse.quote_plus(msg[cmdLen(b'duckgo', msg)+1:].decode("utf-8"))
                    # if no keyword is supplied ask for one
                    print("Got command '/duckgo' with argument '" + arg1 + "'")
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        time.sleep(1)
                        bot.sendMessage(chat_id=chatId, text="What do you want me to look up?")
                    # if a keyword is supplied return a duckduckgo search link
                    else:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        time.sleep(1)
                        bot.sendMessage(chat_id=chatId, text="Here you go, " + getNickname(update.message.from_user.first_name) + ": https://duckduckgo.com/?q=" + arg1)
                    popocmd = False

                # a bit more complicated version of duckgo. It gets the first results
                # of a duckduckgo search and return it. 
                elif cmd(b'webfetch', msg):
                    arg1 = msg[cmdLen(b'webfetch', msg)+1:].decode("utf-8")
                    print("Got command '/webfetch' with argument '" + arg1 + "'")
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        time.sleep(1)
                        bot.sendMessage(chat_id=chatId, text="What do you want me to look up?")
                    else:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        # Zci means Zero Click Info which is those little boxes that are displayed on DuckDuckGo
                        searchResult = duckduckgo.get_zci(arg1)
                        bot.sendMessage(chat_id=chatId, text=getNickname(update.message.from_user.first_name) + ", here is what I can gather about '" + arg1 + "':\n" + searchResult)
                    popocmd = False

                # ask hyphan a question
                elif cmd(b'ask', msg):
                    arg1 = msg[cmdLen(b'ask', msg)+1:].decode("utf-8")
                    print("Got command '/ask' with argument '" + arg1 + "'")
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        time.sleep(1)
                        bot.sendMessage(chat_id=chatId, text="What is your question?")
                    else:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        # return the result of a keyword
                        searchResult = duckduckgo.query(arg1)
                        if searchResult.answer.text == "":
                            bot.sendMessage(chat_id=chatId, text="Sorry, " + getNickname(update.message.from_user.first_name) + ", I don't know how to answer that..")
                        else:
                            bot.sendMessage(chat_id=chatId, text=searchResult.answer.text)
                    popocmd = False

                # a command to give yourself a different nickname
                elif cmd(b'callme', msg):
                    arg1 = msg[cmdLen(b'callme', msg)+1:].decode("utf-8")
                    print("Got command '/callme' with argument '" + arg1 + "'")
                    
                # Registers a chat id with a username or, if used in a group chat, a short name.
                elif cmd(b'register', msg):
                    arg1 = msg[cmdLen(b'register', msg)+1:].decode("utf-8")
                    command = "Got command '/register' with argument {}".format(arg1)
                    print(command)

                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        if chatId < 0: # If the chat ID is less than 0 (aka negative number), it's a group chat, otherwise it's not.
                            args = arg1.split(" ") # To insure that no spaces will be registered
                            if not getShortChatName(chatId) and addRegKey(args[0], chatId):
                                message = "Registered group chat with {}.".format(args[0])
                                bot.sendMessage(chat_id=chatId, text=message)
                            else:
                                if not getShortChatName(chatId):
                                    message = "This shortname {} is already registered to another chat".format(args[0])
                                    bot.sendMessage(chat_id=chatId, text=message)
                                else:
                                    message = "This group chat is already as {}.".format(getShortChatName(chatId))
                                    bot.sendMessage(chat_id=chatId, text=message)
                    popocmd = False
                    
                # To test the register command.
                elif cmd(b'chatid', msg):
                    arg1 = msg[cmdLen(b'chatid', msg)+1:].decode("utf-8")
                    print("Got command '/chatid' with argument '" + arg1 + "'")
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
                    popocmd = False

                # Send a private message to someone through Hyphan.
                elif cmd(b'pm', msg):
                    arg1 = msg[cmdLen(b'pm', msg)+1:].decode("utf-8")
                    print("Got command '/pm' with argument '" + arg1 + "'")
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
                                    bot.sendMessage(chat_id=recipientId, text="PM from "+update.message.from_user.first_name+" ("+update.message.from_user.username+"):\n" + pmsg + "\n[To reply to this message, use: /pm "+update.message.from_user.username+" <your reply> ]")
                                else:
                                    bot.sendMessage(chat_id=chatId, text="Sorry, I can't send a private message to a group.")
                            else:
                                bot.sendMessage(chat_id=chatId, text="Sorry to tell you this, but the user you're trying to send a message to is not registered with me.")
                    popocmd = False

                # This command is used only for initialising the database file
                #elif cmd(b'mkdb', msg):
                #    addRegKey("testkey", 1234)

                # remove someones nickname
                elif cmd(b'nonick', msg):
                    print("Got command '/nonick'")
                    # send a message if no nickname is set.
                    if getNickname(update.message.from_user.first_name) == update.message.from_user.first_name:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        time.sleep(1)
                        bot.sendMessage(chat_id=chatId, text="I'm already using the name that you set via Telegram, aren't I, " + getNickname(update.message.from_user.first_name) + "?\nYou can tell me what else to call you by using the /callme command.")
                    else:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        # remove the nickname from the file
                        delNickname(update.message.from_user.first_name)
                        bot.sendMessage(chat_id=chatId, text="Fine, I'll go back to calling you " + getNickname(update.message.from_user.first_name) + " again.")
                    popocmd = False

                # return the nickname of the person askin
                elif cmd(b'whoami', msg):
                    print("Got command '/whoami'")
                    if getNickname(update.message.from_user.first_name) == update.message.from_user.first_name:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="As I know you from Telegram, your name is " + getNickname(update.message.from_user.first_name) + ".\nYou can tell me what else to call you by using the /callme command.")
                    else:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="You're " + getNickname(update.message.from_user.first_name) + ", or so I call you.")
                    popocmd = False

                # give someone a nickname
                elif cmd(b'callme', msg):
                    arg1 = msg[cmdLen(b'callme', msg)+1:].decode("utf-8")
                    print("Got command '/callme' with argument '" + arg1 + "'")
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        time.sleep(1)
                        bot.sendMessage(chat_id=chatId, text="What do you want me to call you, " + getNickname(update.message.from_user.first_name) + "?")
                    else:
                        if not popocmd:
                            bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                            setNickname(update.message.from_user.first_name, arg1)
                            bot.sendMessage(chat_id=chatId, text="From now on, I'll start calling you " + getNickname(update.message.from_user.first_name) + ".")
                    popocmd = False

                # create a magical 8-ball 
                elif cmd(b'magic8', msg) or cmd(b'8', msg):
                    # run the command both if someone uses /magic8 or /8
                    if cmd(b'magic8', msg):
                        arg1 = msg[cmdLen(b'magic8', msg)+1:].decode("utf-8")
                    else:
                        arg1 = msg[cmdLen(b'8', msg)+1:].decode("utf-8")
                    print("Got command '/magic8' with argument '" + arg1 + "'")
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="Ask anything and I shall answer.")
                    else:
                        if not popocmd:
                            # reject the command if it's from someone who cannot be trusted
                            if update.message.from_user.username == "DeadManDying":
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
                    print("Got command '/wait5andsay' with argument '" + arg1 + "'")
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="What do you want me to say after 5 seconds?")
                    elif update.message.from_user.username == "Valentijn":
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
                    print("Got command '/announce' with argument '" + arg1 + "'")
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="What do you want me to announce?")
                    elif update.message.from_user.username == "DeadManDying":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="Bad Maxi bad!")
                    else:
                        announceToChatId = chatId
                        announceStr = arg1
                        announceTime = 20
                        announceStart = True
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="Will announce '" + arg1 + "' in this chat every "+ str(announceTime) +" seconds.")
                    popocmd = False

                # pick one of a list of choices
                elif cmd(b'choose', msg):
                    arg1 = msg[cmdLen(b'choose', msg)+1:].decode("utf-8")
                    print("Got command '/choose' with arguments '" + arg1 + "'")
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
                    print("Got command '/quote' with arguments '" + arg1 + "', '"+arg2+"', '"+arg3+"'")
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
                    
                # STOP ANNOUNCING FOR FUCKS SAKE
                elif cmd(b'stopannounce', msg) or cmd(b'announcestop', msg):
                    print("Got command '/stopannounce'")
                    announceStart = False
                    bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                    bot.sendMessage(chat_id=chatId, text="Will stop announcing '" + announceStr + "' in this chat.")
                    popocmd = False

                # fetch a quote from the IRC quote site bash.
                elif cmd(b'bashorg', msg) or cmd(b'bashquote', msg) or cmd(b'bquote', msg):
                    print("Got command '/bashquote'")
                    bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                    # get one random quote from bash.
                    bot.sendMessage(chat_id=chatId, text="" + bashquotes.print_quotes(option='r', num_quotes=1) + "")
                    popocmd = False

                # Fetch us stuff
                elif cmd(b'get', msg):
                    arg1 = msg[cmdLen(b'get', msg)+1:].decode("utf-8")
                    print("Got command '/get' with argument '" + arg1 + "'")
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="Get? What do you want me to 'get'?")
                    elif update.message.from_user.username == "DeadManDying":
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
                    print("Got command '/sayinchat' with arguments '" + arg1 + "'")
                    args = arg1.split()

                    # create the variable number which contains the first argument
                    number = args[0]

                    # check if number is a digit or that number minus the first letter is a digit
                    # this is to account for the minus symbol  which would case it to return false.
                    if number.isdigit() or number[1:].isdigit():
                        number_check = True
                    else:
                        number_check = False
                    
                    if len(args) == 1:
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
                    print("Got command '/photoinchat' with arguments '" + arg1 + "'")
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
                    print("Got command '/spoil' with arguments '" + arg1 + "'")
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
                    print("Got command '/eval' with arguments '" + str(arg1) + "' and '" + str(arg2) + "'")
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
                    print("Got command '/fuck' with arguments '" + arg1 + "'")
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

                # check the karma of a paticular redditor
                elif cmd(b'check_karma', msg):
                    arg1 = msg[cmdLen(b'check_karma', msg)+1:].decode("utf-8")
                    bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                    
                    command = "Got command 'check_karma' with the argument '{}'".format(arg1)
                    print(command)

                    if arg1 == "":
                        bot.sendMessage(chat_id=chatId, text="Please add a user from whom you want the karma count")
                    else:
                        # get the stats of a redditor
                        redditor = r.get_redditor(arg1)

                        # fetch the comment and link karma and display them
                        bot.sendMessage(chat_id=chatId, text=arg1 + " has " + str(redditor.link_karma) + " link karma and " + str(redditor.comment_karma) + " comment karma.")
                    
                elif cmd(b'reddit', msg):
                    arg1 = msg[cmdLen(b'reddit', msg)+1:].decode("utf-8")
                    args = arg1.split()

                    command = "Got command 'reddit' with the argument '{}'".format(arg1)
                    print(command)

                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="Please add a subreddit you want to look at!")
                    else:
                        # Grab some submissions from reddit
                        r = praw.Reddit(user_agent='HyphanBot')

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
                            number = args[2]
                            number_check = number.isdigit()
                            number = int(number)

                            if args[1] == "top":
                                submissions = r.get_subreddit(args[0]).get_top(limit=number)
                            elif args[1] == "new":
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

                        while number > 0:
                            number = number - 1
                            title = titles.pop(number)
                            url = urls.pop(number)
                            story = title + ": \n" + url
                            bot.sendMessage(chat_id=chatId, text=story)

                # hackernews posts
                elif cmd(b'hackernews', msg):
                    print("Got command '/hackernews'")

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

                    while number > 0:
                        number  = number - 1
                        storys = hn.item(stories.pop(number))
                        story = storys.title + ": \n" + storys.url
                        bot.sendMessage(chat_id=chatId, text=story)
                                        
                # quit the bot. 
                elif cmd(b'quit', msg):
                    print("Got command '/quit'")
                    if update.message.from_user.username == "NerdyBuzz" or update.message.from_user.username == "Faalentijn":
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
                    print("Got command '/restart'")
                    if update.message.from_user.username == "NerdyBuzz" or update.message.from_user.username == "Faalentijn":
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
                    print("Got command '//'")
                    if (b'This is' in msg) and (b'fucking' in msg) and (b'comment' in msg):
                        if not popocmd:
                            bot.sendMessage(chat_id=chatId, text="Your mom is a fucking comment.")
                        else:
                            bot.sendMessage(chat_id=chatId, text="Popo will be doing your mommy now.")
                    elif (b"This is" in msg) and (b"comment" in msg):
                        if not popocmd:
                            bot.sendMessage(chat_id=chatId, text="{} And this is your mom.")
                        else:
                            bot.sendMessage(chat_id=chatId, text="Guess who came in last night.")
                            time.sleep(1)
                            bot.sendMessage(chat_id=chatId, text="Your mom.")
                    else:
                        popocmd = False

                elif msg.startswith((b'@HyphanBot test')):
                    bot.sendMessage(chat_id=chatId, text="Tested.")
                    
                else:
                    print("Got unknown command")
                    popocmd = False
            
                latestUpdateId = update.update_id

if __name__ == '__main__':
    main()
