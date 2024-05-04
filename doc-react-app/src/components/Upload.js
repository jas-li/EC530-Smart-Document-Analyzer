import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Upload() {
    const [file, setFile] = useState(null);
    const [files, setFiles] = useState([]);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const navigate = useNavigate();

    // Function to fetch files from the server
    const fetchFiles = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/get_files', {
                headers: {
                    'Authorization': `Basic ${sessionStorage.getItem('token')}`
                }
            });
            const filesArray = Object.entries(response.data.files).map(([name, id]) => ({ name, id }));
            setFiles(filesArray);
        } catch (error) {
            setError(error.response?.data.error || 'Failed to fetch files');
        }
    };

    // Effect to run fetchFiles on mount
    useEffect(() => {
        fetchFiles();
    }, []);

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
            fetchFiles(); // Re-fetch the files list after successful upload
        } catch (error) {
            setError(error.response?.data.error || 'Upload failed');
        }
    };

    const handleLogout = () => {
        sessionStorage.removeItem('token');
        navigate('/');
    };

    return (
        <div>
            <h2>Upload File</h2>
            <form onSubmit={handleSubmit}>
                <input type="file" onChange={e => setFile(e.target.files[0])} />
                <button type="submit">Upload</button>
            </form>
            <button onClick={handleLogout}>Log Out</button>
            {success && <p>{success}</p>}
            {error && <p>{error}</p>}
            <h3>Uploaded Files</h3>
            <ul>
                {files.map((file, index) => (
                    <li key={index}>{file.name}</li>
                ))}
            </ul>
        </div>
    );
}

export default Upload;
