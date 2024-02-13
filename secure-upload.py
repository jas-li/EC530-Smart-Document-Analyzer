def login(username, password):
    return 0

def load(file):
    if(open(file) == 1):
        return 0
    else:
        return -1

def convert_to_str(file):
    fd = load(file)
    if(fd):
        new_str = fd.parse()
        return new_str
    else:
        return -1

def upload_doc(document):
    if(load(document)):
        return 0
    else:
        return -1

def upload_pdf(document):
    if(load(document)):
        convert_to_str(document)
        return 0
    else:
        return -1

def upload_image(img):
    return 0 # Convert to img to text

def tag_document(documents):
    return 0 # Get the leywords and topics in a document

def analyze_sentiment(text):
    return 0 # Analyze a string and return a sentiment

def get_keyword_definitions(keywords):
    return 0 # Get definitions of keywords

def summarize_document(doc_text):
    return 0 # Return the summary of a document
