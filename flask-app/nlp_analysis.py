import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.probability import FreqDist
from nltk.util import ngrams
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def extract_keywords(text, num_keywords=10, n=2):
    # Tokenize the text
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalnum()]

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]

    # Generate n-grams
    n_grams = list(ngrams(filtered_words, n))

    # Concatenate n-grams into phrases
    phrases = [' '.join(gram).lower() for gram in n_grams]
    
    # Combine individual words and phrases
    combined_keywords = filtered_words + phrases

    # Frequency distribution of combined keywords
    freq_dist = FreqDist(combined_keywords)
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

def analyze_sentiment(text):
    sid = SentimentIntensityAnalyzer()

    # Obtain polarity scores for the text
    scores = sid.polarity_scores(text)
    
    compound_score = scores['compound']
    
    # Determine the type of sentiment
    if compound_score >= 0.05:
        return "positive"
    elif compound_score > -0.05 and compound_score < 0.05:
        return "neutral"
    else:
        return "negative"