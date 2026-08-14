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
  getDistribution(
    timeframe: Timeframe,
    accessToken: string | null,
  ): Promise<AnalyticsDistribution>;
  getTimeSeries(
    timeframe: Timeframe,
    mistakeCategory: string,
    accessToken: string | null,
  ): Promise<AnalyticsTimeSeries>;
}

export interface AuthGateway {
  login(credentials: AuthCredentials): Promise<AuthSession>;
  register(credentials: AuthCredentials): Promise<User>;
  delete(accessToken: string | null): Promise<void>;
}

export interface SpeechGateway {
  upload(file: File, accessToken: string | null): Promise<Speech>;
  delete(speech_id: string, accessToken: string | null): Promise<void>;
  list(
    accessToken: string | null,
    limit: number,
    offset: number,
  ): Promise<Array<Speech>>;
}

export interface SessionStore {
  getSession(): AuthSession | null;
  setSession(session: AuthSession): void;
  clearSession(): void;
}
