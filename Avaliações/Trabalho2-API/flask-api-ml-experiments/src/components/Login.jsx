import './Login.css';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../services/api';

const Login = ({ setUser }) => {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    console.log('Submitting login with:', { email, name });

    try {
      const response = await login(email, name);
      console.log('Response received:', response.data);
      if (response.data.token) {
        setUser(response.data.user, response.data.token);
        navigate('/dashboard')
    }
    } catch (err) {
      console.error('Login error:', err.response.data.error);
      setError(err.response.data.error);
    }
  };

  return (
    <main className='login'>
      <h2 className="login-title">Faça seu login</h2>
      <form className="login-form" onSubmit={handleSubmit}>
        <input
          className="login-component"
          type="text"
          name="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          placeholder="Insira seu nome"
        />
        <input
          className="login-component"
          type="text"
          name="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          placeholder="Insira seu e-mail"
        />
        <input className="login-component submit" type="submit" value="Entrar" />
      </form>
      {error && <p className="error-message">{error}</p>}
    </main>
  );
};

export default Login;
