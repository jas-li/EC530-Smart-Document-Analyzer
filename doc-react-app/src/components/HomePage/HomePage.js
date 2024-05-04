import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import DocumentProcessor from '../DocumentProcessor/DocumentProcessor';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';  

function HomePage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = sessionStorage.getItem('token');
    setIsLoggedIn(!!token);  // Update isLoggedIn based on token presence
  }, []);

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

  const handleLogout = () => {
    sessionStorage.removeItem('token');
    navigate('/');
    window.dispatchEvent(new Event('loginChange'));
  };    

  return (
    <div className="homepage-container">
      <h1>Smart Document Analyzer</h1>
      {!isLoggedIn ? (
        <>
          <p>Please log in to access the analysis tools.</p>
          <Link to="/login"><button className="login-button">Login</button></Link>
        </>
      ) : (
        <>
          <button onClick={handleLogout} className="button">Log Out</button>
          <p>Use the tools below to upload and analyze your text:</p>
          <DocumentProcessor />
        </>
      )}
    </div>
  );
}

export default HomePage;
