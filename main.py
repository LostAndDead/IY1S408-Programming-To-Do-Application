from json import load
from msilib.schema import ComboBox
from xmlrpc.client import Boolean
from colorama import Fore, Back, Style
from enum import Enum
from pynput import keyboard
import os
from pyfiglet import Figlet
from pymongo import MongoClient

class Controls(Enum):
    Exit = -1
    Nothing = 0
    UP = 1
    DOWN = 2
    ENTER = 3
    BACK = 4

global menuOptions, selectedOption, pressedKey, listener, todoItems, colourOptions

menuOptions = ["1. View To-Do Tasks", "2. Options", "3. Credits", "4. Close"]
colourOptions = ["red", "green"]
selectedOption = 0
pressedKey = Controls.Nothing
listener = keyboard.Listener()
todoItems = []

# Reusable function for clearing the screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to print the main menu of the program
def printMainMenu():
    clear()
    f = Figlet(font='cybermedium')
    print (f.renderText('To-Do'))   
    global menuOptions, selectedOption
    for i in range(len(menuOptions)):
        if(i == selectedOption):
            print("> " + menuOptions[i] + Style.RESET_ALL)
        else:
            print("  " + menuOptions[i] + Style.RESET_ALL)
    print("""\n
[CTRL] Exit   [Enter] Choose
[↑] Move Up   [↓] Move Down
""")

# Here we decipher the keyboard key to a format we can use internall
    # this just makes it easier for dealing with keyboard input
def handleInput(key):
    global pressedKey
    if key == keyboard.Key.up:
        pressedKey = Controls.UP
    elif key == keyboard.Key.down:
        pressedKey = Controls.DOWN
    elif key == keyboard.Key.enter:
        pressedKey = Controls.ENTER
    elif key == keyboard.Key.ctrl_l:
        pressedKey = Controls.Exit
    elif hasattr(key, "char"):
        if key.char == 'b':
            pressedKey = Controls.BACK
    else:
        return Controls.Nothing
        
# Here we listen for 1 key press and report it back
# We do this by having a Nothing key by default and using the input handler
# to decode any other key presses and break the loop, we also stop listening
# when we dont need too
def getNextKey():
    global pressedKey, listener
    pressedKey = Controls.Nothing
    # Start Listening
    listener = keyboard.Listener(
            on_press=handleInput,
            suppress=True)
    listener.start()
    # Loop for aslong as nothing is pressed
    while pressedKey == Controls.Nothing:
        pass
    # When something is pressed we stop listening and return
    listener.stop()
    return pressedKey

# The start of the program, prints out main menu and waits for the users input
def mainMenu():
    global menuOptions, selectedOption
    printMainMenu()
    value = getNextKey()
    if(value == Controls.DOWN):
        # Make sure we stay within the valid options
        if selectedOption < len(menuOptions) - 1:
            selectedOption += 1
            mainMenu()
        else:
            mainMenu()
    elif(value == Controls.UP):
        # Make sure we stay within the valid options
        if selectedOption > 0:
            selectedOption -= 1
            mainMenu()
        else:
            mainMenu()
    elif(value == Controls.ENTER):
        # Temporary
        if(selectedOption == 0):
            selectedOption = 0
            viewToDo()
        elif(selectedOption == 3):
            clear()
            print("Have a good day o/")
            exit()
        else:
            print("Selected {0}".format(menuOptions[selectedOption]))
    elif(value == Controls.Exit):
        # Nice and cleanly exit the program
        clear()
        print("Have a good day o/")
        exit()
    else:
        mainMenu()

def printToDo():
    global todoItems, selectedOption
    clear()
    f = Figlet(font='cybermedium')
    print (f.renderText('To-Do'))

    print("  Text                          Completed    Status")
    print("-----------------------------------------------------")
    for i in range(len(todoItems)):
        value = todoItems[i]["value"]
        completed = "✗"
        if todoItems[i]["completed"]:
            completed = "✓"
        if len(value) > 30:
            value = value[0:27] + "..."
        elif len(value) < 30:
            while len(value) < 30:
                value = value + " "
        if(i == selectedOption):
            print("> " + value + Style.RESET_ALL + "   [{0}]         [{1}■".format(completed, resolveColour(todoItems[i]["colour"])) + Style.RESET_ALL +  "]")
        else:
            print("  " + value + Style.RESET_ALL + "   [{0}]         [{1}■".format(completed, resolveColour(todoItems[i]["colour"])) + Style.RESET_ALL + "]")
    print("""\n
[B] Back      [Enter] Edit
[↑] Move Up   [↓] Move Down
[N] New       [C] Change Status
""")
    print(todoItems)

def resolveColour(colour):
    if colour == "red":
        return Fore.RED
    elif colour == "green":
        return Fore.GREEN

def viewToDo():
    global todoItems, selectedOption
    printToDo()
    value = getNextKey()
    if(value == Controls.DOWN):
        # Make sure we stay within the valid options
        if selectedOption < len(todoItems) - 1:
            selectedOption += 1
            viewToDo()
        else:
            viewToDo()
    elif(value == Controls.UP):
        # Make sure we stay within the valid options
        if selectedOption > 0:
            selectedOption -= 1
            viewToDo()
        else:
            viewToDo()
    elif(value == Controls.ENTER):
        # Temporary
        print("Selected {0}".format(todoItems[selectedOption]["value"]))
    elif(value == Controls.BACK):
        # Go back to the main menu
        selectedOption = 0
        mainMenu()

def loadItemsFromDB():
    global todoItems
    dbname = connectToDB()
    collection = dbname["items"]
    dbItems = collection.find()
    for item in dbItems:
        todoItems.append(item)
    print(todoItems)

def connectToDB():
    CONNECTION_STRING = "mongodb+srv://todo:O0B9bDRod8A87nJl@uni-db.ptlajcy.mongodb.net/test"
    client = MongoClient(CONNECTION_STRING)
    return client['todo']

loadItemsFromDB()
mainMenu()