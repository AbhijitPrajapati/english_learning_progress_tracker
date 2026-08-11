import { AnalyticsGateway, AuthGateway, SessionStore, SpeechGateway } from "./ports";
import type { Timeframe, AuthCredentials, AnalyticsDistribution, AnalyticsTimeSeries, AuthSession } from "./models"
import { MistakeCategory } from "@/lib/domain/analysis";
import { Speech } from "@/lib/domain/speech";
import { User } from "@/lib/domain/user";

export type GetDistribution = (timeframe: Timeframe) => Promise<AnalyticsDistribution>;
export const createGetDistribution = (analyticsGateway: AnalyticsGateway): GetDistribution => async (timeframe: Timeframe) => analyticsGateway.getDistribution(timeframe);

export type GetTimeSeries = (timeframe: Timeframe, mistakeCategory: MistakeCategory) => Promise<AnalyticsTimeSeries>;
export const createGetTimeSeries = (analyticsGateway: AnalyticsGateway): GetTimeSeries => async (timeframe: Timeframe, mistakeCategory: MistakeCategory) => analyticsGateway.getTimeSeries(timeframe, mistakeCategory);

export type Login = (credentials: AuthCredentials) => Promise<AuthSession>;
export const createLogin = (authGateway: AuthGateway, sessionStore: SessionStore): Login => async (credentials: AuthCredentials) => {
    const session = await authGateway.login(credentials);
    sessionStore.setSession(session);
    return session;
};

export type Register = (credentials: AuthCredentials) => Promise<User>;
export const createRegister = (authGateway: AuthGateway): Register => async (credentials: AuthCredentials) => authGateway.register(credentials);

export type Logout = () => void;
export const createLogout = (sessionStore: SessionStore): Logout => async () => sessionStore.clearSession();

export type RestoreSession = () => AuthSession | null;
export const createRestoreSession = (sessionStore: SessionStore): RestoreSession => () => sessionStore.getSession(); 

export type UploadSpeech = (file: File) => Promise<Speech>;
export const createUploadSpeech = (speechGateway: SpeechGateway): UploadSpeech => async (file: File) => speechGateway.upload(file);