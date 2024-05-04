import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Upload from './Upload';

function HomePage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = sessionStorage.getItem('token');
    setIsLoggedIn(!!token);  // Update isLoggedIn based on token presence
  }, []);

  // Listen to custom event to trigger re-check of login state
  useEffect(() => {
    const handleLoginChange = () => {
      const token = sessionStorage.getItem('token');
      setIsLoggedIn(!!token);
    };

    window.addEventListener('loginChange', handleLoginChange);

    return () => {
      window.removeEventListener('loginChange', handleLoginChange);
    };
  }, []);

  return (
    <div>
      <h1>Welcome</h1>
      {!isLoggedIn ? (
        <Link to="/login"><button>Login</button></Link>
      ) : (
        <Upload />
      )}
    </div>
  );
}

export default HomePage;
