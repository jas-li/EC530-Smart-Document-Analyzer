import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../flask-app')))
import pytest
from nlp_analysis import extract_keywords, summarize_text, analyze_sentiment

# Test for extract_keywords to check the right number of keywords
@pytest.mark.parametrize("text, num_keywords", [
    ("Python is great. Python can be used for scripting, Python can be fun!", 5),
    ("Data science involves Python. Python includes machine learning, data processing, and data visualization.", 10)
])
def test_extract_keywords(text, num_keywords):
    result = extract_keywords(text, num_keywords)
    assert len(result) == num_keywords, f"Expected {num_keywords} keywords, got {len(result)}"

# Test for summarize_text to check the right number of sentences
@pytest.mark.parametrize("text, num_sentences", [
    ("Python is a programming language. It's used widely for web development, data analysis, artificial intelligence, and scientific computing. Python supports multiple programming paradigms.", 3),
    ("Python is easy to learn. It supports different programming paradigms. It is used in many scientific applications. It is popular in data science. Python has a large community.", 5)
])
def test_summarize_text(text, num_sentences):
    result = summarize_text(text, num_sentences)
    result_sentences = result.split('. ')
    assert len(result_sentences) == num_sentences, f"Expected {num_sentences} sentences, got {len(result_sentences)}"

# Test for analyze_sentiment
@pytest.mark.parametrize("text, expected_sentiment", [
    ("I love Python programming!", "positive"),
    ("This is pizza.", "neutral"),
    ("I hate bad weather.", "negative")
])
def test_analyze_sentiment(text, expected_sentiment):
    sentiment = analyze_sentiment(text)
    assert sentiment == expected_sentiment

