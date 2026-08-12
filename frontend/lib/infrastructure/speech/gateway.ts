import type { SpeechGateway } from "@/lib/application/ports";
import { MistakeCategory } from "@/lib/domain/analysis";
import { Speech } from "@/lib/domain/speech";
import { AuthenticatedApiClient } from "@/lib/infrastructure/api/authenticated-client";

export interface CategoryFrequencyResponse {
  category: MistakeCategory;
  occurances: number;
  opportunities: number;
}

export interface DetectedMistakeResponse {
  category: MistakeCategory;
  original_text: string;
  correction: string;
  explanation: string;
}

export interface SpeechAnalysisResponse {
  frequencies: CategoryFrequencyResponse[];
  mistakes: DetectedMistakeResponse[];
  feedback: string;
}

interface SpeechResponse {
  id: string;
  created_at: string;
  transcript: string;
  analysis: SpeechAnalysisResponse;
}

export const createSpeechGateway = (
  client: AuthenticatedApiClient,
): SpeechGateway => ({
  upload: async (file: File): Promise<Speech> => {
    const formData = new FormData();
    formData.append("file", file);

    const payload = await client.request<SpeechResponse>("/speeches/", {
      method: "POST",
      body: formData,
    });

    return {
      id: payload.id,
      createdAt: payload.created_at,
      transcript: payload.transcript,
      analysis: {
        feedback: payload.analysis.feedback,
        frequencies: payload.analysis.frequencies.map(
          (freq: CategoryFrequencyResponse) => ({
            category: freq.category,
            occurances: freq.occurances,
            opportunities: freq.opportunities,
          }),
        ),
        mistakes: payload.analysis.mistakes.map(
          (mistake: DetectedMistakeResponse) => ({
            category: mistake.category,
            originalText: mistake.original_text,
            correction: mistake.correction,
            explanation: mistake.explanation,
          }),
        ),
      },
    };
  },
});
