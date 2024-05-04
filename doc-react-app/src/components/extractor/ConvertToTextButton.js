import React from 'react';
import axios from 'axios';

function ConvertToTextButton({ filename, setOutputText, setLoading, setError, setTitle }) {
    const handleDocToText = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`http://127.0.0.1:5000/doc_to_text?filename=${filename}`, {
                headers: {
                    'Authorization': `Basic ${sessionStorage.getItem('token')}`
                }
            });
            setOutputText(response.data.text);
            setTitle(filename);
            setLoading(false);
        } catch (error) {
            setError('Failed to convert document to text.');
            setLoading(false);
        }
    };

    return <button onClick={handleDocToText}>Convert to Text</button>;
}

export default ConvertToTextButton;
