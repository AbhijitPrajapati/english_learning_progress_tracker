import type { SpeechGateway } from "@/lib/application/ports";
import { Speech } from "@/lib/domain/speech";
import { ApiError } from "../api/errors";
import { InvalidToken, SpeechNotFound } from "@/lib/application/errors";
import { components } from "../openapi-schema";
import AuthenticatedApiClient from "../api/authenticated-client";

type DetectedMistakeResponse = components["schemas"]["DetectedMistake"];
type SpeechResponse = components["schemas"]["SpeechResponse"];
type SpeechesResponse = components["schemas"]["SpeechListResponse"];

export default class HttpSpeechGateway implements SpeechGateway {
  constructor(private readonly client: AuthenticatedApiClient) {}

  async upload(file: File, accessToken: string | null): Promise<Speech> {
    if (!accessToken) {
      throw new InvalidToken();
    }

    const formData = new FormData();
    formData.append("file", file);

    const payload = await this.client.request<SpeechResponse>("/speeches/", {
      method: "POST",
      body: formData,
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    return {
      id: payload.speech_id,
      createdAt: payload.created_at,
      transcript: payload.transcript,
      analysis: {
        feedback: payload.analysis.feedback,
        frequencies: payload.analysis.frequencies,
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
  }

  async delete(speech_id: string, accessToken: string | null): Promise<void> {
    if (!accessToken) {
      throw new InvalidToken();
    }
    const url = `/speeches/${speech_id}/`;
    try {
      await this.client.request(url, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
    } catch (error) {
      if (error instanceof ApiError && error.code == "SPEECH_NOT_FOUND") {
        throw new SpeechNotFound();
      }
      throw error;
    }
  }

  async list(
    accessToken: string | null,
    limit: number,
    offset: number,
  ): Promise<Array<Speech>> {
    if (!accessToken) {
      throw new InvalidToken();
    }
    const payload = await this.client.request<SpeechesResponse>("/speeches/", {
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
      id: speech.speech_id,
      createdAt: speech.created_at,
      transcript: speech.transcript,
      analysis: {
        feedback: speech.analysis.feedback,
        frequencies: speech.analysis.frequencies,
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
  }
}
