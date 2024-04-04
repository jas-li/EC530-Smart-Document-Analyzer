from werkzeug.utils import secure_filename
from flask import current_app, jsonify
import os
import pdfplumber
from PIL import Image
import pytesseract

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
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    if filename.rsplit('.', 1)[1].lower() in {'pdf'}:
        text = pdf_to_text(file_path)
    else:
        text = image_to_text(file_path)

    return jsonify({"message": "File processed successfully", "text": text}), 200
