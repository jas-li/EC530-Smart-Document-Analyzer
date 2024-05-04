import React, { useState } from 'react';
import ConvertToTextButton from '../Extractor/ConvertToTextButton';
import DeleteFileButton from '../Extractor/DeleteFileButton';
import FileUploadForm from '../Extractor/FileUploadForm';
import GetFiles from '../Extractor/GetFiles';  
import NLP from '../NLP/NLP'
import ExtractFromUrl from '../Extractor/ExtractFromUrl';
import './DocumentProcessor.css'; 

function formatText(text) {
    const textParts = text.split('\n').map((line, index) => (
        <React.Fragment key={index}>
            {line}
            <br />
        </React.Fragment>
    ));
    return textParts;
}

function DocumentProcessor() {
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [selectedFileText, setSelectedFileText] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [files, setFiles] = GetFiles(setIsLoading, setError);  
    const [title, setTitle] = useState('');

    return (
        <div className="container">
            <div className="left-panel">
                <h2 className="upload-header">Upload File</h2>
                <FileUploadForm setFiles={setFiles} setError={setError} setSuccess={setSuccess} />
                <ExtractFromUrl
                    setExtractedText={setSelectedFileText} 
                    setTitle={setTitle} 
                    setIsLoading={setIsLoading} 
                    setError={setError} 
                />
                {success && <p>{success}</p>}
                {error && <p>{error}</p>}
                <h2 className="upload-header">Uploaded Files</h2>
                <ul>
                    {files.map((file, index) => (
                        <li key={index} className="file-list-item">
                            {file.name}
                            <ConvertToTextButton filename={file.name} setOutputText={setSelectedFileText} setLoading={setIsLoading} setError={setError} setTitle={setTitle} />
                            <DeleteFileButton filename={file.name} setFiles={setFiles} setError={setError} />
                        </li>
                    ))}
                </ul>
            </div>
            <div className="right-panel">
                <h2 className="upload-header">Document Text</h2>
                {isLoading ? (
                    <p>Loading...</p>
                ) : selectedFileText ? (
                    <div className="file-list">
                        {title && <h3 className="file-title">{title}</h3>}
                        {formatText(selectedFileText)}
                    </div>
                ) : (
                    <div className="empty-placeholder"></div>
                )}
                {selectedFileText && <NLP text={selectedFileText} />}
            </div>
        </div>
    );
}

export default DocumentProcessor;
