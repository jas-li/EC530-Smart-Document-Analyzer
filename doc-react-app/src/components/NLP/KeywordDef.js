import React, { useState, useEffect } from 'react';
import axios from 'axios';

function KeywordDefinition({ word }) {
    const [definitions, setDefinitions] = useState([]);
    const [partOfSpeech, setPartOfSpeech] = useState('');
    const [pronunciation, setPronunciation] = useState('');
    const [nytimesLinks, setNytimesLinks] = useState([]);
    const [wikipediaLinks, setWikipediaLinks] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchContent = async () => {
            try {
                const linksResponse = await axios.get(`http://127.0.0.1:5000/content_links`, {
                    params: { keyword: word }
                });
                setNytimesLinks(linksResponse.data.nytimes_links.slice(0, 2));
                setWikipediaLinks(linksResponse.data.wikipedia_links.slice(0, 1));
            } catch (error) {
                setError('Failed to fetch content links');
            }
        };

        const fetchDefinitions = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/keyword_def', {
                    params: { word: word }
                });
                const data = response.data;
                if (data.definitions) {
                    setDefinitions(data.definitions);
                    setPartOfSpeech(data.part_of_speech);
                    setPronunciation(data.pronunciation);
                    // fetchContent();  // Fetch content links after successful definition fetch
                } else {
                    setError('Definition not found');
                }
            } catch (error) {
                setError('No definition found');
            }
        };

        fetchDefinitions();
        fetchContent();
    }, [word]);

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '10px', width: '550px' }}>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '0px' }}>
                <h2 style={{ margin: '0', marginRight: '5px', verticalAlign: 'bottom' }}>{word}</h2>
                <p style={{ margin: '0', fontSize: '1rem', color: '#666', verticalAlign: 'bottom' }}>{partOfSpeech}</p>
            </div>
            {error && <p style={{ margin: '5px 0' }}>{error}</p>}
            {definitions.length > 0 && (
                <div style={{ marginBottom: '5px', paddingTop: '5px', textAlign: 'center' }}>
                    <p style={{ margin: '0', fontSize: '1rem', color: '#666' }}>/ {pronunciation} /</p>
                    <h3 style={{ textAlign: 'left', marginBottom: '5px', marginTop: '5px', color: '#E76F51' }}>Definitions:</h3>
                    <ul style={{ textAlign: 'left', marginTop: '0', marginBottom: '0', color: '#264653' }}>
                        {definitions.map((definition, index) => (
                            <li key={index}>{index + 1}. {definition}</li>
                        ))}
                    </ul>
                </div>
            )}
            <div>
                <h3 style={{ textAlign: 'left', marginBottom: '5px', marginTop: '5px', color: '#E76F51' }}>Wikipedia:</h3>
                {wikipediaLinks.map((link, index) => (
                    <p style={{ textAlign: 'left' }} key={index}><a href={link} style={{ color: '#007bff'}}>{link}</a></p>
                ))}
                <h3 style={{ textAlign: 'left', marginBottom: '5px', marginTop: '5px', color: '#E76F51' }}>New York Times Articles:</h3>
                {nytimesLinks.map((link, index) => (
                    <p style={{ textAlign: 'left' }} key={index}><a href={link} style={{ color: '#007bff'}}>{link}</a></p>
                ))}
            </div>
        </div>
    );      
}

export default KeywordDefinition;
