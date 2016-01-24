HyphanBot
=========
**HyphanBot** is an expandable [Telegram](https://telegram.org) bot server 
written in Python. The original goal of the project was to experiment with 
Telegram's Bot API and test its capabilities. HyphanBot is currently under 
development and will be publically available as soon as we have a good, stable 
Hyphan.

Installation/Set-up
-------------------
Currently, we have no installation script available for HyphanBot, *yet*. 
Instead, you can run HyphanBot with `python3 core/main.py` (assuming you're in 
HyphanBot's root directory).

Configuration
-------------
HyphanBot's configuration file is accessed by HyphanBot and its mods. The 
current base configuration requires two values, the bot's token you recieved 
from [@BotFather](https://telegram.me/botfather), and the list of bot 
administrators' usernames seperated by spaces.
```
# config.ini #
[general]
token = BOT_TOKEN
admins = username1 username2 ...
```

Hyphan or HyphanBot?
--------------------
Hyphan refers to the bot itself.

HyphanBot refers to the codebase in which Hyphan runs on (this program).

License
-------
HyphanBot is licensed under the [GNU Afferno General Public License v3.0](https://gnu.org/licenses/agpl-3.0.html).