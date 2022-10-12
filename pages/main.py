from pyfiglet import Figlet
from colorama import Fore, Back, Style

menuOptions = ["1. View To-Do Tasks", "2. Options", "3. Credits", "4. Close"]

# Function to print the main menu of the program
def printMenu(selectedOption):
    import main
    import utils
    utils.clear()
    f = Figlet(font='cybermedium')
    print (f.renderText('To-Do:'))   
    for i in range(len(menuOptions)):
        if(i == selectedOption):
            print("> " + menuOptions[i] + Style.RESET_ALL)
        else:
            print("  " + menuOptions[i] + Style.RESET_ALL)
    print("""\n
[CTRL] Exit   [Enter] Choose
[↑] Move Up   [↓] Move Down
""")

# The start of the program, prints out main menu and waits for the users input
def show(selectedOption):
    import main
    import utils
    printMenu(selectedOption)
    value = utils.getNextKey()
    if(value == utils.Controls.DOWN):
        # Make sure we stay within the valid options
        if selectedOption < len(menuOptions) - 1:
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
        if(selectedOption == 0):
            selectedOption = 0
            main.switchToToDo(0)
        elif(selectedOption == 2):
            main.switchToCreditsPage()
        elif(selectedOption == 3):
            utils.clear()
            print("Have a good day o/")
            exit()
        else:
            print("Selected {0}".format(menuOptions[selectedOption]))
    elif(value == utils.Controls.Exit):
        # Nice and cleanly exit the program
        utils.clear()
        print("Have a good day o/")
        exit()
    else:
        show(selectedOption)