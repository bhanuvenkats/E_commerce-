/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useEffect, useState } from "react";
import api from "../api/api";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);

  // Restore session on page refresh
  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    if (storedToken) {
      setToken(storedToken);
      setUser({}); // placeholder, decode token later if needed
    }
  }, []);

  // Login using backend API
  const login = async (credentials) => {
    const res = await api.post("/login", credentials);

    const accessToken = res.data.token || res.data.access_token;
    const profile = res.data.profile || res.data.user || {};

    localStorage.setItem("token", accessToken);
    setToken(accessToken);
    setUser(profile);

    return res.data;
  };

  // Logout and clear session
  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        login,
        logout,
        isAuthenticated: !!token,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);