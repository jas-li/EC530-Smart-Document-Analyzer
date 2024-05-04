from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from pymongo import MongoClient
import certifi
import bcrypt
from base64 import b64encode
from config import Config
from hmac import compare_digest

auth = HTTPBasicAuth()

# MongoDB connection
client = MongoClient(Config.MONGODB_KEY, tlsCAFile=certifi.where())
db = client["app_data"]
users_collection = db["users"]

@auth.verify_password
def verify_password(username, password):
    user_doc = users_collection.find_one({"username": username})
    if user_doc:
        stored_password = user_doc["password"]
        # Mitigate timing attacks
        if compare_digest(bcrypt.hashpw(password.encode('utf-8'), stored_password.encode('utf-8')), stored_password.encode('utf-8')):
            return user_doc
    return False

def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    if users_collection.find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 400
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # Store the hashed password as a decoded string for storage
    users_collection.insert_one({
        "username": username,
        "password": hashed_password.decode('utf-8'),
        "files": []  # Initialize
    })
    return jsonify({"message": "User registered successfully"}), 201

def login(username, password):
    user_doc = users_collection.find_one({"username": username})
    if user_doc:
        stored_password = user_doc["password"]
        # Mitigate timing attacks
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            # Create Basic Authentication token
            auth_token = b64encode(f"{username}:{password}".encode('utf-8')).decode('utf-8')
            return jsonify({"message": "Logged in successfully", "token": auth_token}), 200
        else:
            return jsonify({"error": "Incorrect password"}), 401
    else:      
        return jsonify({"error": "User does not exist"}), 404