import type { AuthCredentials, AuthSession } from "@/lib/application/models";
import type { AuthGateway } from "@/lib/application/ports";
import type { User } from "@/lib/domain/user";
import type { ApiWireClient } from "../api/wire-client";
import { requireData, requireNoContent } from "../api/response";
import { toDate } from "../api/scalars";

export default class HttpAuthGateway implements AuthGateway {
  constructor(private readonly client: ApiWireClient) {}

  async login(credentials: AuthCredentials): Promise<AuthSession> {
    const payload = await requireData(
      this.client.POST("/api/v1/auth/login", { body: credentials }),
    );
    return { userId: payload.user_id };
  }

  async register(credentials: AuthCredentials): Promise<User> {
    const payload = await requireData(
      this.client.POST("/api/v1/auth/register", { body: credentials }),
    );
    return {
      id: payload.id,
      email: payload.email,
      createdAt: toDate(payload.created_at),
    };
  }

  async getSession(): Promise<AuthSession> {
    const payload = await requireData(this.client.GET("/api/v1/auth/session"));
    return { userId: payload.user_id };
  }

  async logout(): Promise<void> {
    await requireNoContent(this.client.POST("/api/v1/auth/logout"));
  }
}
