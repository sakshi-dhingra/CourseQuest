import React, { useState } from 'react';
import './Login.css'; // Import CSS file for styling
import { Link, useNavigate } from 'react-router-dom';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [loginSuccess, setLoginSuccess] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`http://localhost:5000/login?user_email=${username}&user_password=${password}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        setLoginSuccess(true);
        const name = username;
        setTimeout(() => {
          navigate('/home', { state: { username: name } });
        }, 5000);
      } else {
        const data = await response.json();
        setErrorMessage(data.message || 'Login failed');
      }
    } catch (error) {
      console.error('Error:', error);
      setErrorMessage('An error occurred. Please try again later.');
    }
  };

  const LoginSuccessMessage = () => (
    <div className="blank-page">
      <div className="success-message-container">
        <p className="success-message">Login Successful</p>
      </div>
    </div>
  );

  return (
    <>
      {!loginSuccess ? (
        <div className="login-container">
          <h2>Login</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="username">Email:</label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="password">Password:</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            {errorMessage && <div className="error-message">{errorMessage}</div>}
            <button type="submit">Login</button>
          </form>
          <p>
            New user? <Link to="/register">Register here</Link>
          </p>
        </div>
      ) : (
        <LoginSuccessMessage />
      )}
    </>
  );
};

export default Login;
