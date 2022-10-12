from pynput import keyboard
import os
from colorama import Fore, Back, Style
from enum import Enum

class Controls(Enum):
    Exit = -1
    Nothing = 0
    UP = 1
    DOWN = 2
    ENTER = 3
    BACK = 4
    CYCLE = 5
    TOGGLE = 6
    NEW = 7
    DELETE = 8
    YES = 9
    NO = 10

global pressedKey
pressedKey = Controls.Nothing

colourOptions = ["red", "yellow", "green"]

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

# Here we decipher the keyboard key to a format we can use internal
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
        elif key.char == 'c':
            pressedKey = Controls.CYCLE
        elif key.char == 't':
            pressedKey = Controls.TOGGLE
        elif key.char == 'n':
            pressedKey = Controls.NEW
        elif key.char == 'd':
            pressedKey = Controls.DELETE
        elif key.char == 'y':
            pressedKey = Controls.YES
        elif key.char == 'n':
            pressedKey = Controls.NO
    else:
        pressedKey = Controls.Nothing

# Reusable function for clearing the screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def resolveColour(colour):
    if colour == "red":
        return Fore.RED
    elif colour == "yellow":
        return Fore.YELLOW
    elif colour == "green":
        return Fore.GREEN

def findNextColour(colour):
    index = colourOptions.index(colour)
    if(index == len(colourOptions) - 1):
        index = 0
    else:
        index += 1
    return colourOptions[index]