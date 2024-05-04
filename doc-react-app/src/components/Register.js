import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Login/Login.css';  // Assuming the CSS file is still named Login.css

function Register() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:5000/register', {
                username,
                password
            }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (response.status === 201) {  // Check if the registration was successful
                alert('Registration successful');
                navigate('/login');
            }
        } catch (error) {
            setError(error.response ? error.response.data.error || 'An unexpected error occurred.' : 'Failed to connect to the server.');
        }
    };

    return (
        <div className="login-container">
            <h2>Register</h2>
            <form onSubmit={handleSubmit} className="login-form">
                <label>
                    Username:
                    <input type="text" value={username} onChange={e => setUsername(e.target.value)} />
                </label>
                <label>
                    Password:
                    <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
                </label>
                <button type="submit">Register</button>
            </form>
            {error && <p className="error-message">{error}</p>}
        </div>
    );
}

export default Register;