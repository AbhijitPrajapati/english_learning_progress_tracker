import type { MistakeCategoryId } from "@/lib/domain/analysis";
import type { components } from "./generated/schema";

type ApiMistakeCategory = components["schemas"]["MistakeCategory"];

const TO_DOMAIN_CATEGORY = {
  subject_verb_agreement: "subject_verb_agreement",
  verb_tense: "verb_tense",
  article_usage: "article_usage",
  preposition_usage: "preposition_usage",
  word_order: "word_order",
  plurality: "plurality",
} as const satisfies Record<ApiMistakeCategory, MistakeCategoryId>;

export function toDomainMistakeCategory(
  category: ApiMistakeCategory,
): MistakeCategoryId {
  return TO_DOMAIN_CATEGORY[category];
}

export function toApiMistakeCategory(
  category: MistakeCategoryId,
): ApiMistakeCategory {
  return category;
}
