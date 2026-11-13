import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';
import type { User } from '../types';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: { email: string; username: string; password: string; full_name?: string }) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(() => {
    const saved = localStorage.getItem('bhashaai_user');
    return saved ? JSON.parse(saved) : null;
  });
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('bhashaai_token'));
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const fetchProfile = async () => {
    try {
      const profile = await api.auth.getMe();
      setUser(profile);
      localStorage.setItem('bhashaai_user', JSON.stringify(profile));
    } catch (err) {
      console.warn('Session verification failed, logging out...');
      setUser(null);
      setToken(null);
      localStorage.removeItem('bhashaai_token');
      localStorage.removeItem('bhashaai_user');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (token) {
      fetchProfile();
    } else {
      setIsLoading(false);
    }
  }, [token]);

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const data = await api.auth.login(email, password);
      localStorage.setItem('bhashaai_token', data.access_token);
      setToken(data.access_token);
      const profile = await api.auth.getMe();
      setUser(profile);
      localStorage.setItem('bhashaai_user', JSON.stringify(profile));
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (data: { email: string; username: string; password: string; full_name?: string }) => {
    setIsLoading(true);
    try {
      await api.auth.register(data);
      // Automatically log in upon successful registration
      await login(data.email, data.password);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    await api.auth.logout();
    setUser(null);
    setToken(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!token && !!user,
        isLoading,
        login,
        register,
        logout,
        refreshUser: fetchProfile
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

