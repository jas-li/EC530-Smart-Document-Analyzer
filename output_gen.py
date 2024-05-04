import requests
from config import Config

def search_wikipedia(keyword):
    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': keyword,
        'format': 'json',
        'prop': 'info',
        'inprop': 'url'
    }
    response = requests.get(base_url, params=params)
    search_results = response.json().get('query', {}).get('search', [])
    
    urls = []
    for result in search_results:
        page_id = result['pageid']
        url = f"https://en.wikipedia.org/?curid={page_id}"
        urls.append(url)
    
    return urls

def search_nytimes(keyword):
    base_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    params = {
        'q': keyword,
        'api-key': Config.NYTIMES_KEY
    }
    response = requests.get(base_url, params=params)
    articles = response.json().get('response', {}).get('docs', [])
    
    urls = [article['web_url'] for article in articles if 'web_url' in article]
    
    return urls

def get_word_definitions(word):
    url = f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={Config.MERRIAM_KEY}"
    response = requests.get(url)
    definitions = response.json()
    
    if definitions and isinstance(definitions[0], dict):
        entry = definitions[0]
        # Extract the word, pronunciation, and part of speech
        word = entry.get('meta', {}).get('id', '').split(':')[0]  # Get the word itself, strip any extraneous codes
        fl = entry.get('fl', '')  # Part of speech
        prs = entry.get('hwi', {}).get('prs', [{}])[0].get('mw', '')  # Phonetic pronunciation

        # Extract definitions, ensuring to capture all available definitions
        first_definition = entry.get('shortdef', []) if 'shortdef' in entry else None
        
        # Return structured dictionary
        return {
            'word': word,
            'pronunciation': prs,
            'part_of_speech': fl,
            'definitions': first_definition
        }
    
    # Return None if no valid dictionary entry was found
    return None