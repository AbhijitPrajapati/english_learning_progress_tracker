"use client";

import type { Application } from "@/lib/application/use-cases";
import composeApplication from "@/lib/infrastructure/composition";
import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  useSyncExternalStore,
} from "react";

const ApplicationContext = createContext<Application | null>(null);

export function ApplicationProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [application] = useState(composeApplication);
  return (
    <ApplicationContext.Provider value={application}>
      {children}
    </ApplicationContext.Provider>
  );
}

export function useApplication(): Application {
  const application = useContext(ApplicationContext);
  if (!application) {
    throw new Error("useApplication must be used within ApplicationProvider");
  }
  return application;
}

interface AuthContextValue {
  isAuthenticated: boolean;
  isRestoring: boolean;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const application = useApplication();
  const session = useSyncExternalStore(
    application.auth.subscribe,
    application.auth.getSnapshot,
    () => null,
  );
  const [isRestoring, setIsRestoring] = useState(true);

  useEffect(() => {
    application.auth
      .restore()
      .catch(() => undefined)
      .finally(() => setIsRestoring(false));
  }, [application]);

  const value = useMemo(
    () => ({
      isAuthenticated: session !== null,
      isRestoring,
    }),
    [session, isRestoring],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
}
