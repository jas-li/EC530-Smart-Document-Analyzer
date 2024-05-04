import React, { useState } from 'react';
import axios from 'axios';

function NLP({ text }) {
    const [keywords, setKeywords] = useState('');
    const [summary, setSummary] = useState('');
    const [sentiment, setSentiment] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const handleAnalysis = async (type) => {
        setIsLoading(true);
        setError('');

        // Clear previous results based on what is checked
        if (type === 'keywords') setKeywords('');
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
                        setKeywords(result.data.keywords.join(', '));
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

    return (
        <div>
            <h3>Text Analysis</h3>
            <div>
                <input type="checkbox" id="get-keywords" onChange={() => handleAnalysis('keywords')} /> Get Keywords
                <input type="checkbox" id="get-summary" onChange={() => handleAnalysis('summary')} /> Get Summary
                <input type="checkbox" id="get-sentiment" onChange={() => handleAnalysis('sentiment')} /> Get Sentiment
            </div>
            {isLoading && <p>Loading...</p>}
            {error && <p>{error}</p>}
            {keywords && <div><h4>Keywords:</h4> <p>{keywords}</p></div>}
            {summary && <div><h4>Summary:</h4> <p>{summary}</p></div>}
            {sentiment && <div><h4>Sentiment:</h4> <p>{sentiment}</p></div>}
        </div>
    );
}

export default NLP;
