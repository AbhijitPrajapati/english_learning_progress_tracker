"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { useAuth } from "@/app/providers";
import { analyticsApi } from "@/lib/api";

const timeframes = [
  { label: "All time", value: "all_time" },
  { label: "Yearly", value: "yearly" },
  { label: "Monthly", value: "monthly" },
  { label: "Weekly", value: "weekly" },
] as const;

function getTimeframeRange(selected: (typeof timeframes)[number]["value"]) {
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

const mistakeCategories = [
  { label: "Test abc error", value: "test abc error" },
  { label: "Test def error", value: "test def error" },
] as const;

export default function AnalyticsPage() {
  const router = useRouter();
  const { token, logout } = useAuth();
  const [timeframe, setTimeframe] = useState<(typeof timeframes)[number]["value"]>("all_time");
  const [mistakeCategory, setMistakeCategory] = useState<(typeof mistakeCategories)[number]["value"]>("test abc error");
  const [distribution, setDistribution] = useState<Awaited<ReturnType<typeof analyticsApi.getDistribution>> | null>(null);
  const [timeSeries, setTimeSeries] = useState<Awaited<ReturnType<typeof analyticsApi.getTimeSeries>> | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      router.replace("/auth");
      return;
    }

    void loadAnalytics();
  }, [router, token]);

  const loadAnalytics = async (selectedTimeframe = timeframe) => {
    setIsLoading(true);
    setError(null);

    try {
      const { start, end } = getTimeframeRange(selectedTimeframe);
      const [nextDistribution, nextTimeSeries] = await Promise.all([
        analyticsApi.getDistribution({ start, end }),
        analyticsApi.getTimeSeries({ start, end }, mistakeCategory),
      ]);
      setDistribution(nextDistribution);
      setTimeSeries(nextTimeSeries);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load analytics.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (!token) {
      return;
    }

    void loadAnalytics(timeframe);
  }, [mistakeCategory, token, timeframe]);

  const selectedTimeframeLabel = useMemo(() => timeframes.find((option) => option.value === timeframe)?.label ?? "All time", [timeframe]);

  if (!token) {
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
          <CardContent className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="timeframe">Timeframe</Label>
              <Select id="timeframe" value={timeframe} onChange={(event) => setTimeframe(event.target.value as (typeof timeframes)[number]["value"])}>
                {timeframes.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="mistake-category">Mistake category</Label>
              <Select id="mistake-category" value={mistakeCategory} onChange={(event) => setMistakeCategory(event.target.value as (typeof mistakeCategories)[number]["value"])}>
                {mistakeCategories.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </Select>
            </div>
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
              ) : distribution ? (
                <div className="space-y-3">
                  <div className="text-sm text-muted-foreground">Total samples: {distribution.total_samples}</div>
                  <ul className="space-y-2">
                    {distribution.mistake_frequencies.map((item) => (
                      <li key={item.category} className="flex items-center justify-between rounded-md border p-3 text-sm">
                        <span>{item.category}</span>
                        <span className="font-medium">{item.occurances}/{item.opportunities}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">No distribution available.</p>
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
              ) : timeSeries?.points.length ? (
                <ul className="space-y-2">
                  {timeSeries.points.map((point) => (
                    <li key={point.time} className="rounded-md border p-3 text-sm">
                      <div className="font-medium">{new Date(point.time).toLocaleDateString()}</div>
                      <div className="text-muted-foreground">Opportunities: {point.opportunities} • Occurrences: {point.occurances}</div>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-muted-foreground">No time series data available.</p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  );
}
