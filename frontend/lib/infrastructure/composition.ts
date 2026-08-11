import { ApiClient } from "@/lib/infrastructure/api/client";
import { createAuthGateway } from "@/lib/infrastructure/auth/gateway";
import { createSpeechGateway } from "@/lib/infrastructure/speech/gateway";
import { createAnalyticsGateway } from "@/lib/infrastructure/analytics/gateway";
import { createSessionStore } from "./auth/session-store";
import { createGetDistribution, createGetTimeSeries, createLogin, createLogout, createRegister, createRestoreSession, createUploadSpeech, GetDistribution, GetTimeSeries, Login, Logout, Register, RestoreSession, UploadSpeech } from "@/lib/application/use-cases";
import { AuthenticatedApiClient } from "./api/authenticated-client";


const sessionStore = createSessionStore()
const apiClient = new ApiClient();
const authenticatedApiClient = new AuthenticatedApiClient(apiClient, (): string | null => sessionStore.getSession()?.accessToken ?? null);

const authGateway = createAuthGateway(apiClient);
const speechGateway = createSpeechGateway(authenticatedApiClient);
const analyticsGateway = createAnalyticsGateway(authenticatedApiClient);

export interface ApplicationDependencies {
    getDistribution: GetDistribution,
    getTimeSeries: GetTimeSeries,
    login: Login,
    register: Register,
    logout: Logout,
    restoreSession: RestoreSession,
    uploadSpeech: UploadSpeech
}

export const createDependencies = (): ApplicationDependencies => ({
    getDistribution: createGetDistribution(analyticsGateway),
    getTimeSeries: createGetTimeSeries(analyticsGateway),
    login: createLogin(authGateway, sessionStore),
    register: createRegister(authGateway),
    logout: createLogout(sessionStore),
    restoreSession: createRestoreSession(sessionStore),
    uploadSpeech: createUploadSpeech(speechGateway)
});