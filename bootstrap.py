from subprocess import call
from time import sleep
from sys import exit

def main():
	call("cd $OPENSHIFT_REPO_DIR/HyphanBot/; python HyBotLauncher.py", shell=True)

if __name__ == '__main__':
	main()