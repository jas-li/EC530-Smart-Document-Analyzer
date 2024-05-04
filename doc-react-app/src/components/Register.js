import React, { useState } from 'react';
import axios from 'axios';

function Register() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            await axios.post('http://127.0.0.1:5000/register', {
                "username": username,
                "password": password
            }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            // You can check the response status code if specific actions are needed
            // response.status === 201
            alert('Registration successful');
        } catch (error) {
            if (error.response) {
                // Assuming the server might send back a structured error
                setError(error.response.data.error || 'An unexpected error occurred.');
            } else {
                // This case handles scenarios where the error response is not from the server
                setError('Failed to connect to the server.');
            }
        }
    };

    return (
        <div>
            <h2>Register</h2>
            <form onSubmit={handleSubmit}>
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
            {error && <p>{error}</p>}
        </div>
    );
}

export default Register;