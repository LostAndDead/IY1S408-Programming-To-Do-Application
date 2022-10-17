from pyfiglet import Figlet
from colorama import Fore, Back, Style

class TodoPage:

    def __init__(self, main, utils, todoItems):
        self.todoItems = todoItems
        self.main = main
        self.utils = utils

    def printToDo(self, selectedOption):
        self.utils.clear()
        f = Figlet(font='cybermedium')
        print (f.renderText('To-Do:'))
        print("  Text                          Completed    Status")
        print("-----------------------------------------------------")
        for i in range(len(self.todoItems)):
            value = self.todoItems[i]["value"]
            completed = Fore.RED + Style.BRIGHT + "✗" + Style.RESET_ALL
            if self.todoItems[i]["completed"]:
                completed = Fore.GREEN + Style.BRIGHT + "✓" + Style.RESET_ALL
            if len(value) > 30:
                value = value[0:27] + "..."
            elif len(value) < 30:
                while len(value) < 30:
                    value = value + " "
            if(i == selectedOption):
                print("> " + value + Style.RESET_ALL + "   [{0}]         [{1}■".format(completed, self.utils.resolveColour(self.todoItems[i]["colour"])) + Style.RESET_ALL +  "]")
            else:
                print("  " + value + Style.RESET_ALL + "   [{0}]         [{1}■".format(completed, self.utils.resolveColour(self.todoItems[i]["colour"])) + Style.RESET_ALL + "]")
        print("""\n
    [B] Back      [Enter] Edit
    [↑] Move Up   [↓] Move Down
    [N] New       [C] Change Status
    [D] Delete    [T] Complete/Uncomplete
    """)
        self.main.debugPrint("\nDEBUG MODE ACTIVE\n")
        self.main.debugPrint("SelectedOption = " + str(selectedOption))
        self.main.debugPrint(self.todoItems)

    def show(self, selectedOption):
        self.printToDo(selectedOption)
        value = self.utils.getNextKey()
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
            self.main.switchToTodoItem(self.todoItems[selectedOption], 0 )
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

    def setTodoItems(self, items):
        self.todoItems = items

    def cycleStatus(self, selectedOption):
        print("Updating...")
        item = self.todoItems[selectedOption]
        item["colour"] = self.utils.findNextColour(item["colour"])
        self.todoItems[selectedOption] = item
        self.main.saveItemToDB(item)
        self.show(selectedOption)

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

    def deleteItem(self, selectedOption):
        self.utils.clear()
        print("Are you sure? [Y/N]")
        value = self.utils.getNextKey()
        if(value == self.utils.Controls.YES):
            self.confirmDeleteItem(selectedOption)
        else:
            self.show(selectedOption)


    def confirmDeleteItem(self, selectedOption):
        print("Deleting...")
        item = self.todoItems[selectedOption]
        self.todoItems.pop(selectedOption)
        self.main.removeItemFromDB(item)
        self.show(selectedOption)