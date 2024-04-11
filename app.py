from flask import Flask, request, jsonify
from config import Config
from auth import auth, register
from secure_upload import process_file, upload_file
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

if __name__ == '__main__':
    app.run(debug=True)
