import { createContext, useState, useContext } from 'react';

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);

  const login = (role) => {
    let name = 'User';
    if (role === 'EMPLOYEE') name = 'Alex Employee';
    if (role === 'MANAGER') name = 'Sam Manager';
    if (role === 'ADMIN') name = 'Admin Sys';
    
    setCurrentUser({ role, name });
  };

  const logout = () => {
    setCurrentUser(null);
  };

  return (
    <AppContext.Provider value={{ currentUser, login, logout }}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => useContext(AppContext);
