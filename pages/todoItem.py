from pyfiglet import Figlet
from colorama import Fore, Back, Style

class TodoItemPage:

    def __init__(self, main, utils, item):
        self.item = item
        self.main = main
        self.utils = utils

    def printMenu(self, selectedOption):
        canEdit = False
        canLeft = False
        canRight = False
        canUp = True
        canDown = True
        self.utils.clear()
        f = Figlet(font='cybermedium')
        print (f.renderText('Item:'))

        if(selectedOption == 0):
            canEdit = True
            canUp = False
            print("> Text: \n  {0}".format(self.item["value"]))
        else:
            print("  Text: \n  {0}".format(self.item["value"]))
        if(selectedOption == 1):
            canEdit = True
            print("> Description: \n  {0}".format('\n  '.join(self.item["description"])))
        else:
            print("  Description: \n  {0}".format('\n  '.join(self.item["description"])))
        if(selectedOption == 2):
            canLeft = True
            canRight = True
            print("\n> Status: " + 
            Style.RESET_ALL + Style.DIM + " [{0}■".format(self.utils.resolveColour(self.utils.findPreviousColour(self.item["colour"]))) + Style.RESET_ALL + Style.DIM + "]" +
            Style.RESET_ALL + " [{0}■".format(self.utils.resolveColour(self.item["colour"])) + Style.RESET_ALL + "]" + 
            Style.RESET_ALL + Style.DIM + " [{0}■".format(self.utils.resolveColour(self.utils.findNextColour(self.item["colour"]))) + Style.RESET_ALL + Style.DIM + "]" + 
            Style.RESET_ALL
            )
        else:
            print("\n  Status: [{0}■".format(self.utils.resolveColour(self.item["colour"])) + Style.RESET_ALL + "]")
        
        completed = Fore.RED + Style.BRIGHT + "✗" + Style.RESET_ALL
        altCompleted = Fore.GREEN + Style.BRIGHT + "✓" + Style.RESET_ALL
        if self.item["completed"]:
            completed = Fore.GREEN + Style.BRIGHT + "✓" + Style.RESET_ALL
            altCompleted = Fore.RED + Style.BRIGHT + "✗" + Style.RESET_ALL
        if(selectedOption == 3):
            canDown = False
            if self.item["completed"]:
                canLeft = True
                print("\n> Completed: " + Style.DIM + "[{0}".format(altCompleted) + Style.RESET_ALL + Style.DIM + "]" + 
                Style.RESET_ALL + " [{0}".format(completed) + Style.RESET_ALL + "]" + Style.RESET_ALL + 
                Style.RESET_ALL
                )
            else:
                canRight = True
                print("\n> Completed: " + "[{0}".format(completed) + Style.RESET_ALL + "]" + 
                Style.DIM + " [{0}".format(altCompleted) + Style.RESET_ALL + Style.DIM + "]" + 
                Style.RESET_ALL
                )
        else:
            print("\n  Completed: [{0}".format(completed) + Style.RESET_ALL + "]")
        print("""\n
    [B] Back      {0}[Enter] Edit{1}
    {2}[↑] Move Up{3}   {4}[↓] Move Down{5}
    {6}[←] Move Left{7} {8}[→] Move Right{9}
    """.format(self.resolveCanEditOrArrow(canEdit), 
        Style.RESET_ALL, 
        self.resolveCanEditOrArrow(canUp), 
        Style.RESET_ALL,
        self.resolveCanEditOrArrow(canDown), 
        Style.RESET_ALL,
        self.resolveCanEditOrArrow(canLeft), 
        Style.RESET_ALL,
        self.resolveCanEditOrArrow(canRight), 
        Style.RESET_ALL
        ) + Style.RESET_ALL)

        self.main.debugPrint("\nDEBUG MODE ACTIVE\n")
        self.main.debugPrint("SelectedOption = " + str(selectedOption))
        self.main.debugPrint(self.item)
        self.main.debugPrint("Complete: " + completed)
        self.main.debugPrint("AltComplete: " + altCompleted)
        self.main.debugPrint("Edit?: " + str(canEdit))
        self.main.debugPrint("Left?: " + str(canLeft))
        self.main.debugPrint("Right?: " + str(canRight))
        self.main.debugPrint("Up?: " + str(canUp))
        self.main.debugPrint("Down?: " + str(canDown))


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
        elif(value == self.utils.Controls.LEFT and selectedOption == 2):
            self.cycleStatus(selectedOption, -1)
        elif(value == self.utils.Controls.RIGHT and selectedOption == 2):
            self.cycleStatus(selectedOption, 1)
        elif(value == self.utils.Controls.LEFT and selectedOption == 3 and self.item["completed"] == True):
            self.toggleComplete(selectedOption)
        elif(value == self.utils.Controls.RIGHT and selectedOption == 3 and self.item["completed"] == False):
            self.toggleComplete(selectedOption)
        else:
            self.show(selectedOption)
    
    def cycleStatus(self, selectedOption, direction):
        print("Updating...")
        if direction == 1:
            self.item["colour"] = self.utils.findNextColour(self.item["colour"])
        else:
            self.item["colour"] = self.utils.findPreviousColour(self.item["colour"])
        self.main.saveItemToDB(self.item)
        self.show(selectedOption)

    def toggleComplete(self, selectedOption):
        print("Updating...")
        if self.item["completed"]:
            self.item["completed"] = False
        else:
            self.item["completed"] = True
        self.main.saveItemToDB(self.item)
        self.show(selectedOption)

    def resolveCanEditOrArrow(self, bool):
        if bool:
            return Style.NORMAL
        else:
            return Style.DIM