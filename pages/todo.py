from pyfiglet import Figlet
from colorama import Fore, Back, Style

class TodoPage:

    # Initilize the ToDo page, needs a list of items
    # as well as a link to the main and utils classes
    def __init__(self, main, utils, todoItems):
        self.todoItems = todoItems
        self.main = main
        self.utils = utils

    def printToDo(self, selectedOption):
        self.utils.clear()

        canUp = True
        canDown = True

        # Prints the page header in a Figlet font
        f = Figlet(font='cybermedium')
        print (f.renderText('To-Do:'))
        print("  Text                          Completed    Status")
        print("-----------------------------------------------------")

        # Loops over all the items and prints them to the screen with formatting logic
        for i in range(len(self.todoItems)):
            

            # Choose weather the ✓ or ✗ should be used based on the items completed status
            completed = Fore.RED + Style.BRIGHT + "✗" + Style.RESET_ALL
            if self.todoItems[i]["completed"]:
                completed = Fore.GREEN + Style.BRIGHT + "✓" + Style.RESET_ALL

            # Here we crop the value of the item down to 30 chars, to keep nice formatting
            value = self.todoItems[i]["value"]
            if len(value) > 30:
                value = value[0:27] + "..."

            # If its shorter than 30 we pad it out with spaces for formatting
            elif len(value) < 30:
                while len(value) < 30:
                    value = value + " "
            
            # Simple > or not depending if its selected
            if(i == selectedOption):
                print("> " + value + Style.RESET_ALL + "   [{0}]         [{1}■".format(completed, self.utils.resolveColour(self.todoItems[i]["colour"])) + Style.RESET_ALL +  "]")
            else:
                print("  " + value + Style.RESET_ALL + "   [{0}]         [{1}■".format(completed, self.utils.resolveColour(self.todoItems[i]["colour"])) + Style.RESET_ALL + "]")
        
        # Detects if up or down controlls will work
        if selectedOption == len(self.todoItems) -1:
            canDown = False
        if selectedOption == 0:
            canUp = False

        # Prints the controlls, also dims out controls which arent useable right now
        print("""\n
    [B] Back      [Enter] Edit
    {0}[↑] Move Up{1}   {2}[↓] Move Down{3}
    [N] New       [C] Change Status
    [D] Delete    [T] Complete/Uncomplete
    """.format(self.utils.resolveBoolToDimOrNormal(canUp),
        Style.RESET_ALL,
        self.utils.resolveBoolToDimOrNormal(canDown),
        Style.RESET_ALL
        ) + Style.RESET_ALL)

        # DEBUG PRINTING
        self.main.debugPrint("\nDEBUG MODE ACTIVE\n")
        self.main.debugPrint("SelectedOption = " + str(selectedOption))
        self.main.debugPrint(self.todoItems)

    def show(self, selectedOption):
        # Print the menu then wait for key input
        self.printToDo(selectedOption)
        value = self.utils.getNextKey()

        # Now we have the key input we can proccess it
        if(value == self.utils.Controls.DOWN):
            # Make sure we stay within the valid options
            if selectedOption < len(self.todoItems) - 1:
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
        elif(value == self.utils.Controls.ENTER):
            # User has selected an item, lets switch to it
            self.main.switchToTodoItem(self.todoItems[selectedOption], 0)
        elif(value == self.utils.Controls.BACK):
            # Go back to the main menu
            self.main.switchToMain(0)
        elif(value == self.utils.Controls.CYCLE):
            self.cycleStatus(selectedOption)
        elif(value == self.utils.Controls.TOGGLE):
            self.toggleComplete(selectedOption)
        elif(value == self.utils.Controls.DELETE):
            self.deleteItem(selectedOption)
        else:
            self.show(selectedOption)

    # UNUSED, sets the todo items if they need updating for any reason
    def setTodoItems(self, items):
        self.todoItems = items

    # Allows us to easily cycle the status of the item in this menu
    def cycleStatus(self, selectedOption):
        print("Updating...")
        item = self.todoItems[selectedOption]
        item["colour"] = self.utils.findNextColour(item["colour"])
        self.todoItems[selectedOption] = item
        self.main.saveItemToDB(item)
        self.show(selectedOption)

    # Simple function to toggle if the item is completed or not
    def toggleComplete(self, selectedOption):
        print("Updating...")
        item = self.todoItems[selectedOption]
        if item["completed"]:
            item["completed"] = False
        else:
            item["completed"] = True
        self.todoItems[selectedOption] = item
        self.main.saveItemToDB(item)
        self.show(selectedOption)

    # Delete function, makes sure the user is certain for it confirms the delete
    def deleteItem(self, selectedOption):
        self.utils.clear()
        print("Are you sure? [Y/N]")
        value = self.utils.getNextKey()
        if(value == self.utils.Controls.YES):
            self.confirmDeleteItem(selectedOption)
        else:
            self.show(selectedOption)

    # The user is sure, and the item is gone!
    def confirmDeleteItem(self, selectedOption):
        print("Deleting...")
        item = self.todoItems[selectedOption]
        self.todoItems.pop(selectedOption)
        self.main.removeItemFromDB(item)
        self.show(selectedOption)