import { CategoryFrequency, Frequency } from "@/lib/domain/analysis";

export interface AuthCredentials {
  email: string;
  password: string;
}

export interface AnalyticsDistribution {
  totalSamples: number;
  mistakeFrequencies: CategoryFrequency[];
}

export interface Timeframe {
  start: string;
  end: string;
}

export interface TimeSeriesPoint extends Frequency {
  time: string;
}

export interface AnalyticsTimeSeries {
  points: TimeSeriesPoint[];
}

export interface AuthSession {
  accessToken: string;
  tokenType: string;
  userId: string;
}
