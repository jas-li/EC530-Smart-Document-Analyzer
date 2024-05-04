import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Login.css';  // Import the CSS styles

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:5000/login', {
                username,
                password
            });
            sessionStorage.setItem('token', response.data.token);  // Save the token
            navigate('/');  // Redirect to homepage after successful login
        } catch (error) {
            setError(error.response.data.error || 'Login failed');
        }
    };

    return (
        <div className="login-container">
            <h2>Login</h2>
            <form onSubmit={handleSubmit} className="login-form">
                <label>
                    Username: 
                    <input type="text" value={username} onChange={e => setUsername(e.target.value)} />
                </label>
                <label>
                    Password: 
                    <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
                </label>
                <button type="submit">Login</button>
                <Link to="/register"><button type="button">Register</button></Link>
            </form>
            {error && <p className="error-message">{error}</p>}
        </div>
    );
}

export default Login;
