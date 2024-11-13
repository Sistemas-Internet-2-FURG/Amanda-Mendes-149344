import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Header.css';  // Import the CSS file

const Header = ({ user, onLogout}) => {
  const navigate = useNavigate();
  console.log(user);
  return (
    <header className="header">
      <div className="side-info">
        <div className="welcome-message">
          {user ? (
            <span className="header-title">Welcome, {user.name}!</span>
          ) : null}
        </div>
        <div className="login-logout">
          {user ? (
            <>
              <button className="logout" onClick={onLogout}>
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  {/* Door icon */}
                  <path
                    d="M6 2H18c1.1 0 2 .9 2 2v16c0 1.1-.9 2-2 2H6c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2zm0 2v16h12V4H6zm7 7v-2h-5v2h5zm0 4v-2h-5v2h5z"
                    fill="#FFFFFF"
                  />
                  {/* Arrow icon */}
                  <path
                    d="M16.59 13.59L14.17 16l-1.42-1.42L15.34 12l-2.59-2.59L14.17 8l2.42 2.42L18.83 12l-2.42 2.42z"
                    fill="#FFFFFF"
                  />
                </svg>
                Logout
              </button>
            </>
          ) : (
            <>
              <button className="logout" onClick={() => navigate("/login")}>
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  {/* Door icon */}
                  <path
                    d="M6 2H18c1.1 0 2 .9 2 2v16c0 1.1-.9 2-2 2H6c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2zm0 2v16h12V4H6zm7 7v-2h-5v2h5zm0 4v-2h-5v2h5z"
                    fill="#FFFFFF"
                  />
                  {/* Arrow icon */}
                  <path
                    d="M16.59 13.59L14.17 16l-1.42-1.42L15.34 12l-2.59-2.59L14.17 8l2.42 2.42L18.83 12l-2.42 2.42z"
                    fill="#FFFFFF"
                  />
                </svg>
                Login
              </button>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
