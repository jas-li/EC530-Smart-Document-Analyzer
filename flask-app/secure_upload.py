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

def get_files(user_id):
    user_doc = users_collection.find_one({"_id": user_id})
    file_dict = {}
    if user_doc:
        user_files = user_doc.get("files", [])  # Get the list of files associated with the user
        for file_id in user_files:
            file_obj = fs.get(file_id)
            if file_obj:
                file_dict[file_obj.filename] = str(file_id)
        return file_dict, 200
    else:
        return {}, 404

def remove_file(user_id, filename):
    user_doc = users_collection.find_one({"_id": user_id})
    if not user_doc:
        return jsonify({"error": "User not found"}), 404

    # Extract files array from the user document.
    user_files = user_doc.get("files", [])
    
    # Locate the file in GridFS by its filename and the user's file IDs.
    file_obj = fs.find_one({"filename": filename, "_id": {"$in": user_files}})
    if not file_obj:
        return jsonify({"error": "File not found"}), 404

    # Attempt to delete the file from GridFS.
    try:
        fs.delete(file_obj._id)
        # Update the user document to remove the file reference.
        users_collection.update_one(
            {"_id": user_id},
            {"$pull": {"files": file_obj._id}}
        )
        return jsonify({"success": "File deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
