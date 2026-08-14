import { ApiError, NetworkError } from "@/lib/infrastructure/api/errors";

export default class ApiClient {
  constructor(private readonly baseUrl = "/api") {}

  async request<T>(path: string, init?: RequestInit): Promise<T> {
    const url = `${this.baseUrl}${path}`;
    let response: Response;
    try {
      response = await fetch(url, init);
    } catch (cause) {
      throw new NetworkError({ cause });
    }

    const json = await response.json();
    if (!response.ok) {
      throw new ApiError(response.status, json.detail, json.code);
    }
    return json;
  }
}
