import type { MistakeCategoryId } from "@/lib/domain/analysis";
import type { Speech } from "@/lib/domain/speech";
import type { User } from "@/lib/domain/user";
import type {
  AnalyticsDistribution,
  AnalyticsTimeSeries,
  AudioSample,
  AuthCredentials,
  AuthSession,
  DateRange,
  PasswordChange,
} from "./models";

export interface AnalyticsGateway {
  getDistribution(dateRange: DateRange): Promise<AnalyticsDistribution>;
  getTimeSeries(
    dateRange: DateRange,
    mistakeCategory: MistakeCategoryId,
  ): Promise<AnalyticsTimeSeries>;
}

export interface AuthGateway {
  login(credentials: AuthCredentials): Promise<AuthSession>;
  register(credentials: AuthCredentials): Promise<User>;
  getSession(): Promise<AuthSession>;
  logout(): Promise<void>;
}

export interface AccountGateway {
  changePassword(passwords: PasswordChange): Promise<void>;
  delete(): Promise<void>;
}

export interface SpeechGateway {
  upload(audio: AudioSample): Promise<Speech>;
  delete(speechId: string): Promise<void>;
  list(limit: number, offset: number): Promise<Speech[]>;
}
