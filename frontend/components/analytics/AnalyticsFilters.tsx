import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { MISTAKE_CATEGORIES } from "@/lib/domain/analysis";

type AnalyticsFiltersProps = {
  timeframe: string;
  mistakeCategory: string;
  onTimeframeChange: (value: string) => void;
  onMistakeCategoryChange: (value: string) => void;
  timeframes: Array<{ label: string; value: string }>;
};

export function AnalyticsFilters({
  timeframe,
  mistakeCategory,
  onTimeframeChange,
  onMistakeCategoryChange,
  timeframes,
}: AnalyticsFiltersProps) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      <div className="space-y-2">
        <Label htmlFor="timeframe">Timeframe</Label>
        <Select
          id="timeframe"
          value={timeframe}
          onChange={(event) => onTimeframeChange(event.target.value)}
        >
          {timeframes.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </Select>
      </div>
      <div className="space-y-2">
        <Label htmlFor="mistake-category">Mistake category</Label>
        <Select
          id="mistake-category"
          value={mistakeCategory}
          onChange={(event) => onMistakeCategoryChange(event.target.value)}
        >
          {MISTAKE_CATEGORIES.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </Select>
      </div>
    </div>
  );
}
