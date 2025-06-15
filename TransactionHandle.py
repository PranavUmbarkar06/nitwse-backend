from flask import Blueprint, request, jsonify

transactionhandle = Blueprint('transactionhandle', __name__)
mongo = None  # Will be initialized in app.py

def updateBalance(userID, updatedPrice):
    temp = mongo.db.usertransactions.find_one({"userID": userID})
    if not temp or temp.get("balance", 0) + updatedPrice < 0:
        return False
    mongo.db.usertransactions.update_one(
        {"userID": userID},
        {"$inc": {"balance": updatedPrice}}
    )
    return True

def buyStock(userID, stockPrice, quantity, stockName):
    if updateBalance(userID, -stockPrice * quantity):
        mongo.db.usertransactions.update_one(
            {"userID": userID},
            {"$inc": {f"stocksOwned.{stockName}": quantity}}
        )
        return True
    return False

def sellStock(userID, stockPrice, quantity, stockName):
    temp = mongo.db.usertransactions.find_one({"userID": userID})
    if not temp:
        return False
    owned = temp.get("stocksOwned", {}).get(stockName, 0)
    if owned >= quantity:
        mongo.db.usertransactions.update_one(
            {"userID": userID},
            {"$inc": {f"stocksOwned.{stockName}": -quantity}}
        )
        updateBalance(userID, stockPrice * quantity)
        return True
    return False

@transactionhandle.route('/buy', methods=['POST'])
def buy():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON received"}), 400

    try:
        userID = int(data["userID"])
        stockPrice = float(data["stockPrice"])
        quantity = int(data["quantity"])
        stockName = data["stockName"]
    except (KeyError, ValueError):
        return jsonify({"status": "error", "message": "Invalid or missing data"}), 400

    if quantity <= 0 or stockPrice <= 0:
        return jsonify({"status": "error", "message": "Quantity and stockPrice must be positive"}), 400

    if buyStock(userID, stockPrice, quantity, stockName):
        return jsonify({"status": "success", "message": "Transaction Successful"})
    return jsonify({"status": "failed", "message": "Invalid Transaction or Insufficient balance"})

@transactionhandle.route('/sell', methods=['POST'])
def sell():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON received"}), 400

    try:
        userID = int(data["userID"])
        stockPrice = float(data["stockPrice"])
        quantity = int(data["quantity"])
        stockName = data["stockName"]
    except (KeyError, ValueError):
        return jsonify({"status": "error", "message": "Invalid or missing data"}), 400

    if quantity <= 0 or stockPrice <= 0:
        return jsonify({"status": "error", "message": "Quantity and stockPrice must be positive"}), 400

    if sellStock(userID, stockPrice, quantity, stockName):
        return jsonify({"status": "success", "message": "Transaction Successful"})
    return jsonify({"status": "failed", "message": "Invalid Transaction"})

@transactionhandle.route('/import', methods=['GET'])
def display():
    try:
        userID = int(request.args.get("userID"))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid or missing userID"}), 400

    user = mongo.db.usertransactions.find_one({"userID": userID})
    if user:
        return jsonify({
            "balance": user.get("balance", 0),
            "stocks": user.get("stocksOwned", {})
        })
    return jsonify({"error": "User not found", "stocks": {}}), 404

