import { describe, expect, it, vi } from "vitest";

import type { components } from "./api/generated/schema";
import HttpAccountGateway from "./account/gateway";
import {
  toDistribution,
  toTimeSeries,
  toWireDateRange,
} from "./analytics/mapper";
import { toSpeech } from "./speech/mapper";
import { ApiContractError } from "./api/errors";
import { toDate } from "./api/scalars";
import type { ApiWireClient } from "./api/wire-client";

describe("HTTP anti-corruption mappers", () => {
  it("maps snake_case speech documents and temporal values explicitly", () => {
    const payload: components["schemas"]["SpeechResponse"] = {
      id: "speech-1",
      created_at: "2026-08-17T12:30:00Z",
      transcript: "A sample",
      analysis: {
        feedback: "Keep practicing.",
        frequencies: [
          {
            category: "article_usage",
            occurrences: 1,
            opportunities: 3,
          },
        ],
        mistakes: [
          {
            category: "article_usage",
            original_text: "a apple",
            correction: "an apple",
            explanation: "Use an before a vowel sound.",
          },
        ],
      },
    };

    const speech = toSpeech(payload);

    expect(speech.createdAt).toEqual(new Date("2026-08-17T12:30:00Z"));
    expect(speech.analysis.mistakes[0].originalText).toBe("a apple");
    expect(speech.analysis.frequencies[0].occurrences).toBe(1);
  });

  it("maps analytics dates only at the HTTP boundary", () => {
    expect(
      toWireDateRange({
        start: new Date("2026-08-01T00:00:00Z"),
        end: null,
      }),
    ).toEqual({ start: "2026-08-01T00:00:00.000Z", end: null });

    expect(
      toDistribution({
        total_speeches: 2,
        mistake_frequencies: [
          {
            category: "verb_tense",
            occurrences: 1,
            opportunities: 4,
          },
        ],
      }).totalSpeeches,
    ).toBe(2);

    const series = toTimeSeries({
      points: [
        {
          time: "2026-08-17T00:00:00Z",
          occurrences: 1,
          opportunities: 5,
        },
      ],
    });
    expect(series.points[0].time).toBeInstanceOf(Date);
  });

  it("rejects invalid temporal wire values at the infrastructure boundary", () => {
    expect(() => toDate("not-a-date")).toThrow(ApiContractError);
  });

  it("maps password changes to the API naming convention", async () => {
    const patch = vi.fn(async () => ({
      response: new Response(null, { status: 204 }),
    }));
    const gateway = new HttpAccountGateway({
      PATCH: patch,
    } as unknown as ApiWireClient);

    await gateway.changePassword({
      currentPassword: "old-password",
      newPassword: "new-password",
    });

    expect(patch).toHaveBeenCalledWith("/api/v1/account/password", {
      body: {
        current_password: "old-password",
        new_password: "new-password",
      },
    });
  });
});
