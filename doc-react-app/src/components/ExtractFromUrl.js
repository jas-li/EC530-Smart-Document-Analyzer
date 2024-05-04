import React, { useState } from 'react';
import axios from 'axios';

function ExtractFromUrl({ setExtractedText, setTitle, setTopImage, setIsLoading, setError }) {
    const [url, setUrl] = useState('');

    const handleExtractFromUrl = async () => {
        if (!url) {
            setError("Please enter a URL.");
            return;
        }
        setIsLoading(true);
        try {
            const response = await axios.post('http://127.0.0.1:5000/extract_from_url', { url }, {
                headers: {
                    'Authorization': `Basic ${sessionStorage.getItem('token')}`
                }
            });
            setExtractedText(response.data.text);
            setTitle(response.data.title);
            setTopImage(response.data.top_image);
            setIsLoading(false);
        } catch (error) {
            setError(error.response?.data.error);
            setIsLoading(false);
        }
    };

    return (
        <div>
            <input
                type="text"
                placeholder="Enter URL to extract text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                style={{ marginRight: '10px' }}
            />
            <button onClick={handleExtractFromUrl} disabled={!url.trim()}>Extract Text</button>
        </div>
    );
}

export default ExtractFromUrl;
