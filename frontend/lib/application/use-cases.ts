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

  private getToken(): string | null {
    const session = this.sessionStore.getSession();
    return session?.accessToken ?? null;
  }

  async getDistribution(timeframe: Timeframe): Promise<AnalyticsDistribution> {
    return this.analyticsGateway.getDistribution(timeframe, this.getToken());
  }

  async getTimeSeries(
    timeframe: Timeframe,
    mistakeCategory: MistakeCategory,
  ): Promise<AnalyticsTimeSeries> {
    return this.analyticsGateway.getTimeSeries(
      timeframe,
      mistakeCategory,
      this.getToken(),
    );
  }

  async login(credentials: AuthCredentials): Promise<void> {
    const session = await this.authGateway.login(credentials);
    this.sessionStore.setSession(session);
  }

  async register(credentials: AuthCredentials): Promise<User> {
    return this.authGateway.register(credentials);
  }

  async delete_account(): Promise<void> {
    return this.authGateway.delete(this.getToken());
  }

  logout(): void {
    this.sessionStore.clearSession();
  }

  restoreSession(): AuthSession | null {
    return this.sessionStore.getSession();
  }

  async uploadSpeech(file: File): Promise<Speech> {
    return this.speechGateway.upload(file, this.getToken());
  }

  async deleteSpeech(speech_id: string): Promise<void> {
    await this.speechGateway.delete(speech_id, this.getToken());
  }

  async listSpeeches(limit: number, offset: number): Promise<Array<Speech>> {
    return this.speechGateway.list(this.getToken(), limit, offset);
  }
}
