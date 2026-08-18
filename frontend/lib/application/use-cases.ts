import type { MistakeCategoryId } from "@/lib/domain/analysis";
import type { Speech } from "@/lib/domain/speech";
import type { User } from "@/lib/domain/user";
import { InvalidToken } from "./errors";
import type {
  AnalyticsDistribution,
  AnalyticsTimeSeries,
  AudioSample,
  AuthCredentials,
  AuthSession,
  DateRange,
  PasswordChange,
} from "./models";
import type {
  AccountGateway,
  AnalyticsGateway,
  AuthGateway,
  SpeechGateway,
} from "./ports";

export type SessionListener = () => void;

interface Dependencies {
  authGateway: AuthGateway;
  accountGateway: AccountGateway;
  analyticsGateway: AnalyticsGateway;
  speechGateway: SpeechGateway;
}

export class Application {
  private session: AuthSession | null = null;
  private readonly listeners = new Set<SessionListener>();

  constructor(private readonly dependencies: Dependencies) {}

  private publishSession(nextSession: AuthSession | null): void {
    this.session = nextSession;
    this.listeners.forEach((listener) => listener());
  }

  private async authenticated<T>(operation: () => Promise<T>): Promise<T> {
    try {
      return await operation();
    } catch (error) {
      if (error instanceof InvalidToken) this.publishSession(null);
      throw error;
    }
  }

  readonly auth = {
    subscribe: (listener: SessionListener): (() => void) => {
      this.listeners.add(listener);
      return () => {
        this.listeners.delete(listener);
      };
    },
    getSnapshot: (): AuthSession | null => this.session,
    restore: async (): Promise<AuthSession | null> => {
      try {
        const restored = await this.dependencies.authGateway.getSession();
        this.publishSession(restored);
        return restored;
      } catch (error) {
        if (error instanceof InvalidToken) {
          this.publishSession(null);
          return null;
        }
        throw error;
      }
    },
    login: async (credentials: AuthCredentials): Promise<void> => {
      this.publishSession(
        await this.dependencies.authGateway.login(credentials),
      );
    },
    register: async (credentials: AuthCredentials): Promise<User> => {
      const user = await this.dependencies.authGateway.register(credentials);
      this.publishSession(
        await this.dependencies.authGateway.login(credentials),
      );
      return user;
    },
    logout: async (): Promise<void> => {
      try {
        await this.dependencies.authGateway.logout();
      } finally {
        this.publishSession(null);
      }
    },
  };

  readonly account = {
    changePassword: (passwords: PasswordChange): Promise<void> =>
      this.authenticated(() =>
        this.dependencies.accountGateway.changePassword(passwords),
      ),
    delete: async (): Promise<void> => {
      await this.authenticated(() => this.dependencies.accountGateway.delete());
      this.publishSession(null);
    },
  };

  readonly analytics = {
    getDistribution: (dateRange: DateRange): Promise<AnalyticsDistribution> =>
      this.authenticated(() =>
        this.dependencies.analyticsGateway.getDistribution(dateRange),
      ),
    getTimeSeries: (
      dateRange: DateRange,
      mistakeCategory: MistakeCategoryId,
    ): Promise<AnalyticsTimeSeries> =>
      this.authenticated(() =>
        this.dependencies.analyticsGateway.getTimeSeries(
          dateRange,
          mistakeCategory,
        ),
      ),
  };

  readonly speeches = {
    upload: (audio: AudioSample): Promise<Speech> =>
      this.authenticated(() => this.dependencies.speechGateway.upload(audio)),
    delete: (speechId: string): Promise<void> =>
      this.authenticated(() =>
        this.dependencies.speechGateway.delete(speechId),
      ),
    list: (): Promise<Speech[]> =>
      this.authenticated(() => this.dependencies.speechGateway.list(100, 0)),
  };
}
