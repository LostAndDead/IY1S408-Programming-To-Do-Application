from pyfiglet import Figlet
from colorama import Fore, Back, Style

class CreditsPage:

    def __init__(self, main, utils):
        self.main = main
        self.utils = utils

    def printMenu(self, main, utils):
        self.main = main
        self.utils = utils
        self.utils.clear()
        f = Figlet(font='cybermedium')
        print (f.renderText('Credits:'))
        print("""  Made by Jake, or the online alias LostAndDead
  A simple console based To-Do Application for a university
  coursework. No, using Python was not my choice.

  https://lostanddead.com/
  https://github.com/LostAndDead

Press [ENTER] To Exit...
""")
        self.main.debugPrint("\nDEBUG MODE ACTIVE\n")

    def show(self):
        self.printMenu(self.main, self.utils)
        self.utils.getNextKey()
        self.main.switchToMain(0)