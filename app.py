from flask import Flask, request
from config import Config
from auth import auth
from secure_upload import process_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

@app.route('/upload', methods=['POST'])
@auth.login_required
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

if __name__ == '__main__':
    app.run(debug=True)
