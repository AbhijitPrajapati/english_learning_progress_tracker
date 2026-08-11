import { ApiError } from "@/lib/infrastructure/api/errors";
import { ApiClient } from "./client";
import { InvalidToken } from "@/lib/application/errors";


export class AuthenticatedApiClient {

  constructor(private readonly apiClient: ApiClient, private readonly accessTokenProvider: () => string | null) {
  }

  async request<T>(path: string, init?: RequestInit): Promise<T> {
    const token = this.accessTokenProvider();
    if (!token) {
        throw new InvalidToken();
    }

    const headers = new Headers(init?.headers);
    headers.set("Authorization", `Bearer ${token}`);
    try {
        return this.apiClient.request<T>(path, {...init, headers})
    } catch (error) {
        if (error instanceof ApiError && error.code == "INVALID_TOKEN") {
            throw new InvalidToken();
        }
        throw error;
    }
  }
}
