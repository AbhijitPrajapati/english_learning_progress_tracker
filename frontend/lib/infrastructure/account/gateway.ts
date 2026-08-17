import { AccountGateway } from "@/lib/application/ports";
import AuthenticatedApiClient from "../api/authenticated-client";

export default class HttpAccountGateway implements AccountGateway {
  constructor(private readonly client: AuthenticatedApiClient) {}

  async delete(accessToken: string | null): Promise<void> {
    await this.client.request("/account/", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
    });
  }
}
