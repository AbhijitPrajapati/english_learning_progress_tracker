import { describe, expect, it, vi } from "vitest";

import { InvalidToken } from "./errors";
import { Application } from "./use-cases";
import type {
  AccountGateway,
  AnalyticsGateway,
  AuthGateway,
  SpeechGateway,
} from "./ports";

function dependencies() {
  const authGateway: AuthGateway = {
    login: vi.fn(async () => ({ userId: "user-1" })),
    register: vi.fn(async ({ email }) => ({
      id: "user-1",
      email,
      createdAt: new Date("2026-01-01T00:00:00Z"),
    })),
    getSession: vi.fn(async () => ({ userId: "user-1" })),
    logout: vi.fn(async () => undefined),
  };
  const accountGateway: AccountGateway = {
    changePassword: vi.fn(async () => undefined),
    delete: vi.fn(async () => undefined),
  };
  const analyticsGateway: AnalyticsGateway = {
    getDistribution: vi.fn(async () => ({
      totalSpeeches: 0,
      mistakeFrequencies: [],
    })),
    getTimeSeries: vi.fn(async () => ({ points: [] })),
  };
  const speechGateway: SpeechGateway = {
    upload: vi.fn(),
    delete: vi.fn(async () => undefined),
    list: vi.fn(async () => []),
  };
  return { authGateway, accountGateway, analyticsGateway, speechGateway };
}

describe("application session policy", () => {
  it("registers, logs in, and publishes the server session", async () => {
    const gateways = dependencies();
    const application = new Application(gateways);
    const sessions: Array<string | null> = [];
    application.auth.subscribe(() =>
      sessions.push(application.auth.getSnapshot()?.userId ?? null),
    );

    await application.auth.register({
      email: "learner@example.com",
      password: "long-enough-password",
    });

    expect(gateways.authGateway.register).toHaveBeenCalledOnce();
    expect(gateways.authGateway.login).toHaveBeenCalledOnce();
    expect(sessions).toEqual(["user-1"]);
  });

  it("clears local session state when a protected operation is rejected", async () => {
    const gateways = dependencies();
    gateways.speechGateway.list = vi.fn(async () => {
      throw new InvalidToken();
    });
    const application = new Application(gateways);
    const sessions: Array<string | null> = [];
    application.auth.subscribe(() =>
      sessions.push(application.auth.getSnapshot()?.userId ?? null),
    );
    await application.auth.login({ email: "a@b.com", password: "password" });

    await expect(application.speeches.list()).rejects.toBeInstanceOf(
      InvalidToken,
    );
    expect(sessions).toEqual(["user-1", null]);
  });

  it("treats an invalid restore cookie as an anonymous session", async () => {
    const gateways = dependencies();
    gateways.authGateway.getSession = vi.fn(async () => {
      throw new InvalidToken();
    });
    const application = new Application(gateways);

    await expect(application.auth.restore()).resolves.toBeNull();
  });

  it("clears the session after account deletion", async () => {
    const gateways = dependencies();
    const application = new Application(gateways);
    const sessions: Array<string | null> = [];
    application.auth.subscribe(() =>
      sessions.push(application.auth.getSnapshot()?.userId ?? null),
    );
    await application.auth.login({ email: "a@b.com", password: "password" });

    await application.account.delete();

    expect(gateways.accountGateway.delete).toHaveBeenCalledOnce();
    expect(sessions).toEqual(["user-1", null]);
  });

  it("changes a password without disturbing the active session", async () => {
    const gateways = dependencies();
    const application = new Application(gateways);
    await application.auth.login({ email: "a@b.com", password: "password" });

    await application.account.changePassword({
      currentPassword: "old-password",
      newPassword: "new-password",
    });

    expect(gateways.accountGateway.changePassword).toHaveBeenCalledWith({
      currentPassword: "old-password",
      newPassword: "new-password",
    });
    expect(application.auth.getSnapshot()).toEqual({ userId: "user-1" });
  });
});
