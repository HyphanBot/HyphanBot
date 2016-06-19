HyphanBot
=========
**HyphanBot** is an expandable [Telegram](https://telegram.org) bot server
written in Python. The original goal of the project was to experiment with
Telegram's Bot API and test its capabilities. HyphanBot is currently under
development and will be publically available as soon as we have a good, stable
Hyphan.

Installation/Setup
-------------------
Currently, we have no installation script available for HyphanBot, *yet*.

Instead, you can run HyphanBot using the `hyphanbot.sh` script provided in this
repository after cloning it:
```
$ git clone https://gitlab.com/NerdyBuzz/HyphanBot.git
$ cd HyphanBot/
$ chmod +x hyphanbot.sh
$ ./hyphanbot.sh
```
After running HyphanBot, you will be prompted to enter the two basic
configuration values required to make HyphanBot run on Telegram:
* The **Bot Token** obtained from Telegram's [@BotFather]
(https://telegram.me/botfather) where you create your bot username for HyphanBot
to run under, and
* The **Bot Administerators**, a list of Telegram usernames, separated by a
space, who can have access to control the bot through specific commands.

You could also manually configure these values from HyphanBot's configuration
file (see below).

Configuration
-------------
HyphanBot's configuration file is accessed by HyphanBot and its mods. It is
created under the `~/.config/hyphan/config.ini` path by default.

As stated above, the current base configuration requires two values, the bot's
token you recieved from [@BotFather](https://telegram.me/botfather), and the
list of bot administrators' usernames seperated by spaces.
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
HyphanBot is licensed under the
[GNU Afferno General Public License v3.0]
(https://gnu.org/licenses/agpl-3.0.html).