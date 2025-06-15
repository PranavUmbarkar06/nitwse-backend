from flask import Blueprint, request, jsonify
from pymongo import MongoClient

accountdetails = Blueprint('accountdetails', __name__)
users = None  # Will be set in app.py

def get_next_user_id():
    highest_user = users.find_one(sort=[("userId", -1)])
    if highest_user and "userId" in highest_user:
        return highest_user["userId"] + 1
    return 1001

@accountdetails.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if users.find_one({"email": email}):
        return jsonify({"message": "User already exists", "success": False}), 409

    userId = get_next_user_id()

    users.insert_one({
        "name": name,
        "email": email,
        "password": password,
        "userId": userId
    })

    return jsonify({
        "message": "Signup successful",
        "success": True,
        "userId": userId,
        "name": name
    }), 201

@accountdetails.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = users.find_one({"email": email, "password": password})
    if user:
        return jsonify({
            "message": "Login successful",
            "success": True,
            "userId": user["userId"],
            "name": user["name"]
        }), 200

    return jsonify({"message": "Invalid credentials", "success": False}), 401
