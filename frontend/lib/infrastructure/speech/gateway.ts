import type { SpeechGateway } from "@/lib/application/ports";
import { MistakeCategory } from "@/lib/domain/analysis";
import { Speech } from "@/lib/domain/speech";
import { ApiClient } from "../api/client";
import { ApiError } from "../api/errors";
import { InvalidToken, SpeechNotFound } from "@/lib/application/errors";

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

interface SpeechesResponse {
  speeches: Array<SpeechResponse>;
}

export function createSpeechGateway(client: ApiClient): SpeechGateway {
  return {
    upload: async (file: File, accessToken: string | null): Promise<Speech> => {
      if (!accessToken) {
        throw new InvalidToken();
      }

      const formData = new FormData();
      formData.append("file", file);

      try {
        const payload = await client.request<SpeechResponse>("/speeches/", {
          method: "POST",
          body: formData,
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
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
      } catch (error) {
        if (error instanceof ApiError && error.code == "INVALID_TOKEN") {
          throw new InvalidToken();
        }
        throw error;
      }
    },

    delete: async (
      speech_id: string,
      accessToken: string | null,
    ): Promise<void> => {
      if (!accessToken) {
        throw new InvalidToken();
      }
      const url = `/speeches/${speech_id}/`;
      try {
        await client.request(url, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
      } catch (error) {
        if (error instanceof ApiError) {
          if (error.code == "INVALID_TOKEN") {
            throw new InvalidToken();
          }
          if (error.code == "SPEECH_NOT_FOUND") {
            throw new SpeechNotFound();
          }
        }
        throw error;
      }
    },
    list: async (
      accessToken: string | null,
      limit: number,
      offset: number,
    ): Promise<Array<Speech>> => {
      if (!accessToken) {
        throw new InvalidToken();
      }
      try {
        const payload = await client.request<SpeechesResponse>("/speeches/", {
          method: "GET",
          body: JSON.stringify({
            limit,
            offset,
          }),
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        return payload.speeches.map((speech: SpeechResponse) => ({
          id: speech.id,
          createdAt: speech.created_at,
          transcript: speech.transcript,
          analysis: {
            feedback: speech.analysis.feedback,
            frequencies: speech.analysis.frequencies.map(
              (freq: CategoryFrequencyResponse) => ({
                category: freq.category,
                occurances: freq.occurances,
                opportunities: freq.opportunities,
              }),
            ),
            mistakes: speech.analysis.mistakes.map(
              (mistake: DetectedMistakeResponse) => ({
                category: mistake.category,
                originalText: mistake.original_text,
                correction: mistake.correction,
                explanation: mistake.explanation,
              }),
            ),
          },
        }));
      } catch (error) {
        if (error instanceof ApiError && error.code == "INVALID_TOKEN") {
          throw new InvalidToken();
        }
        throw error;
      }
    },
  };
}
