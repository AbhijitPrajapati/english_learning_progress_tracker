import type { AudioSample } from "@/lib/application/models";
import type { SpeechGateway } from "@/lib/application/ports";
import type { Speech } from "@/lib/domain/speech";
import type { ApiWireClient } from "../api/wire-client";
import { requireData, requireNoContent } from "../api/response";
import { toSpeech } from "./mapper";

export default class HttpSpeechGateway implements SpeechGateway {
  constructor(private readonly client: ApiWireClient) {}

  async upload(audio: AudioSample): Promise<Speech> {
    const file = new Blob([audio.content], { type: audio.mediaType });
    const payload = await requireData(
      this.client.POST("/api/v1/speeches", {
        body: { file },
        bodySerializer(body) {
          const form = new FormData();
          form.append("file", body.file, audio.filename);
          return form;
        },
      }),
    );
    return toSpeech(payload);
  }

  async delete(speechId: string): Promise<void> {
    await requireNoContent(
      this.client.DELETE("/api/v1/speeches/{speech_id}", {
        params: { path: { speech_id: speechId } },
      }),
    );
  }

  async list(limit: number, offset: number): Promise<Speech[]> {
    const payload = await requireData(
      this.client.GET("/api/v1/speeches", {
        params: { query: { limit, offset } },
      }),
    );
    return payload.speeches.map(toSpeech);
  }
}
