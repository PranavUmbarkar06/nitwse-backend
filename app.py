from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

from LoginHandle import accountdetails
from StockHandle import stockhandle
from TransactionHandle import transactionhandle



CORS(app, origins=["http://localhost:5173", "https://nitwse-backend.onrender.com"], supports_credentials=True)


client = MongoClient("mongodb+srv://nitwse:mayankthegoat@wse.0zosyhw.mongodb.net/?retryWrites=true&w=majority&appName=WSE")
db = client["nitwse"]

# Inject collections into modules
import LoginHandle as acc
import StockHandle as sh
import TransactionHandle as tr

acc.users = db["users"]
sh.db = db
tr.db = db

# Register all blueprints
app.register_blueprint(accountdetails, url_prefix="/auth")
app.register_blueprint(stockhandle, url_prefix="/stocks")
app.register_blueprint(transactionhandle, url_prefix="/txn")

if __name__ == '__main__':
    app.run(debug=True)
