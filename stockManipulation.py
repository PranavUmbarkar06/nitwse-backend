from pymongo import MongoClient

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://nitwse:mayankthegoat@wse.0zosyhw.mongodb.net/nitwse?retryWrites=true&w=majority&appName=WSE")
db = client["nitwse"]

collection = db["stockdata"]

stockName = input("Enter Stock you want to update: ")

stock = collection.find_one({"Name": stockName})
oldprice = stock["Price"]

inactivedays = int(input("Inactive Days? : "))
numberofparticipants = int(input("If event conducted today, enter number of participants: "))

new_price = oldprice - inactivedays * 0.1 + numberofparticipants * 0.08  # Change this as needed

collection.update_one(
    {"Name": stockName},
    {"$set": {"Price": new_price}}
)

print(f"{stockName} price updated to ₹{new_price}")
