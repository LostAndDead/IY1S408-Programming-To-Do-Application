from pyfiglet import Figlet
from colorama import Fore, Back, Style

global todoItems
todoItems = []

def printToDo(selectedOption):
    import utils
    global todoItems
    utils.clear()
    f = Figlet(font='cybermedium')
    print (f.renderText('To-Do:'))

    print("  Text                          Completed    Status")
    print("-----------------------------------------------------")
    for i in range(len(todoItems)):
        value = todoItems[i]["value"]
        completed = Fore.RED + "✗" + Style.RESET_ALL
        if todoItems[i]["completed"]:
            completed = Fore.GREEN + "✓" + Style.RESET_ALL
        if len(value) > 30:
            value = value[0:27] + "..."
        elif len(value) < 30:
            while len(value) < 30:
                value = value + " "
        if(i == selectedOption):
            print("> " + value + Style.RESET_ALL + "   [{0}]         [{1}■".format(completed, utils.resolveColour(todoItems[i]["colour"])) + Style.RESET_ALL +  "]")
        else:
            print("  " + value + Style.RESET_ALL + "   [{0}]         [{1}■".format(completed, utils.resolveColour(todoItems[i]["colour"])) + Style.RESET_ALL + "]")
    print("""\n
[B] Back      [Enter] Edit
[↑] Move Up   [↓] Move Down
[N] New       [C] Change Status
[D] Delete    [T] Complete/Uncomplete
""")
    print(todoItems)

def show(selectedOption):
    import main
    import utils
    global todoItems
    printToDo(selectedOption)
    value = utils.getNextKey()
    if(value == utils.Controls.DOWN):
        # Make sure we stay within the valid options
        if selectedOption < len(todoItems) - 1:
            selectedOption += 1
            show(selectedOption)
        else:
            show(selectedOption)
    elif(value == utils.Controls.UP):
        # Make sure we stay within the valid options
        if selectedOption > 0:
            selectedOption -= 1
            show(selectedOption)
        else:
            show(selectedOption)
    elif(value == utils.Controls.ENTER):
        # Temporary
        print("Selected {0}".format(todoItems[selectedOption]["value"]))
    elif(value == utils.Controls.BACK):
        # Go back to the main menu
        main.switchToMain(0)
    elif(value == utils.Controls.CYCLE):
        cycleStatus(selectedOption)
    elif(value == utils.Controls.TOGGLE):
        toggleComplete(selectedOption)
    elif(value == utils.Controls.DELETE):
        deleteItem(selectedOption)
    else:
        show(selectedOption)

def setTodoItems(items):
    global todoItems
    todoItems = items

def cycleStatus(selectedOption):
    print("Updating...")
    import main
    import utils
    global todoItems
    item = todoItems[selectedOption]
    item["colour"] = utils.findNextColour(item["colour"])
    todoItems[selectedOption] = item
    main.saveItemToDB(item)
    show(selectedOption)

def toggleComplete(selectedOption):
    print("Updating...")
    import main
    global todoItems
    item = todoItems[selectedOption]
    if item["completed"]:
        item["completed"] = False
    else:
        item["completed"] = True
    todoItems[selectedOption] = item
    main.saveItemToDB(item)
    show(selectedOption)

def deleteItem(selectedOption):
    import utils
    utils.clear()
    print("Are you sure? [Y/N]")
    value = utils.getNextKey()
    if(value == utils.Controls.YES):
        confirmDeleteItem(selectedOption)
    else:
        show(selectedOption)


def confirmDeleteItem(selectedOption):
    import main
    print("Deleting...")
    global todoItems
    item = todoItems[selectedOption]
    todoItems.pop(selectedOption)
    main.removeItemFromDB(item)
    show(selectedOption)