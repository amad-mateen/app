import React, { useState } from 'react';
import axios from 'axios';

function Registration() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/signup', { username, password });
      setMessage('Registration successful!');
      window.location.href = '/fraud-check';
    } catch (err) {
      setMessage(err.response?.data?.detail || 'Registration failed');
    }
  };

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required />
        <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
        <button type="submit">Sign Up</button>
      </form>
      <p>{message}</p>
      <a href="/login">Already have an account? Login</a>
    </div>
  );
}

export default Registration;
