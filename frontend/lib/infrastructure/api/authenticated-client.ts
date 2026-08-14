import { ApiError } from "@/lib/infrastructure/api/errors";
import ApiClient from "./client";
import { InvalidToken } from "@/lib/application/errors";

export default class AuthenticatedApiClient {
  constructor(private readonly apiClient: ApiClient) {}

  async request<T>(path: string, init?: RequestInit): Promise<T> {
    try {
      return this.apiClient.request(path, init);
    } catch (error) {
      if (error instanceof ApiError && error.code == "INVALID_TOKEN") {
        throw new InvalidToken();
      }
      throw error;
    }
  }
}
