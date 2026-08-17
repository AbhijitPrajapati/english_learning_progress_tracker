"use client";

import { useEffect, useMemo, useState } from "react";

import { useApplication } from "@/app/providers";
import { AnalyticsFilters } from "@/components/analytics/AnalyticsFilters";
import { DistributionPanel } from "@/components/analytics/DistributionPanel";
import { TimeSeriesPanel } from "@/components/analytics/TimeSeriesPanel";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type {
  AnalyticsDistribution,
  AnalyticsTimeSeries,
  DateRange,
} from "@/lib/application/models";
import type { MistakeCategoryId } from "@/lib/domain/analysis";
import {
  MISTAKE_CATEGORY_OPTIONS,
  mistakeCategoryLabel,
} from "@/lib/presentation/mistake-categories";

const DATE_RANGES = [
  { value: "all_time", label: "All Time" },
  { value: "yearly", label: "Yearly" },
  { value: "monthly", label: "Monthly" },
  { value: "weekly", label: "Weekly" },
] as const;
type DateRangeSelection = (typeof DATE_RANGES)[number]["value"];

function getDateRange(selected: DateRangeSelection): DateRange {
  const end = new Date();
  const days = selected === "weekly" ? 7 : selected === "monthly" ? 30 : 365;
  const start = new Date(end.getTime() - days * 24 * 60 * 60 * 1000);
  return {
    start: selected === "all_time" ? null : start,
    end: selected === "all_time" ? null : end,
  };
}

export default function AnalyticsPage() {
  const application = useApplication();
  const [dateRange, setDateRange] = useState<DateRangeSelection>("monthly");
  const [mistakeCategory, setMistakeCategory] = useState<MistakeCategoryId>(
    MISTAKE_CATEGORY_OPTIONS[0].id,
  );
  const [distribution, setDistribution] =
    useState<AnalyticsDistribution | null>(null);
  const [timeSeries, setTimeSeries] = useState<AnalyticsTimeSeries | null>(
    null,
  );
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    const selectedRange = getDateRange(dateRange);

    Promise.all([
      application.analytics.getDistribution(selectedRange),
      application.analytics.getTimeSeries(selectedRange, mistakeCategory),
    ])
      .then(([nextDistribution, nextTimeSeries]) => {
        if (cancelled) return;
        setDistribution(nextDistribution);
        setTimeSeries(nextTimeSeries);
      })
      .catch(() => {
        if (!cancelled) setError("Unable to load analytics.");
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [application, dateRange, mistakeCategory]);

  const selectedDateRangeLabel = useMemo(
    () =>
      DATE_RANGES.find((option) => option.value === dateRange)?.label ??
      "All time",
    [dateRange],
  );
  const selectedCategoryLabel = mistakeCategoryLabel(mistakeCategory);

  return (
    <main className="px-4 py-10">
      <div className="mx-auto flex max-w-6xl flex-col gap-6">
        <div>
          <p className="text-sm font-medium text-primary">Analytics</p>
          <h1 className="text-3xl font-semibold tracking-tight">
            Track recurring mistakes over time
          </h1>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Filters</CardTitle>
            <CardDescription>
              Choose a date range and a mistake category to inspect analytics.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <AnalyticsFilters
              dateRange={dateRange}
              mistakeCategory={mistakeCategory}
              onDateRangeChange={(value) => {
                setError(null);
                setIsLoading(true);
                setDateRange(value as DateRangeSelection);
              }}
              onMistakeCategoryChange={(value) => {
                setError(null);
                setIsLoading(true);
                setMistakeCategory(value as MistakeCategoryId);
              }}
              dateRanges={[...DATE_RANGES]}
              mistakeCategories={MISTAKE_CATEGORY_OPTIONS}
            />
          </CardContent>
        </Card>

        {error ? <p className="text-sm text-destructive">{error}</p> : null}

        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Distribution</CardTitle>
              <CardDescription>
                Overview for {selectedDateRangeLabel}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {isLoading && !distribution ? (
                <p className="text-sm text-muted-foreground">
                  Loading distribution...
                </p>
              ) : (
                <DistributionPanel distribution={distribution} />
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Time series</CardTitle>
              <CardDescription>
                Trend for {selectedCategoryLabel}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {isLoading && !timeSeries ? (
                <p className="text-sm text-muted-foreground">
                  Loading time series...
                </p>
              ) : (
                <TimeSeriesPanel timeSeries={timeSeries} />
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  );
}
