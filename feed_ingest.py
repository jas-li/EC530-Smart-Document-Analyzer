# Coverting pdf to strings
import PyPDF2
import pytesseract
from PIL import Image

# MongoDB
import gridfs
from pymongo import MongoClient
import certifi
from config import Config
from bson import ObjectId

# Flask
from auth import auth
from secure_upload import get_files

client = MongoClient(Config.MONGODB_KEY, tlsCAFile=certifi.where())
db = client["app_data"]
fs = gridfs.GridFS(db)
users_collection = db["users"]

def pdf_to_text(pdf_path):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    extracted_text = ""
    for page_num in range(len(pdf_reader.pages)):
        # Extract text from the current page
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        
        # Add the extracted text to the overall text
        extracted_text += text.strip()  # Remove leading and trailing whitespace
    
    # Split the text into paragraphs based on newline characters
    paragraphs = extracted_text.split('\n')
    
    # Join the paragraphs into a single string with paragraph breaks
    text_with_paragraphs = ' '.join(paragraphs)
    
    return text_with_paragraphs

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