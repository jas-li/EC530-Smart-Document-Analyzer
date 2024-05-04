import React, { useState } from 'react';
import axios from 'axios';

function FileUploadForm({ setFiles, setError, setSuccess }) {
    const [file, setFile] = useState(null);
    const [isHovering, setIsHovering] = useState(false);  // State to manage hover effect

    const handleSubmit = async (event) => {
        event.preventDefault();
        const formData = new FormData();
        formData.append('file', file);

        try {
            await axios.post('http://127.0.0.1:5000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Authorization': `Basic ${sessionStorage.getItem('token')}`
                }
            });
            setSuccess('File uploaded successfully.');
            setFiles(prev => [...prev, { name: file.name, id: 'newlyGeneratedId' }]); // Adjust as per actual API response
        } catch (error) {
            setError(error.response?.data.error || 'Upload failed');
        }
    };

    // Inline styles for the button
    const buttonStyle = {
        width: '100px',
        padding: '10px 20px',
        backgroundColor: isHovering ? '#3e8e41' : '#4CAF50',  // Change color on hover
        color: 'white',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        outline: 'none',
        transition: 'background-color 0.3s'
    };

    return (
        <form onSubmit={handleSubmit} style={{ padding: '20px' }}>
            <input type="file" onChange={e => setFile(e.target.files[0])} style={{ marginBottom: '10px' }} />
            <button 
                type="submit" 
                style={buttonStyle}
                onMouseEnter={() => setIsHovering(true)}
                onMouseLeave={() => setIsHovering(false)}
            >
                Upload
            </button>
        </form>
    );
}

export default FileUploadForm;
