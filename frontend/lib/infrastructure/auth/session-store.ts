import type { SessionStore } from "@/lib/application/ports";
import type { AuthSession } from "@/lib/application/models";

const STORAGE_KEY = "authSession";

export default class LocalSessionStore implements SessionStore {
  getSession(): AuthSession | null {
    const raw = window.localStorage.getItem(STORAGE_KEY);
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
  setSession(session: AuthSession): void {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(session));
  }
  clearSession(): void {
    window.localStorage.removeItem(STORAGE_KEY);
  }
}
