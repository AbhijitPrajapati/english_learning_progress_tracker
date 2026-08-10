"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/app/providers";
import { AnalyticsFilters } from "@/components/analytics/AnalyticsFilters";
import { DistributionPanel } from "@/components/analytics/DistributionPanel";
import { TimeSeriesPanel } from "@/components/analytics/TimeSeriesPanel";
import { MistakeCategory } from "@/lib/domain/analysis";
import { AnalyticsDistribution, AnalyticsTimeSeries, Timeframe } from "@/lib/application/models";
import { getDistribution, getTimeSeries } from "@/lib/services";

const TIMEFRAMES = [
  { value: "all_time", label: "All Time" },
  { value: "yearly", label: "Yearly" },
  { value: "monthly", label: "Monthly" },
  { value: "weekly", label: "Weekly" },
]
type TimeframeSelection = (typeof TIMEFRAMES)[number]["value"]

function getTimeframe(selected: TimeframeSelection): Timeframe {
  const end = new Date();
  const start = new Date(end);

  if (selected === "weekly") {
    start.setDate(end.getDate() - 7);
  } else if (selected === "monthly") {
    start.setMonth(end.getMonth() - 1);
  } else if (selected === "yearly") {
    start.setFullYear(end.getFullYear() - 1);
  } else {
    start.setFullYear(1970);
  }

  return {
    start: start.toISOString(),
    end: end.toISOString(),
  };
}

export default function AnalyticsPage() {
  const router = useRouter();
  const { isAuthenticated, logout } = useAuth();
  const [timeframe, setTimeframe] = useState<TimeframeSelection>("monthly");
  const [mistakeCategory, setMistakeCategory] = useState<MistakeCategory>("test_abc_error");
  const [distribution, setDistribution] = useState<AnalyticsDistribution | null>(null);
  const [timeSeries, setTimeSeries] = useState<AnalyticsTimeSeries | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace("/auth");
    }
  }, [router, isAuthenticated]);
  
  useEffect(() => {
    if (!isAuthenticated) return

    const loadTimeSeries = async () => {
      setIsLoading(true);
      setError(null);

      try {
        const timerange = getTimeframe(timeframe);
        const timeseries = await getTimeSeries(timerange, mistakeCategory);
        setTimeSeries(timeseries);
      } catch {
        setError("Unable to load time series.")
      } finally {
        setIsLoading(false);
      }
    }

    loadTimeSeries();
  }
  )

  useEffect(() => {
    if (!isAuthenticated) return

    const loadDistribution = async () => {
      setIsLoading(true);
      setError(null);

      try {
        const timerange = getTimeframe(timeframe);
        const distribution = await getDistribution(timerange);
        setDistribution(distribution);
      } catch {
        setError("Unable to load distribution.")
      } finally {
        setIsLoading(false);
      }
    }

    loadDistribution();
  })

  const selectedTimeframeLabel = useMemo(() => TIMEFRAMES.find((option) => option.value === timeframe)?.label ?? "All time", [timeframe]);

  if (!isAuthenticated) {
    return null;
  }

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-10">
      <div className="mx-auto flex max-w-6xl flex-col gap-6">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="text-sm font-medium text-primary">Analytics</p>
            <h1 className="text-3xl font-semibold tracking-tight">Track recurring mistakes over time</h1>
          </div>
          <div className="flex items-center gap-2">
            <Link href="/">
              <Button variant="outline">Home</Button>
            </Link>
            <Button variant="secondary" onClick={logout}>Logout</Button>
          </div>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Filters</CardTitle>
            <CardDescription>Choose a timeframe and a mistake category to inspect analytics.</CardDescription>
          </CardHeader>
          <CardContent>
            <AnalyticsFilters
              timeframe={timeframe}
              mistakeCategory={mistakeCategory}
              onTimeframeChange={(value) => setTimeframe(value as TimeframeSelection)}
              onMistakeCategoryChange={(value) => setMistakeCategory(value as MistakeCategory)}
              timeframes={TIMEFRAMES}
            />
          </CardContent>
        </Card>

        {error ? <p className="text-sm text-destructive">{error}</p> : null}

        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Distribution</CardTitle>
              <CardDescription>Overview for {selectedTimeframeLabel}</CardDescription>
            </CardHeader>
            <CardContent>
              {isLoading && !distribution ? (
                <p className="text-sm text-muted-foreground">Loading distribution…</p>
              ) : (
                <DistributionPanel distribution={distribution} />
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Time series</CardTitle>
              <CardDescription>Trend for {mistakeCategory}</CardDescription>
            </CardHeader>
            <CardContent>
              {isLoading && !timeSeries ? (
                <p className="text-sm text-muted-foreground">Loading time series…</p>
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
