import { useState, useEffect } from 'react';
import axios from 'axios';

const GetFiles = (setIsLoading, setError) => {
    const [files, setFiles] = useState([]);

    useEffect(() => {
        const fetchFiles = async () => {
            setIsLoading(true);
            try {
                const response = await axios.get('http://127.0.0.1:5000/get_files', {
                    headers: {
                        'Authorization': `Basic ${sessionStorage.getItem('token')}`
                    }
                });
                const filesArray = Object.entries(response.data.files).map(([name, id]) => ({ name, id }));
                setFiles(filesArray);
                setIsLoading(false);
            } catch (error) {
                setError(error.response?.data.error || 'Failed to fetch files');
                setIsLoading(false);
            }
        };

        fetchFiles();
    }, [setIsLoading, setError]);

    return [files, setFiles];
};

export default GetFiles;
