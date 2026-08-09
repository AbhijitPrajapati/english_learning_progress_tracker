import type { User } from "@/lib/domain/user";
import type { Speech } from "@/lib/domain/speech";
import type { Timeframe, AnalyticsDistribution, AnalyticsTimeSeries, AuthCredentials, AuthSession } from "./models"


export interface AnalyticsPort {
  getDistribution(timeframe: Timeframe): Promise<AnalyticsDistribution>;
  getTimeSeries(timeframe: Timeframe, mistakeCategory: string): Promise<AnalyticsTimeSeries>;
}


export interface AuthPort {
  login(credentials: AuthCredentials): Promise<AuthSession>;
  register(credentials: AuthCredentials): Promise<User>;
}


export interface SpeechPort {
  upload(file: File): Promise<Speech>;
}

export interface SessionStorePort {
  getSession(): AuthSession | null;
  setSession(session: AuthSession): void;
  clearSession(): void;
}