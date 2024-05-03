import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def extract_keywords(text, num_keywords=10):
    # Tokenize the text
    words = word_tokenize(text)
    words = [word for word in words if word.isalnum()]

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.lower() not in stop_words]

    # Frequency distribution of words
    freq_dist = FreqDist(filtered_words)
    keywords = sorted(freq_dist, key=freq_dist.get, reverse=True)[:num_keywords]  # top keywords

    return keywords

def summarize_text(text, num_sentences=3):
    # Create a plaintext parser
    parser = PlaintextParser.from_string(text, Tokenizer('english'))
    summarizer = LsaSummarizer()

    # Generate summary
    summary = summarizer(parser.document, num_sentences)  # summarize into num_sentences

    summarized_text = ' '.join(str(sentence) for sentence in summary)

    return summarized_text