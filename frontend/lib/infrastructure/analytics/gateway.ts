import type {
  AnalyticsDistribution,
  AnalyticsTimeSeries,
  DateRange,
} from "@/lib/application/models";
import type { AnalyticsGateway } from "@/lib/application/ports";
import type { MistakeCategoryId } from "@/lib/domain/analysis";
import type { ApiWireClient } from "../api/wire-client";
import { requireData } from "../api/response";
import {
  toDistribution,
  toTimeSeries,
  toWireDateRange,
  toWireMistakeCategory,
} from "./mapper";

export default class HttpAnalyticsGateway implements AnalyticsGateway {
  constructor(private readonly client: ApiWireClient) {}

  async getDistribution(dateRange: DateRange): Promise<AnalyticsDistribution> {
    const payload = await requireData(
      this.client.POST("/api/v1/analytics/distribution", {
        body: { date_range: toWireDateRange(dateRange) },
      }),
    );
    return toDistribution(payload);
  }

  async getTimeSeries(
    dateRange: DateRange,
    mistakeCategory: MistakeCategoryId,
  ): Promise<AnalyticsTimeSeries> {
    const payload = await requireData(
      this.client.POST("/api/v1/analytics/time-series", {
        body: {
          date_range: toWireDateRange(dateRange),
          mistake_category: toWireMistakeCategory(mistakeCategory),
        },
      }),
    );
    return toTimeSeries(payload);
  }
}
