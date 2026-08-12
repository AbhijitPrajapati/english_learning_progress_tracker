import {
  AnalyticsGateway,
  AuthGateway,
  SessionStore,
  SpeechGateway,
} from "./ports";
import type {
  Timeframe,
  AuthCredentials,
  AnalyticsDistribution,
  AnalyticsTimeSeries,
  AuthSession,
} from "./models";
import { MistakeCategory } from "@/lib/domain/analysis";
import { Speech } from "@/lib/domain/speech";
import { User } from "@/lib/domain/user";

export type GetDistribution = (
  timeframe: Timeframe,
) => Promise<AnalyticsDistribution>;
export function createGetDistribution(
  analyticsGateway: AnalyticsGateway,
): GetDistribution {
  return async (timeframe: Timeframe) =>
    analyticsGateway.getDistribution(timeframe);
}

export type GetTimeSeries = (
  timeframe: Timeframe,
  mistakeCategory: MistakeCategory,
) => Promise<AnalyticsTimeSeries>;

export function createGetTimeSeries(
  analyticsGateway: AnalyticsGateway,
): GetTimeSeries {
  return async (timeframe: Timeframe, mistakeCategory: MistakeCategory) =>
    analyticsGateway.getTimeSeries(timeframe, mistakeCategory);
}

export type Login = (credentials: AuthCredentials) => Promise<AuthSession>;
export function createLogin(
  authGateway: AuthGateway,
  sessionStore: SessionStore,
): Login {
  return async (credentials: AuthCredentials) => {
    const session = await authGateway.login(credentials);
    sessionStore.setSession(session);
    return session;
  };
}

export type Register = (credentials: AuthCredentials) => Promise<User>;
export function createRegister(authGateway: AuthGateway): Register {
  return async (credentials: AuthCredentials) =>
    authGateway.register(credentials);
}

export type Logout = () => void;
export function createLogout(sessionStore: SessionStore): Logout {
  return async () => sessionStore.clearSession();
}

export type RestoreSession = () => AuthSession | null;
export function createRestoreSession(
  sessionStore: SessionStore,
): RestoreSession {
  return () => sessionStore.getSession();
}

export type UploadSpeech = (file: File) => Promise<Speech>;
export function createUploadSpeech(speechGateway: SpeechGateway): UploadSpeech {
  return async (file: File) => speechGateway.upload(file);
}
