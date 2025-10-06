import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

function Login() {
  const [id, setId] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8888/login', { id, password });
      if (response.data.token) {
        localStorage.setItem('token', response.data.token);
        // Dispatch custom event to notify Navbar of auth change
        window.dispatchEvent(new Event('authChange'));
        setMessage('Login successful!');
        navigate('/dashboard');
      } else {
        setMessage(response.data.status);
      }
    } catch (error) {
      setMessage('Error during login.');
      console.error('Login error:', error);
    }
  };

  return (
    <div className="auth-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>ID:</label>
          <input type="text" value={id} onChange={(e) => setId(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Password:</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        <button type="submit">Login</button>
      </form>
      {message && <p className="message">{message}</p>}
      <p>Don't have an account? <Link to="/">Register here</Link></p>
    </div>
  );
}

export default Login;
