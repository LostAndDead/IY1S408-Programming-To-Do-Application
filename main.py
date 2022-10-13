from colorama import Fore, Back, Style

from pymongo import MongoClient

import pages.main as mainPage
import pages.todo as todoPage
import pages.credits as creditsPage
import pages.todoItem as todoItem

def loadItemsFromDB():
    todoItems = []
    dbname = connectToDB()
    collection = dbname["items"]
    dbItems = collection.find()
    for item in dbItems:
        todoItems.append(item)
    todoPage.setTodoItems(todoItems)

def saveItemToDB(item):
    dbname = connectToDB()
    collection = dbname["items"]
    query = {"_id": item["_id"]}
    values = {"$set" : item}
    collection.update_one(query, values, upsert=True)

def removeItemFromDB(item):
    dbname = connectToDB()
    collection = dbname["items"]
    collection.delete_one({"_id": item["_id"]})

def connectToDB():
    CONNECTION_STRING = "mongodb+srv://todo:O0B9bDRod8A87nJl@uni-db.ptlajcy.mongodb.net/test"
    client = MongoClient(CONNECTION_STRING)
    return client['todo']

def switchToMain(selectedOption):
    mainPage.show(selectedOption)

def switchToToDo(selectedOption):
    todoPage.show(selectedOption)

def switchToCreditsPage():
    creditsPage.show()

def switchToTodoItem(item, selectedOption):
    todoItem.show(item, selectedOption)

loadItemsFromDB()
mainPage.show(0)