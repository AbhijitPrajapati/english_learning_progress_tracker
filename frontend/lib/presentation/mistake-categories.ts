import type { MistakeCategoryId } from "@/lib/domain/analysis";

export interface MistakeCategoryOption {
  id: MistakeCategoryId;
  label: string;
}

export const MISTAKE_CATEGORY_OPTIONS = [
  { id: "subject_verb_agreement", label: "Subject-verb agreement" },
  { id: "verb_tense", label: "Verb tense" },
  { id: "article_usage", label: "Article usage" },
  { id: "preposition_usage", label: "Preposition usage" },
  { id: "word_order", label: "Word order" },
  { id: "plurality", label: "Plurality" },
] as const satisfies readonly MistakeCategoryOption[];

export function mistakeCategoryLabel(categoryId: MistakeCategoryId): string {
  return (
    MISTAKE_CATEGORY_OPTIONS.find((option) => option.id === categoryId)
      ?.label ?? categoryId
  );
}
