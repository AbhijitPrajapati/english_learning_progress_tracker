export const MISTAKE_CATEGORY_IDS = [
  "subject_verb_agreement",
  "verb_tense",
  "article_usage",
  "preposition_usage",
  "word_order",
  "plurality",
] as const;

export type MistakeCategoryId = (typeof MISTAKE_CATEGORY_IDS)[number];

export interface Frequency {
  occurrences: number;
  opportunities: number;
}

export interface CategoryFrequency extends Frequency {
  category: MistakeCategoryId;
}

export interface DetectedMistake {
  category: MistakeCategoryId;
  originalText: string;
  correction: string;
  explanation: string;
}

export interface SpeechAnalysis {
  frequencies: CategoryFrequency[];
  mistakes: DetectedMistake[];
  feedback: string;
}
