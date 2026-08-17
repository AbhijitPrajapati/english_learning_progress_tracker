import type { components } from "../api/generated/schema";
import type { Speech } from "@/lib/domain/speech";
import { toDomainMistakeCategory } from "../api/mistake-category";
import { toDate } from "../api/scalars";

type SpeechResponse = components["schemas"]["SpeechResponse"];

export function toSpeech(payload: SpeechResponse): Speech {
  return {
    id: payload.id,
    createdAt: toDate(payload.created_at),
    transcript: payload.transcript,
    analysis: {
      feedback: payload.analysis.feedback,
      frequencies: payload.analysis.frequencies.map((frequency) => ({
        category: toDomainMistakeCategory(frequency.category),
        occurrences: frequency.occurrences,
        opportunities: frequency.opportunities,
      })),
      mistakes: payload.analysis.mistakes.map((mistake) => ({
        category: toDomainMistakeCategory(mistake.category),
        originalText: mistake.original_text,
        correction: mistake.correction,
        explanation: mistake.explanation,
      })),
    },
  };
}
