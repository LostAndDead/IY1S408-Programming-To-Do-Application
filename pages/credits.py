from pyfiglet import Figlet
from colorama import Fore, Back, Style

def printMenu():
    import utils
    utils.clear()
    f = Figlet(font='cybermedium')
    print (f.renderText('Credits:'))
    print("""  Made by Jake, or the online alias LostAndDead
  A simple console based To-Do Application for a university
  coursework. No, using Python was not my choice.

  https://lostanddead.com/
  https://github.com/LostAndDead

Press [ENTER] To Exit...
""")

def show():
    import main
    import utils
    printMenu()
    utils.getNextKey()
    main.switchToMain(0)