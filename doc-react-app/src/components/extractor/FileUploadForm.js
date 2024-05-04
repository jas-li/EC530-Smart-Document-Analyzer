import React, { useState } from 'react';
import axios from 'axios';

function FileUploadForm({ setFiles, setError, setSuccess }) {
    const [file, setFile] = useState(null);

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

    return (
        <form onSubmit={handleSubmit}>
            <input type="file" onChange={e => setFile(e.target.files[0])} />
            <button type="submit">Upload</button>
        </form>
    );
}

export default FileUploadForm;
