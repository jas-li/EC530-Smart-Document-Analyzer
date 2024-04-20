import pdfplumber
import pytesseract
from PIL import Image
import os

import gridfs
from pymongo import MongoClient
import certifi
from config import Config
from auth import auth

from secure_upload import get_files

from bson import ObjectId

client = MongoClient(Config.MONGODB_KEY, tlsCAFile=certifi.where())
db = client["app_data"]
fs = gridfs.GridFS(db)
users_collection = db["users"]

def pdf_to_text(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def image_to_text(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

def convert_file(filename):
    files, status_code = get_files()
    if status_code != 200:
        return "Error: Unable to retrieve files", 500
    
    if filename not in files:
        return "Error: File not found", 404

    grid_out = fs.get(ObjectId(files[filename]))

    if not grid_out:
        return "Error: File not found in GridFS", 404

    if filename.lower().endswith('.pdf'):
        try:
            text = pdf_to_text(grid_out)
            return text, 200
        except Exception as e:
            return f"Error: Failed to extract text from PDF - {str(e)}", 500
    else:
        try:
            text = image_to_text(grid_out)
            return text, 200
        except Exception as e:
            return f"Error: Failed to extract text from image - {str(e)}", 500