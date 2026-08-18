import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import type { MistakeCategoryOption } from "@/lib/presentation/mistake-categories";

type AnalyticsFiltersProps = {
  dateRange: string;
  mistakeCategory: string;
  onDateRangeChange: (value: string) => void;
  onMistakeCategoryChange: (value: string) => void;
  dateRanges: Array<{ label: string; value: string }>;
  mistakeCategories: readonly MistakeCategoryOption[];
};

export function AnalyticsFilters({
  dateRange,
  mistakeCategory,
  onDateRangeChange,
  onMistakeCategoryChange,
  dateRanges,
  mistakeCategories,
}: AnalyticsFiltersProps) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      <div className="space-y-2">
        <Label htmlFor="date-range">Date range</Label>
        <Select
          id="date-range"
          value={dateRange}
          onChange={(event) => onDateRangeChange(event.target.value)}
        >
          {dateRanges.map((option) => (
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
          {mistakeCategories.map((option) => (
            <option key={option.id} value={option.id}>
              {option.label}
            </option>
          ))}
        </Select>
      </div>
    </div>
  );
}
