from werkzeug.utils import secure_filename
from flask import current_app, jsonify, request
import gridfs
from pymongo import MongoClient
import certifi
from config import Config
from auth import auth

client = MongoClient(Config.MONGODB_KEY, tlsCAFile=certifi.where())
db = client["app_data"]
fs = gridfs.GridFS(db)
users_collection = db["users"]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def process_file(file):
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    filename = secure_filename(file.filename)
    content_type = file.content_type

    file_id = fs.put(file, filename=filename, content_type=content_type)
    # grid_out = fs.get(file_id)
    # if filename.lower().endswith('pdf'):
    #     text = pdf_to_text(grid_out)
    # else:
    #     text = image_to_text(grid_out)

    # return jsonify({"message": "File processed successfully", "text": text}), 200
    return file_id

def upload_file():
    if 'file' not in request.files:
        return {"error": "No file part"}, 400
    file = request.files['file']
    if file.filename == '':
        return {"error": "No selected file"}, 400
    try:
        user = auth.current_user()  # Get the authenticated user
        if user:
            file_id = process_file(file)  # Process the file and get its ID
            # Update the user document with the file ID
            users_collection.update_one({"_id": user["_id"]}, {"$push": {"files": file_id}})
            return jsonify({"message": "File uploaded successfully"}), 200
        else:
            return jsonify({"error": "Authentication failed"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_files():
    user = auth.current_user()  # Get the authenticated user
    if user:
        user_doc = users_collection.find_one({"_id": user["_id"]})
        if user_doc:
            user_files = user_doc.get("files", [])  # Get the list of files associated with the user
            file_names = [fs.get(file).filename for file in user_files]
            return jsonify({"files": file_names}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({"error": "Authentication failed"}), 401

