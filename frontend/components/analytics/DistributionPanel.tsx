import type { AnalyticsDistribution } from "@/lib/application/models";

type DistributionPanelProps = {
  distribution: AnalyticsDistribution | null;
};

export function DistributionPanel({ distribution }: DistributionPanelProps) {
  if (!distribution) {
    return <p className="text-sm text-muted-foreground">No distribution available.</p>;
  }

  return (
    <div className="space-y-3">
      <div className="text-sm text-muted-foreground">Total samples: {distribution.totalSamples}</div>
      <ul className="space-y-2">
        {distribution.mistakeFrequencies.map((item) => (
          <li key={item.category} className="flex items-center justify-between rounded-md border p-3 text-sm">
            <span>{item.category}</span>
            <span className="font-medium">{item.occurances}/{item.opportunities}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
