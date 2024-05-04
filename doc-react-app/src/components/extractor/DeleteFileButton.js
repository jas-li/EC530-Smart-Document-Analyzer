import React, { useState } from 'react';
import axios from 'axios';

function DeleteFileButton({ filename, setFiles, setError }) {
    const [isHovering, setIsHovering] = useState(false);  // State to manage hover effect

    const handleDeleteFile = async () => {
        try {
            const response = await axios.post(`http://127.0.0.1:5000/delete_file?filename=${filename}`, {}, {
                headers: {
                    'Authorization': `Basic ${sessionStorage.getItem('token')}`
                }
            });
            if (response.status === 200) {
                setFiles(prevFiles => prevFiles.filter(file => file.name !== filename));
            } else {
                setError(response.data.error || 'Failed to delete file.');
            }
        } catch (error) {
            setError(error.response?.data.error || 'Failed to delete file.');
        }
    };

    // Define inline styles for the button
    const buttonStyle = {
        marginLeft: '10px',
        padding: '10px 20px',
        backgroundColor: isHovering ? '#d32f2f' : '#f44336', // Red background, darker on hover
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        transition: 'background-color 0.3s'
    };

    return (
        <button 
            onClick={handleDeleteFile}
            onMouseEnter={() => setIsHovering(true)}
            onMouseLeave={() => setIsHovering(false)}
            style={buttonStyle}
        >
            Delete
        </button>
    );
}

export default DeleteFileButton;
