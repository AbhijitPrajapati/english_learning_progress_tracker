import { AnalyticsPort, AuthPort, SpeechPort } from "./ports";
import type { Timeframe, AuthCredentials } from "./models"


export const createGetDistribution = async (analyticsService: AnalyticsPort) => (timeframe: Timeframe) => analyticsService.getDistribution(timeframe);
export const createGetTimeSeries = async (analyticsService: AnalyticsPort) => (timeframe: Timeframe, mistakeCategory: string) => analyticsService.getTimeSeries(timeframe, mistakeCategory);

export const createLogin = async (authService: AuthPort) => (credentials: AuthCredentials) => authService.login(credentials);
export const createRegister = async (authService: AuthPort) => (credentials: AuthCredentials) => authService.register(credentials);

export const createUpload = async (speechService: SpeechPort) => (file: File) => speechService.upload(file);