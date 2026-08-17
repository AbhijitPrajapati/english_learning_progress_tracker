import { SpeechAnalysis } from "./analysis";

export interface Speech {
  id: string;
  createdAt: Date;
  transcript: string;
  analysis: SpeechAnalysis;
}
