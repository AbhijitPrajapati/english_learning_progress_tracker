"use client";

import { AuthCredentials, AuthSession } from "@/lib/application/models";
import ApplicationUseCases from "@/lib/application/use-cases";
import createUseCases from "@/lib/infrastructure/composition";
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

const UseCaseContext = createContext<ApplicationUseCases | null>(null);

export function UseCaseProvider({ children }: { children: React.ReactNode }) {
  const [useCases] = useState(() => createUseCases());
  return (
    <UseCaseContext.Provider value={useCases}>
      {children}
    </UseCaseContext.Provider>
  );
}

export function useUseCases(): ApplicationUseCases {
  const useCases = useContext(UseCaseContext);
  if (!useCases) {
    throw new Error("useUseCases must be used within a UseCaseProvider");
  }
  return useCases;
}

interface AuthContextValue {
  isAuthenticated: boolean;
  isRestoring: boolean;
  login: (credentials: AuthCredentials) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const {
    restoreSession,
    login: loginUseCase,
    logout: logoutUseCase,
  } = useUseCases();
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [isRestoring, setIsRestoring] = useState(true);

  useEffect(() => {
    function handleRestore(): void {
      const session: AuthSession | null = restoreSession();
      setIsAuthenticated(session !== null);
      setIsRestoring(false);
    }
    handleRestore();
  }, [restoreSession]);

  const login = useCallback(
    async (credentials: AuthCredentials): Promise<void> => {
      await loginUseCase(credentials);
      setIsAuthenticated(true);
    },
    [loginUseCase],
  );

  const logout = useCallback((): void => {
    logoutUseCase();
    setIsAuthenticated(false);
  }, [logoutUseCase]);

  const value = useMemo(
    () => ({
      isAuthenticated,
      isRestoring,
      login,
      logout,
    }),
    [isAuthenticated, isRestoring, login, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
