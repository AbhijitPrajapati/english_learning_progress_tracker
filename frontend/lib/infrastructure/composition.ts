import { ApiClient } from "@/lib/infrastructure/api/client";
import { createAuthGateway } from "@/lib/infrastructure/auth/gateway";
import { createSpeechGateway } from "@/lib/infrastructure/speech/gateway";
import { createAnalyticsGateway } from "@/lib/infrastructure/analytics/gateway";
import { createSessionStore } from "./auth/session-store";
import ApplicationUseCases from "@/lib/application/use-cases";

const apiClient = new ApiClient();

const authGateway = createAuthGateway(apiClient);
const speechGateway = createSpeechGateway(apiClient);
const analyticsGateway = createAnalyticsGateway(apiClient);

const sessionStore = createSessionStore();

export default function createUseCases(): ApplicationUseCases {
  return new ApplicationUseCases(
    sessionStore,
    authGateway,
    analyticsGateway,
    speechGateway,
  );
}
