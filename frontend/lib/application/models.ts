import type { CategoryFrequency, Frequency } from "@/lib/domain/analysis";

export interface AuthCredentials {
  email: string;
  password: string;
}

export interface AuthSession {
  userId: string;
}

export interface PasswordChange {
  currentPassword: string;
  newPassword: string;
}

export interface AudioSample {
  content: ArrayBuffer;
  filename: string;
  mediaType: string;
}

export interface AnalyticsDistribution {
  totalSpeeches: number;
  mistakeFrequencies: CategoryFrequency[];
}

export interface DateRange {
  start: Date | null;
  end: Date | null;
}

export interface TimeSeriesPoint extends Frequency {
  time: Date;
}

export interface AnalyticsTimeSeries {
  points: TimeSeriesPoint[];
}
