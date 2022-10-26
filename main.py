from colorama import Fore, Back, Style
import sys
from pymongo import MongoClient

from pages.main import MainPage
from pages.todo import TodoPage
from pages.credits import CreditsPage
from pages.todoItem import TodoItemPage

from utils import Utils

class Main:

    # Initilize the main class, take the mongo connection string
    # and wether or not the code is in debug mode, debug mode just pritns
    # a lot more extra data at the bottom of the console
    def __init__(self, mongoString, debug):
        # Set our values for future use in the self
        self.DEBUG = debug
        self.MONGO_STRING = mongoString

        # Load all our subpages with the data they need
        self.UTILS = Utils(self)
        self.MAIN = MainPage(self, self.UTILS)
        self.TODO = TodoPage(self, self.UTILS, self.loadItemsFromDB())
        self.CREDITS = CreditsPage(self, self.UTILS)
    
    # Loads the items from the mongoDB "items" collection
    def loadItemsFromDB(self):
        todoItems = []
        dbname = self.connectToDB()
        collection = dbname["items"]
        dbItems = collection.find()
        for item in dbItems:
            todoItems.append(item)
        return todoItems

    # Saves 1 single "item" to the database by its ID, automatically updating existing objects
    def saveItemToDB(self, item):
        dbname = self.connectToDB()
        collection = dbname["items"]
        query = {"_id": item["_id"]}
        values = {"$set" : item}
        collection.update_one(query, values)

    # Same as above, just for new items
    def saveNewItemToDB(self, item):
        dbname = self.connectToDB()
        collection = dbname["items"]
        collection.insert_one(item)

    # Poof, and the item is gone!
    def removeItemFromDB(self, item):
        dbname = self.connectToDB()
        collection = dbname["items"]
        collection.delete_one({"_id": item["_id"]})

    # Simply fetches the mongoDB client
    def connectToDB(self):
        client = MongoClient(self.MONGO_STRING)
        return client['todo']

    # Functions bellow are called from all the sub classes
    # and are use to navigate the program from one place

    def switchToMain(self, selectedOption):
        self.MAIN.show(selectedOption)

    def switchToToDo(self, selectedOption):
        self.TODO.show(selectedOption)

    def switchToCreditsPage(self):
        self.CREDITS.show()

    def switchToTodoItem(self, item, selectedOption):
        self.TODO_ITEM = TodoItemPage(self, self.UTILS, item)
        self.TODO_ITEM.show(selectedOption)

    #Debug method use for extra details
    def debugPrint(self, value):
        if self.DEBUG:
            print(value)


# Detects if the program was ran with "--debug" and if it was
# enables the debug mode
debug = False
for i in range(1, len(sys.argv)):
    if sys.argv[i] == "--debug":
        debug = True

# Loads and connects, "url" will need to be replace by a mongoDB connection string
# If you are marking as part of my assignment then a URL connection string should have been provided which you can use,
# It will be an existing DB with some existing testing data.
main = Main("mongodb+srv://todo:O0B9bDRod8A87nJl@uni-db.ptlajcy.mongodb.net/test", debug)
main.switchToMain(0)