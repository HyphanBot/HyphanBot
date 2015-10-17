import sys
import telegram
import time
import urllib
import duckduckgo
import pickle
import random
from html.parser import HTMLParser
import bashquotes
import requests

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

    botName = "Hyphan"
    
    nicknames = {}

    quotes = {}
    
    bot = telegram.Bot(token='136008664:AAE2zBk8l1A4OZPQ5ebYxH1h_pVDMCtvUFo')
    
    print("Initialized "+botName+"Bot.")
    
    try:
        latestUpdateId = bot.getUpdates()[-1].update_id
    except IndexError:
        latestUpdateId = None

    if (len(sys.argv) > 1) and (str(sys.argv[1]) == "recover"):
        print("Recovered from a crash.")
        isRecovered = True
        #bot.sendMessage(chat_id=bot.getUpdates(offset=latestUpdateId)[-1].message.chat_id, text="I either recovered from a crash or just restarted, sorry if I crashed...")
    else:
        isRecovered = False

    announceTimer = 0
    announceStart = False

    photocmd = False
    popocmd = False

    while True:
        getMsg(bot)
        time.sleep(1)

def cmd(command, message):
    global botName
    return (message.startswith((b'/' + command).decode('utf-8').lower().encode('utf-8'))) or (message.startswith((b'' + command).decode('utf-8').lower().encode('utf-8'))) or (message.startswith(b'@'+ botName.encode('utf-8') +b'Bot ' + command))

def cmdLen(command, message):
    global botName
    if message.startswith(b'/' + command):
        return len("/" + command.decode('utf-8'))
    elif message.startswith(b'' + command):
        return len(command.decode('utf-8'))
    elif message.startswith(b'@HyphanBot ' + command):
        return len("@"+botName+"Bot " + command.decode('utf-8'))

def getNickname(firstname):
    global nicknames
    with open("nicknames", 'rb') as nns:
        userNicknames = pickle.loads(nns.read())
        nicknames = userNicknames
    if not firstname in nicknames:
        return firstname
    return nicknames[firstname]

def setNickname(firstname, nickname):
    global nicknames
    nicknames[firstname] = nickname
    with open("nicknames", 'wb') as nns:
        pickle.dump(nicknames, nns)

def delNickname(firstname):
    global nicknames
    del nicknames[firstname]
    with open("nicknames", 'wb') as nns:
        pickle.dump(nicknames, nns)

def getQuote(quoteId):
    global quotes
    with open("quotes", 'rb') as qts:
        userquotes = pickle.loads(qts.read())
        quotes = userquotes
    if not quoteId in quotes:
        return "Sorry, I cannot find the quote with id of '" + quoteId + "'. You can try creating it by typing: \n/quote add " + quoteId + " q=<QuoteText>"
    return '"'+quotes[quoteId]+'"'

def randQuote():
    global quotes
    with open("quotes", 'rb') as qts:
        userquotes = pickle.loads(qts.read())
        quotes = userquotes
    randKey = random.choice(list(quotes.keys()))
    return '"'+quotes[randKey]+'" ('+randKey+')'

def setQuote(quoteId, quoteStr):
    global quotes
    quotes[quoteId] = quoteStr
    with open("quotes", 'wb') as qts:
        pickle.dump(quotes, qts)

def delQuote(quoteId):
    global quotes
    del quotes[quoteId]
    with open("quotes", 'wb') as qts:
        pickle.dump(quotes, qts)

def getRandomUser(field='name'):
	url = "http://nerdyserv.no-ip.org/random-backend.php?for=usr"
	genseed = requests.get(url+"&prop=seed").text
	content = requests.get(url+"&prop="+field+"&filter=seed-"+genseed).text
	seedurl = "http://nerdyserv.no-ip.org/random.html?for=usr&filter=seed-"+genseed+""
	print(content)
	print(seedurl)
	return "" + content + "\n" + seedurl

