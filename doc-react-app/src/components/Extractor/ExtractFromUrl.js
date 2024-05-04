import React, { useState } from 'react';
import axios from 'axios';

function ExtractFromUrl({ setExtractedText, setTitle, setTopImage, setIsLoading, setError }) {
    const [url, setUrl] = useState('');
    const [isHovering, setIsHovering] = useState(false);  // State to manage hover effect

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
            setIsLoading(false);
        }
    };

    // Define inline styles
    const inputStyle = {
        padding: '8px',
        margin: '5px 10px 5px 0',
        width: '50%', 
        fontSize: '16px',
        borderRadius: '4px',
        border: '1px solid #ccc'
    };

    const buttonStyle = {
        padding: '10px 20px',
        backgroundColor: isHovering ? '#357a38' : '#4caf50', // Green background, darker on hover
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        transition: 'background-color 0.3s'
    };

    return (
        <div>
            <input
                type="text"
                placeholder="Enter URL to extract text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                style={inputStyle}
            />
            <button
                onClick={handleExtractFromUrl}
                onMouseEnter={() => setIsHovering(true)}
                onMouseLeave={() => setIsHovering(false)}
                disabled={!url.trim()}
                style={buttonStyle}
            >
                Extract Text
            </button>
        </div>
    );
}

export default ExtractFromUrl;
