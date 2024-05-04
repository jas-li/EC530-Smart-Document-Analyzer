import React, { useState } from 'react';
import axios from 'axios';

function ConvertToTextButton({ filename, setOutputText, setLoading, setError, setTitle }) {
    const [isHovering, setIsHovering] = useState(false);

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

    // Define the inline style object
    const normalStyle = {
        backgroundColor: '#4CAF50', 
        color: 'white',             
        padding: '10px 20px',       
        border: 'none',             
        borderRadius: '5px',        
        cursor: 'pointer',          
        outline: 'none',            
        margin: '10px',            
        transition: 'background-color 0.3s'
    };

    const hoverStyle = {
        ...normalStyle,
        backgroundColor: '#45a049'
    };

    return (
        <button 
            onClick={handleDocToText} 
            style={isHovering ? hoverStyle : normalStyle}
            onMouseEnter={() => setIsHovering(true)}
            onMouseLeave={() => setIsHovering(false)}
        >
            Convert to Text
        </button>
    );
}

export default ConvertToTextButton;