def getBashQuote():
    heads = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) \
          AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64',
         'Accept': 'text/html,application/xhtml+xml, \
          application/xml;q=0.9,*/*;q=0.8',
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         'Accept-Encoding': 'none',
         'Accept-Language': 'en-US,en;q=0.8',
         'Connection': 'keep-alive'}
    
    found = False
    html_parser = HTMLParser()
    while found is not True:
        current_quote = random.randint(2, 90000)
        #print current_quote
        request = urllib.request.Request('http://bash.org/?' + str(current_quote), headers=heads)
        f = urllib.request.urlopen(request)
        # read html from url
        gethtml = f.read()
        # remove multiple spaces (for better looking results)
        gethtml = " ".join(gethtml.split())
        
        result = gethtml.find('<p class="qt">', 0)
        if result != -1:
            found = True
            first_found = gethtml[result + 14:result + 1400]
            result2 = first_found.find('</td>', 0)
            second_found = first_found[0:result2]
            second_found = "\n".join(second_found.split("<br />"))
            second_found = "".join(second_found.split("</p>"))
            return " Link to post: http://bash.org/?" + str(current_quote) + "\n ============================================\n " + html_parser.unescape(second_found)

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

    if announceStart:
        if announceTimer == 0:
            bot.sendMessage(chat_id=announceToChatId, text=""+announceStr+"")
            print("Announced ", announceStr)
            announceTimer = announceTime
        announceTimer = announceTimer - 1

    for update in bot.getUpdates(offset=latestUpdateId):
        if latestUpdateId < update.update_id:
            chatId = update.message.chat_id
            msg = update.message.text.encode('utf-8')
            
            if isRecovered:
                #bot.sendMessage(chat_id=chatId, text="I just recovered from a crash, sorry about that...")
                pass

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
                print("Recieved '", msg, "' in chat", chatId)
                if ("popo" in msg.decode('utf-8').lower()):
                	bot.sendPhoto(chat_id=chatId, photo="http://img08.deviantart.net/e3f9/i/2010/254/f/1/mr__popo__s_deadly_eyes_by_khmaivietboi-d2yjspi.jpg")
                	bot.sendMessage(chat_id=chatId, text="HIII!!")
                	popocmd = True
                if cmd(b'help', msg):
                    print("Got command '/help'")
                    if not popocmd:
                        bot.sendMessage(chat_id=chatId, text="?")
                    popocmd = False
                elif cmd(b'about', msg):
                    print("Got command '/about'")
                    if not popocmd:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        time.sleep(1)
                        bot.sendMessage(chat_id=chatId, text="I am King "+botName+", ruler of the northern part of the galaxy.")
                    popocmd = False
                elif cmd(b'duckgo', msg):
                    arg1 = urllib.parse.quote_plus(msg[cmdLen(b'duckgo', msg)+1:].decode("utf-8"))
                    print("Got command '/duckgo' with argument '" + arg1 + "'")
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        time.sleep(1)
                        bot.sendMessage(chat_id=chatId, text="What do you want me to look up?")
                    else:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        time.sleep(1)
                        bot.sendMessage(chat_id=chatId, text="Here you go, " + getNickname(update.message.from_user.first_name) + ": https://duckduckgo.com/?q=" + arg1)
                    popocmd = False
                elif cmd(b'webfetch', msg):
                    arg1 = msg[cmdLen(b'webfetch', msg)+1:].decode("utf-8")
                    print("Got command '/webfetch' with argument '" + arg1 + "'")
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        time.sleep(1)
                        bot.sendMessage(chat_id=chatId, text="What do you want me to look up?")
                    else:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        searchResult = duckduckgo.get_zci(arg1)
                        bot.sendMessage(chat_id=chatId, text=getNickname(update.message.from_user.first_name) + ", here is what I can gather about '" + arg1 + "':\n" + searchResult)
                    popocmd = False
                elif cmd(b'ask', msg):
                    arg1 = msg[cmdLen(b'ask', msg)+1:].decode("utf-8")
                    print("Got command '/ask' with argument '" + arg1 + "'")
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        time.sleep(1)
                        bot.sendMessage(chat_id=chatId, text="What is your question?")
                    else:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        searchResult = duckduckgo.query(arg1)
                        if searchResult.answer.text == "":
                            bot.sendMessage(chat_id=chatId, text="Sorry, " + getNickname(update.message.from_user.first_name) + ", I don't know how to answer that..")
                        else:
                            bot.sendMessage(chat_id=chatId, text=searchResult.answer.text)
                    popocmd = False
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
                elif cmd(b'nonick', msg):
                    print("Got command '/nonick'")
                    if getNickname(update.message.from_user.first_name) == update.message.from_user.first_name:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        time.sleep(1)
                        bot.sendMessage(chat_id=chatId, text="I'm already using the name that you set via Telegram, aren't I, " + getNickname(update.message.from_user.first_name) + "?\nYou can tell me what else to call you by using the /callme command.")
                    else:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        delNickname(update.message.from_user.first_name)
                        bot.sendMessage(chat_id=chatId, text="Fine, I'll go back to calling you " + getNickname(update.message.from_user.first_name) + " again.")
                    popocmd = False
                elif cmd(b'whoami', msg):
                    print("Got command '/whoami'")
                    if getNickname(update.message.from_user.first_name) == update.message.from_user.first_name:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="As I know you from Telegram, your name is " + getNickname(update.message.from_user.first_name) + ".\nYou can tell me what else to call you by using the /callme command.")
                    else:
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="You're " + getNickname(update.message.from_user.first_name) + ", or so I call you.")
                    popocmd = False
                elif cmd(b'magic8', msg) or cmd(b'8', msg):
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
                            if update.message.from_user.username == "DeadManDying":
                                bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                                bot.sendMessage(chat_id=chatId, text="Go suck a dick, Maxi.")
                            else:
                                bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                                magicMsgs = ["It is certain"," It is decidedly so","Without a doubt","Yes definitely","You may rely on it","As I see it yes","Most likely","Outlook good","Yes","Signs point to yes","Reply hazy try again","Ask again later","Better not tell you now","Cannot predict now","Concentrate and ask again","Don't count on it","My reply is no","God says no","Very doubtful","Outlook not so good"]
                                magicReply = random.randint(0,len(magicMsgs) - 1)
                                bot.sendMessage(chat_id=chatId, text=magicMsgs[magicReply])
                    popocmd = False
                elif cmd(b'wait5andsay', msg):
                    arg1 = msg[cmdLen(b'wait5andsay', msg)+1:].decode("utf-8")
                    print("Got command '/wait5andsay' with argument '" + arg1 + "'")
                    if arg1 == "":
                        bot.sendChatAction(chat_id=chatId, action=telegram.ChatAction.TYPING)
                        bot.sendMessage(chat_id=chatId, text="What do you want me to say after 5 seconds?")
                    else:
                    	if not popocmd:
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