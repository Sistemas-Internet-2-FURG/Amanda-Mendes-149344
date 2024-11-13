import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import AddExperimentForm from './components/AddExperimentForm';
import Header from './components/Header';
import EditExperimentForm from './components/EditExperimentForm';

function App() {
  const [user, setUser] = useState(() => {
    if(localStorage.getItem('user') !== null){
      return JSON.parse(localStorage.getItem('user'))
    }

    return null;
  });

  const [token, setToken] = useState(() => {
    if(localStorage.getItem('token') !== null){
      return JSON.parse(localStorage.getItem('token'))
    }

    return null;
  });

  useEffect(() => {
    if (user) {
      localStorage.setItem('user', JSON.stringify(user));
    } else {
      localStorage.removeItem('user');
    }
  }, [user]);

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', JSON.stringify(token));
    } else {
      localStorage.removeItem('token');
    }
  }, [token]);

  // Handle login action
  const handleLogin = (userInfo, tokenInfo) => {
    setUser(userInfo); // Set user info when logged in
    setToken(tokenInfo); // Set token when logged in
  };

  // Handle logout action
  const handleLogout = () => {
    setUser(null); // Clear user info when logged out
    setToken(null); // Clear token when logged out
  };

  return (
    <Router>
      <div>
        <Header user={user} onLogout={handleLogout} />
        <Routes>
          <Route path="/" element={<Dashboard user={user} />} />
          <Route path="/login" element={<Login setUser={handleLogin} />} />
          <Route path="/dashboard" element={<Dashboard user={user} />} />
          <Route path="/add-experiment" element={<AddExperimentForm user={user} />} />
          <Route path="/edit-experiment/:experiment" element={<EditExperimentForm />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
