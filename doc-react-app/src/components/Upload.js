import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Upload() {
    const [file, setFile] = useState(null);
    const [files, setFiles] = useState([]);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [selectedFileText, setSelectedFileText] = useState('');
    const [isLoading, setIsLoading] = useState(false);  // State to manage loading status

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

    // Function to convert document to text
    const handleDocToText = async (fileName) => {
        setIsLoading(true);  // Start loading
        try {
            const response = await axios.get(`http://127.0.0.1:5000/doc_to_text?filename=${fileName}`, {
                headers: {
                    'Authorization': `Basic ${sessionStorage.getItem('token')}`
                }
            });
            setSelectedFileText(response.data.text);  // Set the text from response
            setIsLoading(false);  // End loading after the response is received
        } catch (error) {
            setError('Failed to convert document to text.');
            setIsLoading(false);  // End loading if there is an error
        }
    };

    // Function to remove files
    const handleDeleteFile = async (filename) => {
        try {
            const response = await axios.post(`http://127.0.0.1:5000/delete_file?filename=${filename}`, {}, {
                headers: {
                    'Authorization': `Basic ${sessionStorage.getItem('token')}`
                }
            });
            if (response.status === 200) {
                setFiles(files.filter(file => file.name !== filename));  // Update state to remove the deleted file from the list
            } else {
                setError(response.data.error || 'Failed to delete file.');
            }
        } catch (error) {
            console.error('Failed to delete file:', error);
            setError(error.response?.data.error || 'Failed to delete file.');
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
        window.dispatchEvent(new Event('loginChange'));  // Notify app of logout
    };

    return (
        <div>
            <h2>Upload File</h2>
            <form onSubmit={handleSubmit}>
                <input type="file" onChange={e => setFile(e.target.files[0])} />
                <button type="submit">Upload</button>
            </form>
            <button onClick={handleLogout}>Log Out</button>
            {isLoading && <p>Loading...</p>} 
            {success && <p>{success}</p>}
            {error && <p>{error}</p>}
            <h3>Uploaded Files</h3>
            <ul>
                {files.map((file, index) => (
                    <li key={index}>
                        {file.name}
                        <button onClick={() => handleDocToText(file.name)} disabled={isLoading}>Convert to Text</button>
                        <button onClick={() => handleDeleteFile(file.name)} style={{ marginLeft: '10px' }}>Delete</button>
                    </li>
                ))}
            </ul>
            {selectedFileText && <div>
                <h3>Document Text</h3>
                <p>{selectedFileText}</p>
            </div>}
        </div>
    );    
}

export default Upload;
