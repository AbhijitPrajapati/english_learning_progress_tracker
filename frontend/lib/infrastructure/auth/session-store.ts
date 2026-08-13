import type { SessionStore } from "@/lib/application/ports";
import type { AuthSession } from "@/lib/application/models";

const STORAGE_KEY = "authSession";

function parseOrNull(raw: string | null): AuthSession | null {
  if (!raw) {
    return null;
  }
  try {
    return JSON.parse(raw);
  } catch {
    window.localStorage.removeItem(STORAGE_KEY);
    return null;
  }
}

export function createSessionStore(): SessionStore {
  return {
    getSession: (): AuthSession | null =>
      parseOrNull(window.localStorage.getItem(STORAGE_KEY)),
    setSession: (session: AuthSession) =>
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(session)),
    clearSession: () => window.localStorage.removeItem(STORAGE_KEY),
  };
}
