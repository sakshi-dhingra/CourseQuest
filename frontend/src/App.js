import React, { useState } from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Register from './Component/Register/register';
import Login from './Component/Login/Login'
import Home from './Component/Home/home'
function App() {
  const [message, setMessage] = useState('');
  const [username, setUsername] = useState('');

  const handleMessage = (msg) => {
    
    setMessage(msg);

  };


  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/register" element={<Register handleMessage={handleMessage} />} />
          <Route path="/" element={<Login handleMessage={handleMessage} setUsername={setUsername}  />} />
          <Route path="/home" element={<Home handleMessage={handleMessage} username={username}/>} />
          
        </Routes>
        {message && <p className="message">{message}</p>}
      </div>
    </Router>
  );
}

export default App;
