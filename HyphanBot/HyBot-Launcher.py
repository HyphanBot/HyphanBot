from subprocess import call
from time import sleep
from sys import exit

def main(recover):
    if recover:
        botLunch = call("python HyphanBot.py recover", shell=True)
    else:
        botLunch = call("python HyphanBot.py", shell=True)
    
    while True:
        if botLunch > 0:
            print("Bot Crashed! Restarting in 3 seconds...")
            sleep(3)
            print("Restarting now!")
            main(True)
        else:
            print("Bot safely quit.")
            exit(0)
        sleep(1)

if __name__ == '__main__':
    main(False)