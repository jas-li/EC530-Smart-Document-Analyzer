from flask import Flask, request, jsonify
from config import Config
from auth import auth, register
from secure_upload import upload_file, get_files
from feed_ingest import convert_file
from nlp_analysis import extract_keywords
from flask_cors import CORS

# Queuing
from queue import Queue
from threading import Thread

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Queue for NLP analysis tasks
nlp_queue = Queue()

# Function to process NLP analysis tasks
def process_nlp_tasks():
    while True:
        task = nlp_queue.get()
        # Perform NLP analysis here
        result = extract_keywords(task)
        # Handle the result 
        print(result)
        nlp_queue.task_done()

# Start a thread to process NLP analysis tasks
nlp_thread = Thread(target=process_nlp_tasks)
nlp_thread.daemon = True
nlp_thread.start()

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

@app.route('/analyze_nlp', methods=['POST'])
@auth.login_required
def analyze_nlp():
    # Extract document or paragraph data from request
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is missing or invalid"}), 400

    # Enqueue NLP analysis task
    nlp_queue.put(data["text"])

    return jsonify({"message": "NLP analysis task enqueued successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)


