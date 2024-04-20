from pymongo import MongoClient
import certifi

import pdfplumber
import pytesseract
from PIL import Image

import gridfs

from bson import ObjectId  # Import ObjectId if needed


# # Replace <connection_string> with your actual connection string
# client = MongoClient("mongodb+srv://jli3469:uJ8EujYz0RboojHm@developmentcluster.7hbkaa1.mongodb.net/?retryWrites=true&w=majority&appName=DevelopmentCluster", tlsCAFile=certifi.where())

# # Access a specific database
# db = client.get_database("app_data")

# # Access a specific collection
# collection = db.users

# user_data = {
#     "username": "john_doe",
#     "email": "john.doe@example.com",
#     "password": "hashed_password",  # You should hash passwords before storing them
#     # Add other user information as needed
# }

# # Insert user information into the collection
# insert_result = collection.insert_one(user_data)

# # Print the inserted document's ID
# print("Inserted document ID:", insert_result.inserted_id)

# # Close the MongoDB connection
# client.close()

client = MongoClient("mongodb+srv://jli3469:uJ8EujYz0RboojHm@developmentcluster.7hbkaa1.mongodb.net/?retryWrites=true&w=majority&appName=DevelopmentCluster", tlsCAFile=certifi.where())
db = client["app_data"]
fs = gridfs.GridFS(db)
users_collection = db["users"]

# users = {}
# for user_doc in users_collection.find():
#     username = user_doc["username"]
#     password = user_doc["password"]
#     users[username] = password

# print(users)

def pdf_to_text(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def image_to_text(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

grid_out = fs.get(ObjectId('66212b16dafe483a8b74eef6'))

text = pdf_to_text(grid_out)

print(text)
