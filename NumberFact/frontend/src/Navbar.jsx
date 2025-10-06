import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function Navbar() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuthStatus = () => {
      const token = localStorage.getItem('token');
      setIsLoggedIn(!!token);
    };

    checkAuthStatus(); // Check on initial mount

    window.addEventListener('authChange', checkAuthStatus);

    return () => {
      window.removeEventListener('authChange', checkAuthStatus);
    };
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
    window.dispatchEvent(new Event('authChange')); // Dispatch event on logout
    navigate('/login');
  };

  const handleLoginRegisterClick = () => {
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-brand-container">
        <span>Number Facts App</span>
      </div>
      <div className="navbar-actions">
        {isLoggedIn ? (
          <button onClick={handleLogout} className="nav-link logout-button">Logout</button>
        ) : (
          <button onClick={handleLoginRegisterClick} className="nav-link login-register-button">Login / Register</button>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
