import type { AnalyticsGateway } from "@/lib/application/ports";
import type {
  AnalyticsDistribution,
  Timeframe,
  AnalyticsTimeSeries,
} from "@/lib/application/models";
import { components } from "../openapi-schema";
import AuthenticatedApiClient from "../api/authenticated-client";

type DistributionResponse = components["schemas"]["DistributionResponse"];
type MistakeFrequencyResponse = components["schemas"]["MistakeFrequency"];
type TimeSeriesResponse = components["schemas"]["TimeSeriesResponse"];
export default class HttpAnalyticsGateway implements AnalyticsGateway {
  constructor(private readonly client: AuthenticatedApiClient) {}

  async getDistribution(
    timeframe: Timeframe,
    accessToken: string | null,
  ): Promise<AnalyticsDistribution> {
    const payload = await this.client.request<DistributionResponse>(
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
  }

  async getTimeSeries(
    timeframe: Timeframe,
    mistakeCategory: string,
    accessToken: string | null,
  ): Promise<AnalyticsTimeSeries> {
    return this.client.request<TimeSeriesResponse>("/analytics/time-series", {
      method: "POST",
      body: JSON.stringify({
        timeframe,
        mistake_category: mistakeCategory,
      }),
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
    });
  }
}
