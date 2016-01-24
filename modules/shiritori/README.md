HyphanBot Shiritori Mod
=======================
**Shiritori**, also known as **Word Chain**, is a game originating in Japan in which the players say a word that begins with the last letter of the previous word. The word "Shiritori" literally means "taking the end" in Japanese according to [this Wikipedia article](https://en.wikipedia.org/wiki/Shiritori) (See also: [Word Chain](https://en.wikipedia.org/wiki/Word_chain)).

This mod implements the game into HyphanBot allowing Hyphan to compete with the player in a simple game of *Word Chain*.

How to play
-----------
Once the player issues the command, `/shiritori start` or `/wordchain start`, Hyphan will start with a random, applicable word from the wordlist. The player then continues by sending a word that starts out with the last letter of the previous word, then Hyphan will do the same. This continues on until there is a win, or the player times out.

This mod uses a score system similar to http://shiritorigame.com, score starts out at a hundred, then decreases each turn by the length of the word minus the minimum length. The goal, in this case, is to get a score of zero.

Installation
------------
As with all HyphanBot mods, the installation of this one is simple. Simply extract and move the 'shiritori' folder into HyphanBot's mods directory. Once you run HyphanBot, it will take care of the rest.

Configuration
-------------
This mod uses HyphanBot's configuration API to provide a number of configurable options that define some of the rules of the game. Below are some of the basic as well as advanced options that can be used.

### Defaults
```
[shiritori]

## Basic rules ##

# Time limit for each turn in seconds (default: 30)
timelimit = 30

# The starting score (default: 100)
startscore = 100

# The minimum number of characters allowed without panalty (default: 3)
minimumlength = 3

## Messages ##

# Message displayed when the user wins
winmessage = Senpai, tell me your secrets!

# Message displayed when the user loses
losemessage = This was so predictable, hehe.

## Advanced ##

# Where to download the wordlist (URL below is an example, not the actual default)
wlurl = http://localhost/hyphan/SCOWL-wl/words.txt

# The filename to use when saving the wordlist
wlsavename = shiritori_wordlist.txt
```

Licence
-------
Same as HyphanBot