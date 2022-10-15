from pyfiglet import Figlet
from colorama import Fore, Back, Style

class MainPage:

    def __init__(self, main, utils,):
        self.menuOptions = ["1. View To-Do Tasks", "2. Options", "3. Credits", "4. Close"]
        self.main = main
        self.utils = utils

    # Function to print the main menu of the program
    def printMenu(self, selectedOption):
        self.utils.clear()
        f = Figlet(font='cybermedium')
        print (f.renderText('To-Do:'))   
        for i in range(len(self.menuOptions)):
            if(i == selectedOption):
                print("> " + self.menuOptions[i] + Style.RESET_ALL)
            else:
                print("  " + self.menuOptions[i] + Style.RESET_ALL)
        print("""\n
    [CTRL] Exit   [Enter] Choose
    [↑] Move Up   [↓] Move Down
    """)
        self.main.debugPrint("\nDEBUG MODE ACTIVE\n")
        self.main.debugPrint("SelectedOption = " + str(selectedOption))

    # The start of the program, prints out main menu and waits for the users input
    def show(self, selectedOption):
        self.printMenu(selectedOption)
        value = self.utils.getNextKey()
        if(value == self.utils.Controls.DOWN):
            # Make sure we stay within the valid options
            if selectedOption < len(self.menuOptions) - 1:
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
            if(selectedOption == 0):
                selectedOption = 0
                self.main.switchToToDo(0)
            elif(selectedOption == 2):
                self.main.switchToCreditsPage()
            elif(selectedOption == 3):
                self.utils.clear()
                print("Have a good day o/")
                exit()
            else:
                print("Selected {0}".format(self.menuOptions[selectedOption]))
        elif(value == self.utils.Controls.Exit):
            # Nice and cleanly exit the program
            self.utils.clear()
            print("Have a good day o/")
            exit()
        else:
            self.show(selectedOption)