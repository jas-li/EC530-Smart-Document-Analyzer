import React, { useState } from 'react';
import axios from 'axios';
import './NLP.css';
import KeywordDefinition from './KeywordDef';

function NLP({ text }) {
    const [keywords, setKeywords] = useState([]);
    const [summary, setSummary] = useState('');
    const [sentiment, setSentiment] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const [selectedKeyword, setSelectedKeyword] = useState(null); // State to track the selected keyword

    const handleAnalysis = async (type) => {
        setIsLoading(true);
        setError('');

        if (type === 'keywords') setKeywords([]);
        if (type === 'summary') setSummary('');
        if (type === 'sentiment') setSentiment('');

        const tasks = [];
        const urls = {
            keywords: 'http://127.0.0.1:5000/text_keyword',
            summary: 'http://127.0.0.1:5000/text_summary',
            sentiment: 'http://127.0.0.1:5000/text_sentiment'
        };

        if (document.getElementById('get-keywords').checked) {
            tasks.push(axios.post(urls.keywords, { text }));
        }
        if (document.getElementById('get-summary').checked) {
            tasks.push(axios.post(urls.summary, { text }));
        }
        if (document.getElementById('get-sentiment').checked) {
            tasks.push(axios.post(urls.sentiment, { text }));
        }

        Promise.all(tasks)
            .then(results => {
                results.forEach(result => {
                    if (result.config.url.includes('text_keyword')) {
                        setKeywords(result.data.keywords);
                    } else if (result.config.url.includes('text_summary')) {
                        setSummary(result.data.summary);
                    } else if (result.config.url.includes('text_sentiment')) {
                        setSentiment(result.data.sentiment);
                    }
                });
                setIsLoading(false);
            })
            .catch(err => {
                setError('Failed to perform analysis');
                setIsLoading(false);
            });
    };

    // Function to handle opening popup for the selected keyword
    const openTextBox = (keyword) => {
        setSelectedKeyword(keyword);
    };

    // Function to close the popup
    const closePopup = () => {
        setSelectedKeyword(null);
    };

    return (
        <div className="nlp-container">
            <h2>Text Analysis</h2>
            <div>
                <input type="checkbox" id="get-keywords" className="checkbox" onChange={() => handleAnalysis('keywords')} /> Get Keywords
                <input type="checkbox" id="get-summary" className="checkbox" onChange={() => handleAnalysis('summary')} /> Get Summary
                <input type="checkbox" id="get-sentiment" className="checkbox" onChange={() => handleAnalysis('sentiment')} /> Get Sentiment
            </div>
            {isLoading && <p className="loading-text">Loading...</p>}
            {error && <p className="error-text">{error}</p>}
            {summary && <div className="result-block"><h3>Summary:</h3> <p>{summary}</p></div>}
            {sentiment && <div className="result-block"><h3>Sentiment:</h3> <p>{sentiment}</p></div>}
            {keywords.length > 0 && (
                <div className="result-block">
                    <h3>Keywords:</h3>
                    <ul>
                        {keywords.map((keyword, index) => (
                            <li className="keywords" key={index} onClick={() => openTextBox(keyword)}>{keyword}</li>
                        ))}
                    </ul>
                </div>
            )}
            {/* Popup to display the selected keyword */}
            {selectedKeyword && (
                <div className="popup">
                    <div className="popup-content">
                        <span className="close" onClick={closePopup}>&times;</span>
                        <KeywordDefinition word={selectedKeyword} />
                    </div>
                </div>
            )}
        </div>
    );
}

export default NLP;
