from subprocess import call
from time import sleep
import os
import sys


def launchBot(recover=False, prefix=""):
    pid = str(os.getpid())
    pidfile = "/tmp/HBLauncher.pid"

    if os.path.isfile(pidfile):
        print(pidfile+" already exists, exiting...")
        sys.exit()
    else:
        open(pidfile, 'w').write(pid)

    if recover:
        botLunch = call("python "+prefix+"HyphanBot.py recover", shell=True)
    else:
        botLunch = call("python "+prefix+"HyphanBot.py", shell=True)
    
    while True:
        if botLunch > 0:
            print("Bot Crashed! Restarting in 3 seconds...")
            sleep(3)
            print("Restarting now!")
            launchBot(True)
        else:
            print("Bot safely quit.")
            os.unlink(pidfile)
            sys.exit(0)
        sleep(1)
    os.unlink(pidfile)

if __name__ == '__main__':
    launchBot(False)