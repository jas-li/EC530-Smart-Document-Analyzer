import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from text import text

def preprocess_text(text):
    # Tokenize the text
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text.lower())

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    # Stemming
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]

    return stemmed_tokens

def extract_keywords(text, num_keywords=10):
    tokens = preprocess_text(text)
    
    # Calculate term frequency
    term_freq = FreqDist(tokens)
    
    # Calculate inverse document frequency
    documents = [tokens]
    idf = nltk.text.FreqDist()
    for term in term_freq.keys():
        num_docs_containing_term = sum(1 for document in documents if term in document)
        idf[term] = num_docs_containing_term

    # Calculate TF-IDF
    tfidf = {term: term_freq[term] * (1 / idf[term]) for term in term_freq.keys()}

    # Sort keywords by TF-IDF score
    sorted_keywords = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)

    return [keyword[0] for keyword in sorted_keywords[:num_keywords]]

keywords = extract_keywords(text)
print("Top 10 Keywords:", keywords)
