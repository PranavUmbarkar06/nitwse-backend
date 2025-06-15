from flask import Blueprint, request, jsonify

stockhandle = Blueprint('stockhandle', __name__)
db = None  # Will be initialized in main app

@stockhandle.route('/get_stocks', methods=['GET'])
def get_stocks():
    stocks = list(db.stockdata.find({}, {"_id": 0}))
    result = {stock['Name']: {"Name": stock['Name'], "Price": stock['Price']} for stock in stocks}
    return jsonify(result)

@stockhandle.route('/get_remaining_stocks', methods=['GET'])
def get_remaining_stocks():
    user_id = request.args.get('userID')
    if not user_id:
        return jsonify({"error": "userID is required"}), 400

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"error": "userID must be an integer"}), 400

    user_data = db.userdata.find_one({"userID": user_id}, {"_id": 0, "stocksOwned": 1})
    user_stocks = set(user_data.get("stocksOwned", {}).keys()) if user_data else set()

    all_stocks = list(db.stockdata.find({}, {"_id": 0}))
    remaining_stocks = [stock for stock in all_stocks if stock['Name'] not in user_stocks]

    return jsonify({"remaining_stocks": remaining_stocks})


