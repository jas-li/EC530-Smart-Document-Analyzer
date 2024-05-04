from flask import Flask, request, jsonify
from config import Config
from auth import auth, register, login
from secure_upload import upload_file, get_files, remove_file
from feed_ingest import convert_file, extract_web_content
from nlp_analysis import extract_keywords, summarize_text, analyze_sentiment
from output_gen import search_nytimes, search_wikipedia, get_word_definitions
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

@app.route('/login', methods=['POST'])
def login_route():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username or password missing"}), 400
    
    return login(username, password)

@app.route('/upload', methods=['POST'])
@auth.login_required
def upload_route():
    return upload_file()

@app.route('/delete_file', methods=['POST'])
@auth.login_required
def delete_file():
    user = auth.current_user()
    file = request.args.get('filename')
    if not file:
        return jsonify({"error": "Missing file"}), 400

    return remove_file(user['_id'], file)

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

@app.route('/extract_from_url', methods=['POST'])
def extract_from_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400

    try:
        content = extract_web_content(data['url'])
        return jsonify(content), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/text_keyword', methods=['POST'])
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

@app.route('/text_sentiment', methods=['POST'])
def text_sentiment():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    sentiment = analyze_sentiment(data['text'])
    return jsonify({'sentiment': sentiment}), 200

@app.route('/content_links', methods=['GET'])
def content_links():
    data = request.args.get('keyword')
    if not data:
        return jsonify({'error': 'No keyword provided'}), 400

    keywords = extract_keywords(data)

    # Gather links
    wikipedia_links = search_wikipedia(keywords[0])  # Simplified to use the first keyword
    nytimes_links = search_nytimes(keywords[0])

    return jsonify({
        'wikipedia_links': wikipedia_links,
        'nytimes_links': nytimes_links
    }), 200

@app.route('/keyword_def', methods=['GET'])
def definition_route():
    word = request.args.get('word')
    if not word:
        return jsonify({'error': 'No word provided'}), 400

    definition = get_word_definitions(word)
    if definition:
        return jsonify(definition), 200
    else:
        return jsonify({'error': 'Definition not found'}), 404

if __name__ == '__main__':
    task_thread = Thread(target=process_tasks, args=(app,))
    task_thread.daemon = True
    task_thread.start()
    app.run(debug=True)