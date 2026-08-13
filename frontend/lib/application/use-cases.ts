import {
  AnalyticsGateway,
  AuthGateway,
  SessionStore,
  SpeechGateway,
} from "./ports";
import type {
  Timeframe,
  AuthCredentials,
  AnalyticsDistribution,
  AnalyticsTimeSeries,
  AuthSession,
} from "./models";
import { MistakeCategory } from "@/lib/domain/analysis";
import { Speech } from "@/lib/domain/speech";
import { User } from "@/lib/domain/user";

export default class ApplicationUseCases {
  constructor(
    private readonly sessionStore: SessionStore,
    private readonly authGateway: AuthGateway,
    private readonly analyticsGateway: AnalyticsGateway,
    private readonly speechGateway: SpeechGateway,
  ) {}

  async getDistribution(timeframe: Timeframe): Promise<AnalyticsDistribution> {
    const session = this.sessionStore.getSession();
    return this.analyticsGateway.getDistribution(
      timeframe,
      session?.accessToken ?? null,
    );
  }

  async getTimeSeries(
    timeframe: Timeframe,
    mistakeCategory: MistakeCategory,
  ): Promise<AnalyticsTimeSeries> {
    const session = this.sessionStore.getSession();
    return this.analyticsGateway.getTimeSeries(
      timeframe,
      mistakeCategory,
      session?.accessToken ?? null,
    );
  }

  async login(credentials: AuthCredentials): Promise<void> {
    const session = await this.authGateway.login(credentials);
    this.sessionStore.setSession(session);
  }

  async register(credentials: AuthCredentials): Promise<User> {
    return this.authGateway.register(credentials);
  }

  logout(): void {
    this.sessionStore.clearSession();
  }

  restoreSession(): AuthSession | null {
    return this.sessionStore.getSession();
  }

  async uploadSpeech(file: File): Promise<Speech> {
    const session = this.sessionStore.getSession();
    return this.speechGateway.upload(file, session?.accessToken ?? null);
  }
}
