import type { AccountGateway } from "@/lib/application/ports";
import type { PasswordChange } from "@/lib/application/models";
import type { ApiWireClient } from "../api/wire-client";
import { requireNoContent } from "../api/response";

export default class HttpAccountGateway implements AccountGateway {
  constructor(private readonly client: ApiWireClient) {}

  async changePassword(passwords: PasswordChange): Promise<void> {
    await requireNoContent(
      this.client.PATCH("/api/v1/account/password", {
        body: {
          current_password: passwords.currentPassword,
          new_password: passwords.newPassword,
        },
      }),
    );
  }

  async delete(): Promise<void> {
    await requireNoContent(this.client.DELETE("/api/v1/account"));
  }
}
