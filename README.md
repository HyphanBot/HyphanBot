HyphanBot
=========
**HyphanBot** is an expandable [Telegram](https://telegram.org) bot server
written in Python. The original goal of the project was to experiment with
Telegram's Bot API and test its capabilities. HyphanBot is currently under
development.

---

Docs: *Coming soon...*

Website: <https://hyphanbot.techisized.com>

IRC: <https://irc.techisized.com/#hyphanbot>

---

Installation/Setup
-------------------
Currently, we have no installation script available for HyphanBot, *yet*.

Instead, you can run HyphanBot using the `hyphanbot.sh` script provided in this
repository after cloning it:
```bash
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

Inline Bot Mode
---------------
HyphanBot has a unique Inline Bot system which can allow the use of multiple
inline bot functionalities (or "features," as we like to call them) in one bot.
This is done by giving users the ability to change which inline feature they
want to use through the bot's private chat (because Telegram doesn't currently
support a way to provide inline bot arguments that can trigger different types
of results). HyphanBot's inline bot features can be provided though various
mods that utilize HyphanBot's Inline Engine.

To enable HyphanBot's Inline Bot system, you'll have to first tell [@BotFather]
(https://telegram.me/botfather) that your bot is capable of handling inline bot
queries. To do this, issue `/set_inline` to BotFather, select your bot, then
think of a placeholder that people would see when they try to use inline bot
features.

Currently, the default HyphanBot Inline feature, called **BOLD CAPS**, simply
allows the user to send bolded, uppercase text to the chat. In order to use
inline features provided by mods, simply click on "Change Settings" in the
inline results box, or type `/start inline` in HyphanBot's chat. This will
allow you to list available inline features and change what HyphanBot does with
inline queries.

HyphanBot's Inline Engine is still under development (just like the rest of
Hyphan) and is currently missing a few features that we think are essential to
the bot.

Hyphan or HyphanBot?
--------------------
Hyphan refers to the bot's personality in the Telegram chat. Specifically, this
guy: [@HyphanBot](https://telegram.me/hyphanbot).

HyphanBot refers to the codebase in which Hyphan runs on (this program).

License
-------
HyphanBot is licensed under the
[GNU Afferno General Public License v3.0]
(https://gnu.org/licenses/agpl-3.0.html).