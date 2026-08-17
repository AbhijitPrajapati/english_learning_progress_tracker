import type { AnalyticsTimeSeries } from "@/lib/application/models";

type TimeSeriesPanelProps = {
  timeSeries: AnalyticsTimeSeries | null;
};

export function TimeSeriesPanel({ timeSeries }: TimeSeriesPanelProps) {
  if (!timeSeries?.points.length) {
    return (
      <p className="text-sm text-muted-foreground">
        No time series data available.
      </p>
    );
  }

  return (
    <ul className="space-y-2">
      {timeSeries.points.map((point) => (
        <li
          key={point.time.toISOString()}
          className="rounded-md border p-3 text-sm"
        >
          <div className="font-medium">{point.time.toLocaleDateString()}</div>
          <div className="text-muted-foreground">
            Opportunities: {point.opportunities} • Occurrences:{" "}
            {point.occurrences}
          </div>
        </li>
      ))}
    </ul>
  );
}
