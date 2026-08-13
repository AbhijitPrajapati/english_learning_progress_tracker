import type { AnalyticsGateway } from "@/lib/application/ports";
import type {
  AnalyticsDistribution,
  Timeframe,
  AnalyticsTimeSeries,
} from "@/lib/application/models";
import type { MistakeCategory } from "@/lib/domain/analysis";
import { ApiClient } from "../api/client";
import { ApiError } from "../api/errors";
import { InvalidToken } from "@/lib/application/errors";

interface MistakeFrequencyResponse {
  occurances: number;
  opportunities: number;
  category: MistakeCategory;
}

interface DistributionResponse {
  total_samples: number;
  mistake_frequencies: MistakeFrequencyResponse[];
}

interface TimeSeriesPointResponse {
  occurances: number;
  opportunities: number;
  time: string;
}

interface TimeSeriesResponse {
  points: TimeSeriesPointResponse[];
}

export function createAnalyticsGateway(client: ApiClient): AnalyticsGateway {
  return {
    getDistribution: async (
      timeframe: Timeframe,
      accessToken: string | null,
    ): Promise<AnalyticsDistribution> => {
      try {
        const payload = await client.request<DistributionResponse>(
          "/analytics/distribution",
          {
            method: "POST",
            body: JSON.stringify({ timeframe }),
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${accessToken}`,
            },
          },
        );
        return {
          totalSamples: payload.total_samples,
          mistakeFrequencies: payload.mistake_frequencies.map(
            (freq: MistakeFrequencyResponse) => ({
              category: freq.category,
              opportunities: freq.opportunities,
              occurances: freq.occurances,
            }),
          ),
        };
      } catch (error) {
        if (error instanceof ApiError && error.code == "INVALID_TOKEN") {
          throw new InvalidToken();
        }
        throw error;
      }
    },

    getTimeSeries: async (
      timeframe: Timeframe,
      mistakeCategory: MistakeCategory,
      accessToken: string | null,
    ): Promise<AnalyticsTimeSeries> => {
      try {
        const payload = await client.request<TimeSeriesResponse>(
          "/analytics/time-series",
          {
            method: "POST",
            body: JSON.stringify({
              timeframe,
              mistake_category: mistakeCategory,
            }),
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${accessToken}`,
            },
          },
        );
        return {
          points: payload.points.map((freq: TimeSeriesPointResponse) => ({
            time: freq.time,
            opportunities: freq.opportunities,
            occurances: freq.occurances,
          })),
        };
      } catch (error) {
        if (error instanceof ApiError && error.code == "INVALID_TOKEN") {
          throw new InvalidToken();
        }
        throw error;
      }
    },
  };
}
