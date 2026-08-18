import type { AnalyticsDistribution } from "@/lib/application/models";
import { errorRate, MISTAKE_CATEGORY_IDS } from "@/lib/domain/analysis";
import { mistakeCategoryLabel } from "@/lib/presentation/mistake-categories";

type DistributionPanelProps = {
  distribution: AnalyticsDistribution | null;
};

export function DistributionPanel({ distribution }: DistributionPanelProps) {
  if (!distribution) {
    return (
      <p className="text-sm text-muted-foreground">
        No distribution available.
      </p>
    );
  }

  const frequenciesByCategory = new Map(
    distribution.mistakeFrequencies.map((frequency) => [
      frequency.category,
      frequency,
    ]),
  );
  const frequencies = MISTAKE_CATEGORY_IDS.map(
    (category) =>
      frequenciesByCategory.get(category) ?? {
        category,
        occurrences: 0,
        opportunities: 0,
      },
  );

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between gap-4 text-sm text-muted-foreground">
        <span>Total speeches: {distribution.totalSpeeches}</span>
        <span>Occurrences ÷ opportunities</span>
      </div>

      <div className="space-y-4" aria-label="Error rate by mistake category">
        {frequencies.map((item) => (
          <DistributionBar key={item.category} frequency={item} />
        ))}
      </div>

      <div
        className="grid grid-cols-5 text-xs text-muted-foreground"
        aria-hidden
      >
        <span>0%</span>
        <span className="text-center">25%</span>
        <span className="text-center">50%</span>
        <span className="text-center">75%</span>
        <span className="text-right">100%</span>
      </div>
    </div>
  );
}

type DistributionBarProps = {
  frequency: AnalyticsDistribution["mistakeFrequencies"][number];
};

function DistributionBar({ frequency }: DistributionBarProps) {
  const rate = errorRate(frequency);
  const percentage = Math.round(rate * 1000) / 10;

  return (
    <div className="space-y-1.5">
      <div className="flex items-baseline justify-between gap-3 text-sm">
        <span className="font-medium">
          {mistakeCategoryLabel(frequency.category)}
        </span>
        <span className="whitespace-nowrap text-muted-foreground tabular-nums">
          {percentage}% · {frequency.occurrences}/{frequency.opportunities}
        </span>
      </div>
      <div
        className="h-3 overflow-hidden rounded-full bg-muted"
        role="meter"
        aria-label={`${mistakeCategoryLabel(frequency.category)} error rate`}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={percentage}
        aria-valuetext={`${percentage}%`}
      >
        <div
          className="h-full rounded-full bg-primary transition-[width] duration-500"
          style={{
            width: `${Math.min(percentage, 100)}%`,
            minWidth: percentage && percentage > 0 ? "2px" : undefined,
          }}
        />
      </div>
    </div>
  );
}
