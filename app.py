from flask import Flask, request, jsonify
from config import Config
from auth import auth, register
from secure_upload import upload_file, get_files
from feed_ingest import convert_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

@app.route('/register', methods=['POST'])
def register_route():
    return register()

@app.route('/upload', methods=['POST'])
@auth.login_required
def upload_route():
    return upload_file()

@app.route('/get_files', methods=['GET'])
@auth.login_required
def user_files_route():
    files, status_code = get_files()
    if status_code == 200:
        return jsonify({"files": files}), 200
    elif status_code == 404:
        return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({"error": "Authentication failed"}), 401

@app.route('/doc_to_text', methods=['GET'])
@auth.login_required
def doc_to_text():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({"error": "Filename parameter is missing"}), 400

    text, status_code = convert_file(filename)
    if status_code == 200:
        return jsonify({"text": text}), 200
    elif status_code == 404:
        return jsonify({"error": "File not found"}), 404
    else:
        return jsonify({"error": text}), status_code

if __name__ == '__main__':
    app.run(debug=True)


