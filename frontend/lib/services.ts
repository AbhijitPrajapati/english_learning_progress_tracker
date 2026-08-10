import { createGetDistribution, createGetTimeSeries, createLogin, createRegister, createUpload } from "./application/use_cases";
import { analyticsService, authService, speechService } from "./infrastructure/composition";

export const getDistribution = await createGetDistribution(analyticsService);
export const getTimeSeries = await createGetTimeSeries(analyticsService);

export const login = await createLogin(authService);
export const register = await createRegister(authService);

export const uploadSpeech = await createUpload(speechService);