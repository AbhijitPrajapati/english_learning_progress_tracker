"use client";

import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { clearAuthToken, getStoredAuthToken, saveAuthToken } from "@/lib/api";

type AuthContextValue = {
  token: string | null;
  userId: string | null;
  login: (token: string, userId: string) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    const storedToken = getStoredAuthToken();
    if (storedToken) {
      setToken(storedToken);
      setUserId(window.localStorage.getItem("authUserId"));
    }
  }, []);

  const login = (nextToken: string, nextUserId: string) => {
    saveAuthToken(nextToken);
    window.localStorage.setItem("authUserId", nextUserId);
    setToken(nextToken);
    setUserId(nextUserId);
  };

  const logout = () => {
    clearAuthToken();
    window.localStorage.removeItem("authUserId");
    setToken(null);
    setUserId(null);
  };

  const value = useMemo(() => ({ token, userId, login, logout }), [token, userId]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }

  return context;
}
