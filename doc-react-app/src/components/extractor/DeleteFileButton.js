import React from 'react';
import axios from 'axios';

function DeleteFileButton({ filename, setFiles, setError }) {
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

    return <button onClick={handleDeleteFile} style={{ marginLeft: '10px' }}>Delete</button>;
}

export default DeleteFileButton;
