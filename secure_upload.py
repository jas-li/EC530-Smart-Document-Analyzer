from werkzeug.utils import secure_filename
from flask import current_app, jsonify, request
import os
import pdfplumber
from PIL import Image
import pytesseract
import gridfs
from pymongo import MongoClient
import certifi
from config import Config

client = MongoClient(Config.MONGODB_KEY, tlsCAFile=certifi.where())
db = client["app_data"]
fs =gridfs.GridFS(db)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def pdf_to_text(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def image_to_text(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

def process_file(file):
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    filename = secure_filename(file.filename)
    content_type = file.content_type

    # file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    # file.save(file_path)
    file_id = fs.put(file, filename=filename, content_type=content_type)

    grid_out = fs.get(file_id)
    if filename.lower().endswith('pdf'):
        text = pdf_to_text(grid_out)
    else:
        text = image_to_text(grid_out)

    return jsonify({"message": "File processed successfully", "text": text}), 200

def upload_file():
    if 'file' not in request.files:
        return {"error": "No file part"}, 400
    file = request.files['file']
    if file.filename == '':
        return {"error": "No selected file"}, 400
    try:
        response = process_file(file)
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

