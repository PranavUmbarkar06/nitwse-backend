from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

from LoginHandle import accountdetails, set_collection
from StockHandle import stockhandle, set_db as set_stock_db
from TransactionHandle import transactionhandle, set_db as set_txn_db

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "https://nitwse-backend.onrender.com"], supports_credentials=True)

client = MongoClient("your-mongo-url")
db = client.get_database("nitwse")

# Inject Mongo collections/databases
set_collection(db["users"])
set_stock_db(client)
set_txn_db(client)

# Register blueprints
app.register_blueprint(accountdetails, url_prefix="/auth")
app.register_blueprint(stockhandle, url_prefix="/stocks")
app.register_blueprint(transactionhandle, url_prefix="/txn")

if __name__ == '__main__':
    app.run(debug=True)
