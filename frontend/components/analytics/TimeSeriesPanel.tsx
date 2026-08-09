import type { AnalyticsTimeSeries } from "@/lib/application/models";

type TimeSeriesPanelProps = {
  timeSeries: AnalyticsTimeSeries | null;
};

export function TimeSeriesPanel({ timeSeries  }: TimeSeriesPanelProps) {
  if (!timeSeries?.points.length) {
    return <p className="text-sm text-muted-foreground">No time series data available.</p>;
  }

  return (
    <ul className="space-y-2">
      {timeSeries.points.map((point) => (
        <li key={point.time} className="rounded-md border p-3 text-sm">
          <div className="font-medium">{new Date(point.time).toLocaleDateString()}</div>
          <div className="text-muted-foreground">Opportunities: {point.opportunities} • Occurrences: {point.occurances}</div>
        </li>
      ))}
    </ul>
  );
}
