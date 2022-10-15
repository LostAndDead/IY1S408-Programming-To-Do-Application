from pyfiglet import Figlet
from colorama import Fore, Back, Style

class TodoItemPage:

    def __init__(self, main, utils, item):
        self.item = item
        self.main = main
        self.utils = utils

    def printMenu(self, selectedOption):
        self.utils.clear()
        f = Figlet(font='cybermedium')
        print (f.renderText('Item:'))

        if(selectedOption == 0):
            print("> Text: \n  {0}".format(self.item["value"]))
        else:
            print("  Text: \n  {0}".format(self.item["value"]))
        if(selectedOption == 1):
            print("> Description: \n  {0}".format('\n  '.join(self.item["description"])))
        else:
            print("  Description: \n  {0}".format('\n  '.join(self.item["description"])))
        if(selectedOption == 2):
            print("\n> Status: [{0}■".format(self.utils.resolveColour(self.item["colour"])) + Style.RESET_ALL + "]")
        else:
            print("\n  Status: [{0}■".format(self.utils.resolveColour(self.item["colour"])) + Style.RESET_ALL + "]")
        completed = Fore.RED + "✗" + Style.RESET_ALL
        if self.item["completed"]:
            completed = Fore.GREEN + "✓" + Style.RESET_ALL
        if(selectedOption == 3):
            print("\n> Completed: [{0}".format(completed) + Style.RESET_ALL + "]")
        else:
            print("\n  Completed: [{0}".format(completed) + Style.RESET_ALL + "]")
        print("""\n
    [B] Back      [Enter] Edit/Cycle/Toggle
    [↑] Move Up   [↓] Move Down
    """)
        self.main.debugPrint("\nDEBUG MODE ACTIVE\n")
        self.main.debugPrint("SelectedOption = " + str(selectedOption))
        self.main.debugPrint(self.item)


    def show(self, selectedOption):
        self.printMenu(selectedOption)
        value = self.utils.getNextKey()
        if(value == self.utils.Controls.DOWN):
            # Make sure we stay within the valid options
            if selectedOption < 3:
                selectedOption += 1
                self.show(selectedOption)
            else:
                self.show(selectedOption)
        elif(value == self.utils.Controls.UP):
            # Make sure we stay within the valid options
            if selectedOption > 0:
                selectedOption -= 1
                self.show(selectedOption)
            else:
                self.show(selectedOption)
        elif(value == self.utils.Controls.BACK):
            # Go back to the main menu
            self.main.switchToToDo(0)
        else:
            self.show(selectedOption)