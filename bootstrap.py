from subprocess import call
from time import sleep
from sys import exit

def main():
	call("cd HyphanBot/; python HyBotLauncher.py", shell=True)

if __name__ == '__main__':
	main()