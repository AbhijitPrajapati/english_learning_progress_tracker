import ApiClient from "@/lib/infrastructure/api/client";
import HttpAuthGateway from "@/lib/infrastructure/auth/gateway";
import HttpSpeechGateway from "@/lib/infrastructure/speech/gateway";
import LocalSessionStore from "./auth/session-store";
import ApplicationUseCases from "@/lib/application/use-cases";
import HttpAnalyticsGateway from "./analytics/gateway";
import AuthenticatedApiClient from "./api/authenticated-client";

const apiClient = new ApiClient();
const authenticatedApiClient = new AuthenticatedApiClient(apiClient);

const authGateway = new HttpAuthGateway(apiClient);
const speechGateway = new HttpSpeechGateway(authenticatedApiClient);
const analyticsGateway = new HttpAnalyticsGateway(authenticatedApiClient);

const sessionStore = new LocalSessionStore();

export default function createUseCases(): ApplicationUseCases {
  return new ApplicationUseCases(
    sessionStore,
    authGateway,
    analyticsGateway,
    speechGateway,
  );
}
