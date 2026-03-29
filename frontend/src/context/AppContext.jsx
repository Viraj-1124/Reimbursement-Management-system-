import { createContext, useState, useContext } from 'react';

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);

  const login = async (email, password) => {
    try {
      const response = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });
      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('auth_token', data.token);
        
        let name = 'User';
        if (data.role === 'EMPLOYEE') name = 'Alex Employee';
        if (data.role === 'MANAGER') name = 'Sam Manager';
        if (data.role === 'ADMIN') name = 'Admin Sys';

        setCurrentUser({ role: data.role, name });
        return data.role;
      } else {
        console.error('Login failed');
        return false;
      }
    } catch (e) {
      console.error('Network error during login', e);
      return false;
    }
  };

  const register = async (name, email, password, company_name, country) => {
    try {
      const response = await fetch('http://localhost:8000/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password, company_name: company_name || null, country: country || null })
      });
      if (response.ok) {
        // Automatically login
        return await login(email, password);
      }
      return false;
    } catch(e) {
      console.error(e);
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    setCurrentUser(null);
  };

  return (
    <AppContext.Provider value={{ currentUser, login, register, logout }}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => useContext(AppContext);
