// Upload.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ConvertToTextButton from './extractor/ConvertToTextButton';
import DeleteFileButton from './extractor/DeleteFileButton';
import FileUploadForm from './extractor/FileUploadForm';
import GetFiles from './extractor/GetFiles';  
import NLP from './NLP'
import ExtractFromUrl from './ExtractFromUrl';

function formatText(text) {
    const textParts = text.split('\n').map((line, index) => (
        <React.Fragment key={index}>
            {line}
            <br />
        </React.Fragment>
    ));
    return textParts;
}

function Upload() {
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [selectedFileText, setSelectedFileText] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [files, setFiles] = GetFiles(setIsLoading, setError);  

    const [title, setTitle] = useState('');
    // const [topImage, setTopImage] = useState('');

    const navigate = useNavigate();

    const handleLogout = () => {
        sessionStorage.removeItem('token');
        navigate('/');
        window.dispatchEvent(new Event('loginChange'));
    };

    return (
        <div>
            <h2>Upload File</h2>
            <FileUploadForm setFiles={setFiles} setError={setError} setSuccess={setSuccess} />
            <ExtractFromUrl
                setExtractedText={setSelectedFileText} 
                setTitle={setTitle} 
                // setTopImage={setTopImage} 
                setIsLoading={setIsLoading} 
                setError={setError} 
            />
            <button onClick={handleLogout}>Log Out</button>
            {success && <p>{success}</p>}
            {error && <p>{error}</p>}
            <h3>Uploaded Files</h3>
            <ul>
                {files.map((file, index) => (
                    <li key={index}>
                        {file.name}
                        <ConvertToTextButton filename={file.name} setOutputText={setSelectedFileText} setLoading={setIsLoading} setError={setError} setTitle={setTitle} />
                        <DeleteFileButton filename={file.name} setFiles={setFiles} setError={setError} />
                    </li>
                ))}
            </ul>
            {isLoading ? (
                <p>Loading...</p>
            ) : (
                selectedFileText && (
                    <div>
                        <h3>Document Text</h3>
                        {title && <h3>{title}</h3>}
                        {/* {topImage && <img src={topImage} alt="Top of the article" style={{ maxWidth: '25%' }} />} */}
                        <div style={{
                            maxHeight: '300px',
                            overflowY: 'auto',
                            border: '2px solid #000', // Add a border
                            borderRadius: '10px', // Rounded corners
                            width: '50%', // Set the width to half of the screen
                        }}>
                            {formatText(selectedFileText)}
                        </div>
                        <NLP text={selectedFileText} />
                    </div>
                )
            )}
        </div>
    );
}

export default Upload;