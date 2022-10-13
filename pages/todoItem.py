from pyfiglet import Figlet
from colorama import Fore, Back, Style

def printMenu(item, selectedOption):
    import utils
    utils.clear()
    f = Figlet(font='cybermedium')
    print (f.renderText('Item:'))
    
    if(selectedOption == 0):
        print("> Text: \n  {0}".format(item["value"]))
    else:
        print("  Text: \n  {0}".format(item["value"]))
    if(selectedOption == 1):
        print("> Description: \n  {0}".format('\n  '.join(item["description"])))
    else:
        print("  Description: \n  {0}".format('\n  '.join(item["description"])))
    if(selectedOption == 2):
        print("\n> Status: [{0}■".format(utils.resolveColour(item["colour"])) + Style.RESET_ALL + "]")
    else:
        print("\n  Status: [{0}■".format(utils.resolveColour(item["colour"])) + Style.RESET_ALL + "]")
    completed = Fore.RED + "✗" + Style.RESET_ALL
    if item["completed"]:
        completed = Fore.GREEN + "✓" + Style.RESET_ALL
    if(selectedOption == 3):
        print("\n> Completed: [{0}".format(completed) + Style.RESET_ALL + "]")
    else:
        print("\n  Completed: [{0}".format(completed) + Style.RESET_ALL + "]")
    print("""\n
[B] Back      [Enter] Edit/Cycle/Toggle
[↑] Move Up   [↓] Move Down
""")


def show(item, selectedOption):
    import main
    import utils
    printMenu(item, selectedOption)
    value = utils.getNextKey()
    if(value == utils.Controls.DOWN):
        # Make sure we stay within the valid options
        if selectedOption < 3:
            selectedOption += 1
            show(item, selectedOption)
        else:
            show(item, selectedOption)
    elif(value == utils.Controls.UP):
        # Make sure we stay within the valid options
        if selectedOption > 0:
            selectedOption -= 1
            show(item, selectedOption)
        else:
            show(item, selectedOption)
    elif(value == utils.Controls.BACK):
        # Go back to the main menu
        main.switchToToDo(0)
    else:
        show(item, selectedOption)