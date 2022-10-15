from pynput import keyboard
import os
from colorama import Fore, Back, Style
from enum import Enum

class Utils:

    def __init__(self, main):
        self.main = main
        self.colourOptions = ["red", "yellow", "green"]
        self.pressedKey = self.Controls.Nothing

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

    # Here we listen for 1 key press and report it back
    # We do this by having a Nothing key by default and using the input handler
    # to decode any other key presses and break the loop, we also stop listening
    # when we dont need too
    def getNextKey(self):
        global pressedKey, listener
        pressedKey = self.Controls.Nothing
        # Start Listening
        listener = keyboard.Listener(
                on_press=self.handleInput,
                suppress=True)
        listener.start()
        # Loop for aslong as nothing is pressed
        while pressedKey == self.Controls.Nothing:
            pass
        # When something is pressed we stop listening and return
        listener.stop()
        return pressedKey

    # Here we decipher the keyboard key to a format we can use internal
    # this just makes it easier for dealing with keyboard input
    def handleInput(self, key):
        global pressedKey
        if key == keyboard.Key.up:
            pressedKey = self.Controls.UP
        elif key == keyboard.Key.down:
            pressedKey = self.Controls.DOWN
        elif key == keyboard.Key.enter:
            pressedKey = self.Controls.ENTER
        elif key == keyboard.Key.ctrl_l:
            pressedKey = self.Controls.Exit
        elif hasattr(key, "char"):
            if key.char == 'b':
                pressedKey = self.Controls.BACK
            elif key.char == 'c':
                pressedKey = self.Controls.CYCLE
            elif key.char == 't':
                pressedKey = self.Controls.TOGGLE
            elif key.char == 'n':
                pressedKey = self.Controls.NEW
            elif key.char == 'd':
                pressedKey = self.Controls.DELETE
            elif key.char == 'y':
                pressedKey = self.Controls.YES
            elif key.char == 'n':
                pressedKey = self.Controls.NO
        else:
            pressedKey = self.Controls.Nothing

    # Reusable function for clearing the screen
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')


    def resolveColour(self, colour):
        if colour == "red":
            return Fore.RED
        elif colour == "yellow":
            return Fore.YELLOW
        elif colour == "green":
            return Fore.GREEN

    def findNextColour(self, colour):
        index = self.colourOptions.index(colour)
        if(index == len(self.colourOptions) - 1):
            index = 0
        else:
            index += 1
        return self.colourOptions[index]