import type {
  AnalyticsDistribution,
  AnalyticsTimeSeries,
  DateRange,
} from "@/lib/application/models";
import type { MistakeCategoryId } from "@/lib/domain/analysis";
import type { components } from "../api/generated/schema";
import {
  toApiMistakeCategory,
  toDomainMistakeCategory,
} from "../api/mistake-category";
import { toDate } from "../api/scalars";

type DistributionResponse = components["schemas"]["DistributionResponse"];
type TimeSeriesResponse = components["schemas"]["TimeSeriesResponse"];
export function toWireDateRange(dateRange: DateRange): {
  start: string | null;
  end: string | null;
} {
  return {
    start: dateRange.start?.toISOString() ?? null,
    end: dateRange.end?.toISOString() ?? null,
  };
}

export function toWireMistakeCategory(
  category: MistakeCategoryId,
): components["schemas"]["MistakeCategory"] {
  return toApiMistakeCategory(category);
}

export function toDistribution(
  payload: DistributionResponse,
): AnalyticsDistribution {
  return {
    totalSpeeches: payload.total_speeches,
    mistakeFrequencies: payload.mistake_frequencies.map((frequency) => ({
      category: toDomainMistakeCategory(frequency.category),
      occurrences: frequency.occurrences,
      opportunities: frequency.opportunities,
    })),
  };
}

export function toTimeSeries(payload: TimeSeriesResponse): AnalyticsTimeSeries {
  return {
    points: payload.points.map((point) => ({
      time: toDate(point.time),
      occurrences: point.occurrences,
      opportunities: point.opportunities,
    })),
  };
}
