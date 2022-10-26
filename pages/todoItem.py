from pyfiglet import Figlet
from colorama import Fore, Back, Style

class TodoItemPage:

    def __init__(self, main, utils, item):
        self.item = item
        self.main = main
        self.utils = utils
        self.editingDesc = False
        self.editingDescOption = 0

    # Oh boy, here we go.
    # This method performs all the formatting and printing based on the many, many different possible
    # states of the menu, its not the cleanest but it works and is relyable 
    def printMenu(self, selectedOption):

        # Keeps track of what options are usable based on the state of the menu
        canEdit = False
        canLeft = False
        canRight = False
        canUp = True
        canDown = True

        # Title time!
        self.utils.clear()
        f = Figlet(font='cybermedium')
        print (f.renderText('Item:'))

        # The main title value
        if(selectedOption == 0):
            # The title value is selected so we show what options are avaible and print it
            canEdit = True
            canUp = False
            print("> Title: \n    {0}".format(self.item["value"]))
        else:
            print("  Title: \n    {0}".format(self.item["value"]))

        if(selectedOption == 1):
            # The description has 2 possible states for if we are editing it or not
            if(self.editingDesc):
                # Here we are editing the description so a bunch fore logic is ran for
                # indivual item selection and new line creation
                canEdit = True
                print("\n> Description:")
                if(self.editingDescOption == 0):
                    canUp = False
                
                # Print all the lines
                for i in range(len(self.item["description"])):
                    # If its selected we format it with a >
                    if(self.editingDescOption == i):
                        print("  > " + self.item["description"][i])
                    else:
                        print("    " + self.item["description"][i])
                
                # At the end we add a new option for the user to use for new lines
                if(self.editingDescOption == len(self.item["description"])):
                    canDown = False
                    print("  > " + Style.DIM + "[+] New Line" + Style.RESET_ALL)
                else:
                    print(Style.DIM + "    [+] New Line" + Style.RESET_ALL)
                
            else:
                canEdit = True
                print("\n> Description: \n    {0}".format('\n    '.join(self.item["description"])))
        else:
            print("\n  Description: \n    {0}".format('\n    '.join(self.item["description"])))
        
        if(selectedOption == 2):
            # This is when the status is selected, when it is we show the other availible options besides it dimmed out
            # Makes it easy for the user to see what they are cycling too
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
        
        # Same kind of logic as the status but for the completed mark
        # This just sets our 2 values depending on what needs to be shown
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
        
        # At the end we print our menu with all the options grayed out if they arent a valid input
        print("""\n
    [B] Back      {0}[Enter] Edit{1}
    {2}[↑] Move Up{3}   {4}[↓] Move Down{5}
    {6}[←] Move Left{7} {8}[→] Move Right{9}
    """.format(self.utils.resolveBoolToDimOrNormal(canEdit), 
        Style.RESET_ALL, 
        self.utils.resolveBoolToDimOrNormal(canUp), 
        Style.RESET_ALL,
        self.utils.resolveBoolToDimOrNormal(canDown), 
        Style.RESET_ALL,
        self.utils.resolveBoolToDimOrNormal(canLeft), 
        Style.RESET_ALL,
        self.utils.resolveBoolToDimOrNormal(canRight), 
        Style.RESET_ALL
        ) + Style.RESET_ALL)

        # DEBUG PRINTING
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
        self.main.debugPrint("EditDesc?: " + str(self.editingDesc))
        self.main.debugPrint("EditDescValue: " + str(self.editingDescOption))
        self.main.debugPrint("DescLen: " + str(len(self.item["description"])))


    # Main controller for the menu, has 2 different operation modes for if we are editing the 
    # description or not, switches based on user selection the description or exiting
    def show(self, selectedOption):
        self.printMenu(selectedOption)
        value = self.utils.getNextKey()
        if (self.editingDesc != True):
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
            elif(value == self.utils.Controls.ENTER and selectedOption == 0):
                self.editTitle(selectedOption)
            elif(value == self.utils.Controls.ENTER and selectedOption == 1):
                self.editDescription(0)
            else:
                self.show(selectedOption)
        else:
            if(value == self.utils.Controls.DOWN):
                if self.editingDescOption < len(self.item["description"]):
                    self.editingDescOption += 1
                    self.show(1)
                else:
                    self.show(1)
            elif(value == self.utils.Controls.UP):
                if self.editingDescOption > 0:
                    self.editingDescOption -= 1
                    self.show(1)
                else:
                    self.show(1)
            elif(value == self.utils.Controls.BACK):
                self.editingDesc = False
                self.show(selectedOption)
            # Detects if its the new item thats selected
            elif(value == self.utils.Controls.ENTER and self.editingDescOption == len(self.item["description"])):
                self.newDescriptionValue()
            elif(value == self.utils.Controls.ENTER):
                self.editDescriptionValue(self.editingDescOption)
            else:
                self.show(selectedOption)

    # Allows us to easily cycle the status of the item in this menu
    def cycleStatus(self, selectedOption, direction):
        print("Updating...")
        if direction == 1:
            self.item["colour"] = self.utils.findNextColour(self.item["colour"])
        else:
            self.item["colour"] = self.utils.findPreviousColour(self.item["colour"])
        self.main.saveItemToDB(self.item)
        self.show(selectedOption)

    # Simple function to toggle if the item is completed or not
    def toggleComplete(self, selectedOption):
        print("Updating...")
        if self.item["completed"]:
            self.item["completed"] = False
        else:
            self.item["completed"] = True
        self.main.saveItemToDB(self.item)
        self.show(selectedOption)

    # Creates a small sub-menu for editing the title value
    # shows the old value for the user to see then saves it
    def editTitle(self, selectedOption):
        self.utils.clear()

        f = Figlet(font='cybermedium')
        print (f.renderText('Edit Title:'))

        defaultValue = self.item["value"]
        print("Current Value: \n  " + defaultValue + "\n")
        print("Leave blank to cancel the edit")
        answer = input("\nEnter New Value: \n  ")

        if(answer != ""):
            print("\nUpdating...")
            self.item["value"] = answer
            self.main.saveItemToDB(self.item)
            self.show(selectedOption)
        else:
            self.show(selectedOption)
    
    # Enters the edit description mode
    def editDescription(self, descOption):
        self.editingDescOption = descOption
        self.editingDesc = True
        self.show(1)
    
    # Creates another sub-menu for editing the description value
    # This also allows delection of the value enterley
    def editDescriptionValue(self, descOption):
        self.utils.clear()

        f = Figlet(font='cybermedium')
        print (f.renderText('Edit Line:'))

        defaultValue = self.item["description"][descOption]
        print("Current Value: \n  " + defaultValue + "\n")
        print("Leave blank to cancel the edit")
        print("Enter \"DELETE\" to remove line")
        answer = input("\nEnter New Value: \n  ")

        if(answer == ""):
            self.show(1)
        elif(answer == "DELETE"):
            print("\nUpdating...")
            self.item["description"].pop(descOption)
            self.main.saveItemToDB(self.item)
            self.show(1)
        else:
            print("\nUpdating...")
            self.item["description"][descOption] = answer
            self.main.saveItemToDB(self.item)
            self.show(1)
    
    # Same as above but for new values only
    def newDescriptionValue(self):
        self.utils.clear()

        f = Figlet(font='cybermedium')
        print (f.renderText('New Line:'))

        print("\nLeave blank to cancel the edit")
        answer = input("\nEnter New Value: \n  ")

        if(answer != ""):
            print("\nUpdating...")
            self.item["description"].append(answer)
            self.main.saveItemToDB(self.item)
            self.show(1)
        else:
            self.show(1)