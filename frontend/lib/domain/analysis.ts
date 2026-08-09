export const MISTAKE_CATEGORIES = [
  { value: "test_abc_error", label: "test abc error" },
  { value: "test_def_error", label: "test def error" },
] as const

export type MistakeCategory = (typeof MISTAKE_CATEGORIES)[number]["value"]

export interface Frequency {
    occurances: number;
    opportunities: number;
}

export interface CategoryFrequency extends Frequency {
    category: MistakeCategory;
}

export interface DetectedMistake {
  category: string;
  originalText: string;
  correction: string;
  explanation: string;
}

export interface SpeechAnalysis {
  frequencies: CategoryFrequency[];
  mistakes: DetectedMistake[];
  feedback: string;
}