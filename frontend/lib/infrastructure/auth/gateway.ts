import { AuthCredentials, AuthSession } from "@/lib/application/models";
import type { AuthGateway } from "@/lib/application/ports";

import { User } from "@/lib/domain/user";
import { ApiClient } from "@/lib/infrastructure/api/client";
import { ApiError } from "../api/errors";
import {
  EmailAlreadyRegistered,
  InvalidCredentials,
} from "@/lib/application/errors";

interface LoginResponse {
  access_token: string;
  token_type: string;
  user_id: string;
}

interface RegisterResponse {
  id: string;
  email: string;
  created_at: string;
}

export const createAuthGateway = (client: ApiClient): AuthGateway => ({
  login: async (credentials: AuthCredentials): Promise<AuthSession> => {
    try {
      const payload = await client.request<LoginResponse>("/auth/login", {
        method: "POST",
        body: JSON.stringify(credentials),
        headers: {
          "Content-Type": "application/json",
        },
      });
      return {
        accessToken: payload.access_token,
        tokenType: payload.token_type,
        userId: payload.user_id,
      };
    } catch (error) {
      if (error instanceof ApiError && error.status === 401) {
        throw new InvalidCredentials();
      }
      throw error;
    }
  },
  register: async (credentials: AuthCredentials): Promise<User> => {
    try {
      const payload = await client.request<RegisterResponse>("/auth/register", {
        method: "POST",
        body: JSON.stringify(credentials),
        headers: {
          "Content-Type": "application/json",
        },
      });
      return {
        id: payload.id,
        email: payload.email,
        createdAt: new Date(payload.created_at),
      };
    } catch (error) {
      if (error instanceof ApiError && error.status === 409) {
        throw new EmailAlreadyRegistered();
      }
      throw error;
    }
  },
});
