import type { AnalyticsPort } from "@/lib/application/ports";
import type { AnalyticsDistribution, Timeframe, AnalyticsTimeSeries } from "@/lib/application/models";
import type { MistakeCategory } from "@/lib/domain/analysis";
import type { ApiClient } from "@/lib/infrastructure/api/client";

interface MistakeFrequencyResponse {
  occurances: number;
  opportunities: number;
  category: MistakeCategory;
}

interface DistributionResponse {
  total_samples: number; 
  mistake_frequencies: MistakeFrequencyResponse[]
}

interface TimeSeriesPointResponse {
  occurances: number;
  opportunities: number;
  time: string;
}

interface TimeSeriesResponse {
  points: TimeSeriesPointResponse[]
}

export const createAnalyticsService = (client: ApiClient): AnalyticsPort => ({
  getDistribution: async (timeframe: Timeframe): Promise<AnalyticsDistribution> => {
    const payload = await client.request<DistributionResponse>("/analytics/distribution", {
      method: "POST",
      body: JSON.stringify({ timeframe }),
    });
    return {
      totalSamples: payload.total_samples,
      mistakeFrequencies: payload.mistake_frequencies.map((freq: MistakeFrequencyResponse) => ({
        category: freq.category,
        opportunities: freq.opportunities,
        occurances: freq.occurances
      })),
    }
  },

  getTimeSeries: async (timeframe: Timeframe, mistakeCategory: MistakeCategory): Promise<AnalyticsTimeSeries> => {
    const payload = await client.request<TimeSeriesResponse>("/analytics/time-series", {
        method: "POST",
        body: JSON.stringify({ timeframe, mistake_category: mistakeCategory }),
      });
    return {
      points: payload.points.map((freq: TimeSeriesPointResponse) => ({
        time: freq.time,
        opportunities: freq.opportunities,
        occurances: freq.occurances
      })),
    };
  },
});
