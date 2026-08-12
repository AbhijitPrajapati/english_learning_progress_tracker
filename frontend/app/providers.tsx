"use client";

import { AuthCredentials, AuthSession } from "@/lib/application/models";
import {
  ApplicationDependencies,
  createDependencies,
} from "@/lib/infrastructure/composition";
import { createContext, useContext, useEffect, useMemo, useState } from "react";

const DependencyContext = createContext<ApplicationDependencies | null>(null);

export function DependencyProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const dependencies = useMemo(() => createDependencies(), []);
  return (
    <DependencyContext.Provider value={dependencies}>
      {children}
    </DependencyContext.Provider>
  );
}

export const useDependencies = (): ApplicationDependencies => {
  const dependencies = useContext(DependencyContext);
  if (!dependencies) {
    throw new Error("useDependencies must be used within a DependencyProvider");
  }
  return dependencies;
};

interface AuthContextValue {
  session: AuthSession | null;
  isRestoring: boolean;
  login: (credentials: AuthCredentials) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const {
    login: loginUseCase,
    logout: logoutUseCase,
    restoreSession: restoreSessionUseCase,
  } = useDependencies();

  const [session, setSession] = useState<AuthSession | null>(null);
  const [isRestoring, setIsRestoring] = useState(true);

  useEffect(() => {
    const restore = async () => {
      try {
        const session = restoreSessionUseCase();
        setSession(session);
      } finally {
        setIsRestoring(false);
      }
    };

    void restore();
  }, [restoreSessionUseCase]);

  const login = async (credentials: AuthCredentials) => {
    const session = await loginUseCase(credentials);
    setSession(session);
  };

  const logout = async () => {
    logoutUseCase();
    setSession(null);
  };

  const value: AuthContextValue = {
    session,
    isRestoring,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
