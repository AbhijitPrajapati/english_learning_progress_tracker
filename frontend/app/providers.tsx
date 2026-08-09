"use client";

import { createContext, useCallback, useContext, useMemo, useState } from "react";
import { authService, sessionStore } from "@/lib/infrastructure/composition";
import { AuthSession, AuthCredentials } from "@/lib/application/models";

type AuthContextValue = {
  userId: string | null,
  isAuthenticated: boolean,
  login: (credentials: AuthCredentials) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [session, setSession] = useState<AuthSession | null>(() => sessionStore.getSession(),);

  const userId = session?.userId ?? null;
  const isAuthenticated = session !== null;

  const login = useCallback(async (credentials: AuthCredentials) => {
    const session = await authService.login(credentials);
    sessionStore.setSession(session);
    setSession(session);
  }, []);

  const logout = useCallback(() => {
    sessionStore.clearSession();
    setSession(null);
  }, [])

  const value = useMemo(() => ({ userId: userId, isAuthenticated, login, logout }), [userId, isAuthenticated, login, logout]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }

  return context;
}
