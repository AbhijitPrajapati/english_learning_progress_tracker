import ApiClient from "@/lib/infrastructure/api/client";
import HttpAuthGateway from "@/lib/infrastructure/auth/gateway";
import HttpSpeechGateway from "@/lib/infrastructure/speech/gateway";
import LocalSessionStore from "./auth/session-store";
import ApplicationUseCases from "@/lib/application/use-cases";
import HttpAnalyticsGateway from "./analytics/gateway";
import AuthenticatedApiClient from "./api/authenticated-client";
import HttpAccountGateway from "./account/gateway";

const apiClient = new ApiClient();
const authenticatedApiClient = new AuthenticatedApiClient(apiClient);

const authGateway = new HttpAuthGateway(apiClient);
const accountGateway = new HttpAccountGateway(authenticatedApiClient);
const speechGateway = new HttpSpeechGateway(authenticatedApiClient);
const analyticsGateway = new HttpAnalyticsGateway(authenticatedApiClient);

const sessionStore = new LocalSessionStore();

export default function createUseCases(): ApplicationUseCases {
  return new ApplicationUseCases(
    sessionStore,
    authGateway,
    accountGateway,
    analyticsGateway,
    speechGateway,
  );
}
