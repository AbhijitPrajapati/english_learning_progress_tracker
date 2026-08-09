import { ApiClient } from "@/lib/infrastructure/api/client";
import { createAuthService } from "@/lib/infrastructure/api/auth";
import { createSpeechService } from "@/lib/infrastructure/api/speech";
import { createAnalyticsService } from "@/lib/infrastructure/api/analytics";
import { createSessionStore } from "./session_store";


export const sessionStore = createSessionStore()
const apiClient = new ApiClient((): string | null => sessionStore.getSession()?.accessToken ?? null);

export const authService = createAuthService(apiClient);
export const speechService = createSpeechService(apiClient);
export const analyticsService = createAnalyticsService(apiClient);
