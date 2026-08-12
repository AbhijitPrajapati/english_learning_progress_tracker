import type { User } from "@/lib/domain/user";
import type { Speech } from "@/lib/domain/speech";
import type {
  Timeframe,
  AnalyticsDistribution,
  AnalyticsTimeSeries,
  AuthCredentials,
  AuthSession,
} from "./models";

export interface AnalyticsGateway {
  getDistribution(timeframe: Timeframe): Promise<AnalyticsDistribution>;
  getTimeSeries(
    timeframe: Timeframe,
    mistakeCategory: string,
  ): Promise<AnalyticsTimeSeries>;
}

export interface AuthGateway {
  login(credentials: AuthCredentials): Promise<AuthSession>;
  register(credentials: AuthCredentials): Promise<User>;
}

export interface SpeechGateway {
  upload(file: File): Promise<Speech>;
}

export interface SessionStore {
  getSession(): AuthSession | null;
  setSession(session: AuthSession): void;
  clearSession(): void;
}
