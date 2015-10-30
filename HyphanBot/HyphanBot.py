# Import modules for use in hyphan
import sys
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
    global isRecovered
    global botName
    global latestUpdateId

    global nicknames
    global quotes

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

    # authenticate as hyphan to the telegram bot API
    bot = telegram.Bot(token='136008664:AAE2zBk8l1A4OZPQ5ebYxH1h_pVDMCtvUFo')

    # start the reddit module
    r = praw.Reddit(user_agent="HyphanBot")

    # print a message for debugging
    print("Initialized "+botName+"Bot.")

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

# set someone nickname
def setNickname(firstname, nickname):
    global nicknames
    # put the nickname into a file
    nicknames[firstname] = nickname
    with open("nicknames", 'wb') as nns:
        pickle.dump(nicknames, nns)

# remove a nickname
def delNickname(firstname):
    global nicknames
    del nicknames[firstname]
    with open("nicknames", 'wb') as nns:
        pickle.dump(nicknames, nns)

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
            bot.sendMessage(chat_id=announceToChatId, text=""+announceStr+"")
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
                        # I've no idea what module is used here so I don't know what this does yet. 
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
                        # same as above. Also these are just boilerplates until I know what bloody module is actually used
                        searchResult = duckduckgo.query(arg1)
                        if searchResult.answer.text == "":
                            bot.sendMessage(chat_id=chatId, text="Sorry, " + getNickname(update.message.from_user.first_name) + ", I don't know how to answer that..")
                        else:
                            bot.sendMessage(chat_id=chatId, text=searchResult.answer.text)
                    popocmd = False

                # a command to give yourself a different nicknamessss
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
                            # call the function to set a nickname with the arguments [accountName] and [nickName]
                            setNickname(update.message.from_user.first_name, arg1)
                            bot.sendMessage(chat_id=chatId, text="From now on, I'll start calling you " + getNickname(update.message.from_user.first_name) + ".")
                    popocmd = False

                # remove your nickname
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

                # return the nickname of the person asking
                elif cmd(b'whoami', msg):
                    print("Got command '/whoami'")
                    if getNickname(update.message.from_user.first_name) == update.message.from_user.first_name:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="As I know you from Telegram, your name is " + getNickname(update.message.from_user.first_name) + ".\nYou can tell me what else to call you by using the /callme command.")
                    else:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="You're " + getNickname(update.message.from_user.first_name) + ", or so I call you.")
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
                                # make a database of answers
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

                    
                elif cmd(b'announce', msg):
                    arg1 = msg[cmdLen(b'announce', msg)+1:].decode("utf-8")
                    print("Got command '/announce' with argument '" + arg1 + "'")
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="What do you want me to announce?")
                    else:
                        announceToChatId = chatId
                        announceStr = arg1
                        announceTime = 20
                        announceStart = True
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="Will announce '" + arg1 + "' in this chat every "+ str(announceTime) +" seconds.")
                    popocmd = False
                    
                elif cmd(b'choose', msg):
                    arg1 = msg[cmdLen(b'choose', msg)+1:].decode("utf-8")
                    print("Got command '/choose' with arguments '" + arg1 + "'")
                    args = arg1.split(" ")
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
                    
                elif cmd(b'quote', msg):
                    arg1 = msg[cmdLen(b'quote', msg)+1:].decode("utf-8")
                    arg2 = msg[cmdLen(b'quote', msg)+1+len(arg1)+1:].decode("utf-8")
                    arg3 = msg[cmdLen(b'quote', msg)+1+len(arg1)+1+len(arg2)+1:].decode("utf-8")
                    print("Got command '/quote' with arguments '" + arg1 + "', '"+arg2+"', '"+arg3+"'")
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="What quote do you want me to find or add? Possible formats:\n/quote <QuoteIdentifier>\n/quote add <QuoteIdentifier> q=<QuoteText>\n/quote random")
                    elif arg1.startswith("add"):
                    	if arg1[4:] == "":
                    		bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                    		bot.sendMessage(chat_id=chatId, text="What quote do you want me to add? Format:\n/quote add <QuoteIdentifier> q=<QuoteText>")
                    	else:
                    		addargs = arg1[4:].split(" q=")
                    		if not addargs[1]:
                    			bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                    			bot.sendMessage(chat_id=chatId, text="What quote do you want me to add? Format:\n/quote add "+arg2+" q=<QuoteText>")
                    		else:
                    			setQuote(addargs[0], addargs[1])
                    			bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                    			bot.sendMessage(chat_id=chatId, text="Added quote with id of '"+addargs[0]+"'.")
                                        
                    elif arg1.startswith("random"):
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text=randQuote())

                    else:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text=getQuote(arg1))
                    popocmd = False
                    
                elif cmd(b'mkquotes', msg):
                	#setQuote("test", "This is a test quote.")
                	bot.sendMessage(chat_id=chatId, text="This command does nothing now.")
                        
                elif cmd(b'stopannounce', msg) or cmd(b'announcestop', msg):
                    print("Got command '/stopannounce'")
                    announceStart = False
                    bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                    bot.sendMessage(chat_id=chatId, text="Will stop announcing '" + announceStr + "' in this chat.")
                    popocmd = False
                    
                elif cmd(b'bashorg', msg) or cmd(b'bashquote', msg) or cmd(b'bquote', msg):
                    print("Got command '/bashquote'")
                    bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                    bot.sendMessage(chat_id=chatId, text="" + bashquotes.print_quotes(option='r', num_quotes=1) + "")
                    popocmd = False
                    
                elif cmd(b'get', msg):
                    arg1 = msg[cmdLen(b'get', msg)+1:].decode("utf-8")
                    print("Got command '/get' with argument '" + arg1 + "'")
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="Get? What do you want me to 'get'?")
                    elif ("lemonade" in arg1) and ("not" not in arg1) and ("don't" not in arg1):
                    	if not popocmd:
                            bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                            bot.sendMessage(chat_id=chatId, text="Sorry, I don't have any lemonade. Go ask THBot to get you some... Oh wait, he's dead..")
                    elif ("lemonade" in arg1) and (("not" in arg1) or ("don't" in arg1)):
                    	if not popocmd:
                            bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                            bot.sendMessage(chat_id=chatId, text="Um... Ok.")
                    else:
                    	if not popocmd:
                            bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                            bot.sendMessage(chat_id=chatId, text="I don't know how to get that..")
                    popocmd = False
                    
                elif cmd(b'sayinchat', msg):
                    arg1 = msg[cmdLen(b'sayinchat', msg)+1:].decode("utf-8")
                    print("Got command '/sayinchat' with arguments '" + arg1 + "'")
                    args = arg1.split(" msg: ")
                    if args[0] == "" or args[1] == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="What do you want me to say and in what chat? The format is like this:\n/sayinchat <chat_id> msg: <message>")
                    else:
                        bot.sendChatAction(chat_id=args[0], action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=args[0], text=""+args[1]+"")
                    popocmd = False
                    
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
                    
                elif cmd(b'randomuser', msg):
                    arg1 = msg[cmdLen(b'randomuser', msg)+1:].decode("utf-8")
                    print("Got command '/randomuser' with arguments '" + arg1 + "'")
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text=getRandomUser())
                    else:
                    	if not popocmd:
                            bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                            bot.sendMessage(chat_id=chatId, text=getRandomUser(arg1))
                    popocmd = False
                    
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
                        if popocmd:
                            bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                            bot.sendMessage(chat_id=chatId, text="Here is your result, maggot.")
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        if ("with-open-file" not in arg1) or ("stream" not in arg1):
	                        lispProc = subprocess.Popen(["clisp", "-modern", "-q", "-q", "-q", "-q", "-i", "lispfuncs", "-x", arg1], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(arg2)
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
                    
                elif cmd(b'fuck', msg):
                    arg1 = msg[cmdLen(b'fuck', msg)+1:].decode("utf-8")
                    print("Got command '/fuck' with arguments '" + arg1 + "'")
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="Who do you want me to bone? And for how much?")
                    else:
                    	if not popocmd:
                            bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                            bot.sendMessage(chat_id=chatId, text="Well, fuck you too.")
                    popocmd = False
                    
                elif cmd(b'reddit', msg):
                    arg1 = msg[cmdLen(b'reddit', msg)+1:].decode("utf-8")
                    print("Got command '/reddit' with arguments '" + arg1 + "'")
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="What do you want me to look up on Reddit?")
                    elif arg1.startswith("top "):
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        submissions = r.get_subreddit(arg1[4:]).get_top(limit=1)
                        cat = [str(x) for x in submissions]
                        caturl = [str(x.url) for x in submissions]
                        bot.sendMessage(chat_id=chatId, text=cat[:1]+["\n"]+caturl[:1])
                    elif arg1.startswith("hot "):
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        submissions = r.get_subreddit(arg1[4:]).get_hot(limit=1)
                        cat = [str(x) for x in submissions]
                        caturl = [str(x.url) for x in submissions]
                        bot.sendMessage(chat_id=chatId, text=cat[:1]+["\n"]+caturl[:1])
                    elif arg1.startswith("u "):
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        redditor = r.get_redditor(arg1[2:])
                        bot.sendMessage(chat_id=chatId, text=arg1[2:]+" has " + str(redditor.link_karma) + " link karma and " + str(redditor.comment_karma) + " comment karma.")
                    else:
                    	if not popocmd:
                            bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                            bot.sendMessage(chat_id=chatId, text="Idk what happens in this else block...")
                    popocmd = False
                    
                elif cmd(b'quit', msg):
                    print("Got command '/quit'")
                    if update.message.from_user.username == "NerdyBuzz":
                        if not popocmd:
                            bot.sendMessage(chat_id=chatId, text="Goodbye!")
                        else:
                            bot.sendMessage(chat_id=chatId, text="NOW BYYYEE!!!")
                        sys.exit(0)
                    else:
                        if not popocmd:
                            bot.sendMessage(chat_id=chatId, text="Bitch, you don't tell me what to do!")
                    popocmd = False
                    
                elif cmd(b'restart', msg):
                    print("Got command '/restart'")
                    if update.message.from_user.username == "NerdyBuzz":
                        if not popocmd:
                            bot.sendMessage(chat_id=chatId, text="See ya!")
                        else:
                            bot.sendMessage(chat_id=chatId, text="NOW BYYYEE!!!")
                        sys.exit(1)
                    else:
                        if not popocmd:
                            bot.sendMessage(chat_id=chatId, text="Bitch, you don't tell me what to do!")
                    popocmd = False
                    
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
                    	bot.sendMessage(chat_id=chatId, text="\"Sorry no ball\" -- Big Mama")
                    popocmd = False
                elif msg.startswith((b'@HyphanBot test')):
                    bot.sendMessage(chat_id=chatId, text="Tested.")
                else:
                    print("Got unknown command")
                    if not popocmd:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        time.sleep(2)
                        bot.sendMessage(chat_id=chatId, text="¯\_(ツ)_/¯")
                    popocmd = False
            
                latestUpdateId = update.update_id

if __name__ == '__main__':
    main()
