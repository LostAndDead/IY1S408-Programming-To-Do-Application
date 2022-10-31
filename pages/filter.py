from re import M
from pyfiglet import Figlet
from colorama import Fore, Back, Style

class FilterPage:

    def __init__(self, main, utils):
        self.main = main
        self.utils = utils
        self.selectedOption = 0
        self.colourFilter = None
        self.completedFilter = None

    def printMenu(self):
        self.utils.clear()
        f = Figlet(font='cybermedium')
        print (f.renderText('Filter:'))

        canUp = False
        canDown = False
        canLeft = False
        canRight = False

        if(self.selectedOption == 0):
            canDown = True
            canLeft = True
            canRight = True
            if(self.colourFilter == None):
                print("> Status: " + 
            Style.RESET_ALL + Style.DIM + " [{0}■".format(self.utils.resolveColour(self.utils.findPreviousColour("red"))) + Style.RESET_ALL + Style.DIM + "]" +
            Style.RESET_ALL + " [{0}■".format(Fore.BLACK + Style.BRIGHT) + Style.RESET_ALL + "]" + 
            Style.RESET_ALL + Style.DIM + " [{0}■".format(self.utils.resolveColour(self.utils.findNextColour("red"))) + Style.RESET_ALL + Style.DIM + "]" + 
            Style.RESET_ALL
            )
            else:
                print("> Status: " + 
            Style.RESET_ALL + Style.DIM + " [{0}■".format(self.utils.resolveColour(self.utils.findPreviousColour(self.colourFilter))) + Style.RESET_ALL + Style.DIM + "]" +
            Style.RESET_ALL + " [{0}■".format(self.utils.resolveColour(self.colourFilter)) + Style.RESET_ALL + "]" + 
            Style.RESET_ALL + Style.DIM + " [{0}■".format(self.utils.resolveColour(self.utils.findNextColour(self.colourFilter))) + Style.RESET_ALL + Style.DIM + "]" + 
            Style.RESET_ALL
            )
        else:
            if(self.colourFilter == None):
                print("  Status: " + Style.RESET_ALL + " [{0}■".format(Fore.BLACK + Style.BRIGHT) + Style.RESET_ALL + "]")
            else:
                print("  Status: " + Style.RESET_ALL + " [{0}■".format(self.utils.resolveColour(self.colourFilter)) + Style.RESET_ALL + "]")
        
        completed = Fore.RED + Style.BRIGHT + "✗" + Style.RESET_ALL
        altCompleted = Fore.GREEN + Style.BRIGHT + "✓" + Style.RESET_ALL
        if self.completedFilter == True:
            completed = Fore.GREEN + Style.BRIGHT + "✓" + Style.RESET_ALL
            altCompleted = Fore.RED + Style.BRIGHT + "✗" + Style.RESET_ALL
        if(self.selectedOption == 1):
            canUp = True
            if(self.completedFilter == None):
                canLeft = True
                canRight = True
                print("\n> Completed: " + 
            Style.RESET_ALL + Style.DIM + " [{0}".format(completed) + Style.RESET_ALL + Style.DIM + "]" +
            Style.RESET_ALL + " [{0}■".format(Fore.BLACK + Style.BRIGHT) + Style.RESET_ALL + "]" + 
            Style.RESET_ALL + Style.DIM + " [{0}".format(altCompleted) + Style.RESET_ALL + Style.DIM + "]" + 
            Style.RESET_ALL
            )
            else:
                if self.completedFilter:
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
            if(self.completedFilter == None):
                print("\n  Completed: " + Style.RESET_ALL + " [{0}■".format(Fore.BLACK + Style.BRIGHT) + Style.RESET_ALL + "]")
            else:
                print("\n  Completed: " + Style.RESET_ALL + " [{0}".format(completed) + Style.RESET_ALL + "]")
        print("""\n
    [B] Back      [D] Clear
    {0}[↑] Move Up{1}   {2}[↓] Move Down{3}
    {4}[←] Move Left{5} {6}[→] Move Right{7}
    """.format(self.utils.resolveBoolToDimOrNormal(canUp),
    Style.RESET_ALL,
    self.utils.resolveBoolToDimOrNormal(canDown),
    Style.RESET_ALL,
    self.utils.resolveBoolToDimOrNormal(canLeft),
    Style.RESET_ALL,
    self.utils.resolveBoolToDimOrNormal(canRight),
    Style.RESET_ALL
    ) + Style.RESET_ALL)

        self.main.debugPrint("\nDEBUG MODE ACTIVE\n")
        self.main.debugPrint("SelectedOption: " + str(self.selectedOption))
        self.main.debugPrint("colourFilter: " + str(self.colourFilter))
        self.main.debugPrint("completedFilter: " + str(self.completedFilter))

    def show(self):
        self.printMenu()
        value = self.utils.getNextKey()
        if(value == self.utils.Controls.DOWN):
            # Make sure we stay within the valid options
            if self.selectedOption < 1:
                self.selectedOption += 1
                self.show()
            else:
                self.show()
        elif(value == self.utils.Controls.UP):
            # Make sure we stay within the valid options
            if self.selectedOption > 0:
                self.selectedOption -= 1
                self.show()
            else:
                self.show()
        elif(value == self.utils.Controls.BACK):
            self.main.switchToToDo(0)
        elif(value == self.utils.Controls.LEFT and self.selectedOption == 0):
            self.cycleStatus(-1)
        elif(value == self.utils.Controls.RIGHT and self.selectedOption == 0):
            self.cycleStatus(1)
        elif(value == self.utils.Controls.LEFT and self.selectedOption == 1 and (self.completedFilter == True or self.completedFilter == None)):
            if(self.completedFilter == None):
                self.completedFilter = False
            else:
                self.completedFilter = not self.completedFilter
            self.show()
        elif(value == self.utils.Controls.RIGHT and self.selectedOption == 1 and (self.completedFilter == False or self.completedFilter == None)):
            if(self.completedFilter == None):
                self.completedFilter = True
            else:
                self.completedFilter = not self.completedFilter
            self.show()
        elif(value == self.utils.Controls.DELETE and self.selectedOption == 0):
            self.colourFilter = None
            self.show()
        elif(value == self.utils.Controls.DELETE and self.selectedOption == 1):
            self.completedFilter = None
            self.show()
        else:
            self.show()
    
    def cycleStatus(self, direction):
        if(self.colourFilter == None):
            self.colourFilter = "red"
        if direction == 1:
            self.colourFilter = self.utils.findNextColour(self.colourFilter)
        else:
            self.colourFilter = self.utils.findPreviousColour(self.colourFilter)
        self.show()

    def getColourFilter(self):
        return self.colourFilter
    
    def getCompleteFilter(self):
        return self.completedFilter
