import pdfplumber
import pytesseract
from PIL import Image
import os

def pdf_to_text(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def image_to_text(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

def convert_file(file_path):
    # Get the file extension
    _, file_extension = os.path.splitext(file_path)
    
    # Check if it's a PDF or image
    if file_extension.lower() == '.pdf':
        text = pdf_to_text(file_path)
    else:
        text = image_to_text(file_path)

    return text