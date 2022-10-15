from colorama import Fore, Back, Style
import sys
from pymongo import MongoClient

from pages.main import MainPage
from pages.todo import TodoPage
from pages.credits import CreditsPage
from pages.todoItem import TodoItemPage

from utils import Utils

class Main:

    def __init__(self, mongoString, debug):
        self.DEBUG = debug
        self.MONGO_STRING = mongoString
        self.UTILS = Utils(self)
        self.MAIN = MainPage(self, self.UTILS)
        self.TODO = TodoPage(self, self.UTILS, self.loadItemsFromDB())
        self.CREDITS = CreditsPage(self, self.UTILS)
    
    def loadItemsFromDB(self):
        todoItems = []
        dbname = self.connectToDB()
        collection = dbname["items"]
        dbItems = collection.find()
        for item in dbItems:
            todoItems.append(item)
        return todoItems

    def saveItemToDB(self, item):
        dbname = self.connectToDB()
        collection = dbname["items"]
        query = {"_id": item["_id"]}
        values = {"$set" : item}
        collection.update_one(query, values, upsert=True)

    def removeItemFromDB(self, item):
        dbname = self.connectToDB()
        collection = dbname["items"]
        collection.delete_one({"_id": item["_id"]})

    def connectToDB(self):
        client = MongoClient(self.MONGO_STRING)
        return client['todo']

    def switchToMain(self, selectedOption):
        self.MAIN.show(selectedOption)

    def switchToToDo(self, selectedOption):
        self.TODO.show(selectedOption)

    def switchToCreditsPage(self):
        self.CREDITS.show()

    def switchToTodoItem(self, item, selectedOption):
        self.TODO_ITEM = TodoItemPage(self, self.UTILS, item)
        self.TODO_ITEM.show(selectedOption)

    def debugPrint(self, value):
        if self.DEBUG:
            print(value)


debug = False
for i in range(1, len(sys.argv)):
    if sys.argv[i] == "--debug":
        debug = True

main = Main("mongodb+srv://todo:O0B9bDRod8A87nJl@uni-db.ptlajcy.mongodb.net/test", debug)
main.switchToMain(0)