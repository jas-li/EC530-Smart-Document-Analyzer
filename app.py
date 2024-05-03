from flask import Flask, request, jsonify
from config import Config
from auth import auth, register
from secure_upload import upload_file, get_files
from feed_ingest import convert_file
from nlp_analysis import extract_keywords, summarize_text
from flask_cors import CORS

# Queuing
from queue import Queue
from threading import Thread, Event

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Queue for NLP analysis tasks
nlp_queue = Queue()

# Function to process NLP analysis tasks
def process_tasks(app):
    with app.app_context():
        while True:
            task = nlp_queue.get()
            task_type = task['type']
            
            if task_type == 'text_keyword':
                result = extract_keywords(task['text'], num_keywords=10)
                status_code = 200
            elif task_type == 'text_summary':
                result = summarize_text(task['text'], num_sentences=3)
                status_code = 200
            elif task_type == 'doc_conversion':
                user_id = task['user_id']
                result, status_code = convert_file(task['filename'], user_id)
            else:
                result, status_code = None, 500
            
            # Store the result in a container
            task['result']['result'] = (result, status_code)
            
            # Signal that the task is done
            task['event'].set()
            
            nlp_queue.task_done()

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
    user = auth.current_user()  # Get the authenticated user
    if not user:
        return jsonify({"error": "Authentication required"}), 401

    files, status_code = get_files(user['_id'])
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

    user = auth.current_user()  # Get the authenticated user
    if not user:
        return jsonify({"error": "Authentication required"}), 401

    # Create an event and a container for the result
    event = Event()
    result_container = {}

    # Prepare the task with user info
    task = {
        'type': 'doc_conversion',
        'filename': filename,
        'user_id': user['_id'],  # Pass the user ID instead of the whole user object
        'event': event,
        'result': result_container
    }

    # Enqueue the task
    nlp_queue.put(task)

    # Wait for the event to be set by the processing thread
    event.wait()

    # Retrieve the result from the container
    text, status_code = result_container['result']

    if status_code == 200:
        return jsonify({"text": text}), 200
    elif status_code == 404:
        return jsonify({"error": "File not found"}), 404
    else:
        return jsonify({"error": text}), status_code

@app.route('/text_keyword', methods=['POST'])
@auth.login_required
def text_keyword():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is missing or invalid"}), 400
    
    # Create an event and a container for the result
    event = Event()
    result_container = {}
    
    # Prepare the task with the text, event, and container
    task = {
        'type': 'text_keyword',
        'text': data['text'],
        'event': event,
        'result': result_container
    }
    
    # Enqueue the task
    nlp_queue.put(task)
    
    # Wait for the event to be set by the processing thread
    event.wait()
    
    # Retrieve the result from the container
    result, status_code = result_container['result']
    
    # Return the result
    return jsonify({"keywords": result}), 200

@app.route('/text_summary', methods=['POST'])
@auth.login_required
def text_summary():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is missing or invalid"}), 400
    
    # Create an event and a container for the result
    event = Event()
    result_container = {}
    
    # Prepare the task with the text, event, and container
    task = {
        'type': 'text_summary',
        'text': data['text'],
        'event': event,
        'result': result_container
    }
    
    # Enqueue the task
    nlp_queue.put(task)
    
    # Wait for the event to be set by the processing thread
    event.wait()
    
    # Retrieve the result from the container
    result, status_code = result_container['result']
    
    # Return the result
    return jsonify({"summary": result}), 200

if __name__ == '__main__':
    task_thread = Thread(target=process_tasks, args=(app,))
    task_thread.daemon = True
    task_thread.start()
    app.run(debug=True)