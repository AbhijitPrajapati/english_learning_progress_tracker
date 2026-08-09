import { ApiError, NetworkError } from "@/lib/infrastructure/api/errors";

type AccessTokenProvider = () => string | null

export class ApiClient {

  constructor(private readonly accessTokenProvider: AccessTokenProvider, private readonly baseUrl = "/api") {
  }

  private buildUrl(path: string) {
    return `${this.baseUrl}${path}`;
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      let body: unknown;

      try {
        body = await response.json();
      } catch {
        body = undefined;
      }

      throw new ApiError(response.status, body)
    }

    return response.json();
  }

  async request<T>(path: string, init?: RequestInit): Promise<T> {
    const headers = new Headers(init?.headers);

    if (init?.body instanceof FormData) {
      headers.delete("Content-Type");
    } else if (init?.body && !headers.has("Content-Type")) {
      headers.set("Content-Type", "application/json");
    }

    const token = this.accessTokenProvider()
    if (token) {
      headers.set("Authorization", `Bearer ${token}`);
    }

    let response: Response;
    try {
      response = await fetch(this.buildUrl(path), {
        ...init,
        headers,
      });
    } catch (cause) {
      throw new NetworkError({ cause });
    }

    return this.handleResponse<T>(response);
  }
}
