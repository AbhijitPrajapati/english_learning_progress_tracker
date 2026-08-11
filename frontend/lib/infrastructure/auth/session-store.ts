import type { SessionStore } from "@/lib/application/ports";
import type { AuthSession } from "@/lib/application/models"

const STORAGE_KEY = "authSession"

const parseOrNull = (raw: string | null): AuthSession | null => raw ? JSON.parse(raw) : null;

export const createSessionStore = (): SessionStore => ({
    getSession: (): AuthSession | null => parseOrNull(window.localStorage.getItem(STORAGE_KEY)),
    setSession: (session: AuthSession) => window.localStorage.setItem(STORAGE_KEY, JSON.stringify(session)),
    clearSession: () => window.localStorage.removeItem(STORAGE_KEY),
});