import { SpeechAnalysis } from "./analysis";

export interface Speech {
  id: string;
  createdAt: string;
  transcript: string;
  analysis: SpeechAnalysis;
}
