"use client";

import { useMemo, useState } from "react";
import type { SubmitEventHandler } from "react";

import { useApplication } from "@/app/providers";
import { SpeechResultCard } from "@/components/speech/SpeechResultCard";
import { SpeechUploadSection } from "@/components/speech/SpeechUploadSection";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type { Speech } from "@/lib/domain/speech";
import { QuotaReached } from "@/lib/application/errors";

export default function HomePage() {
  const application = useApplication();
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [result, setResult] = useState<Speech | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fileName = useMemo(() => file?.name ?? "No file selected", [file]);

  const handleUpload: SubmitEventHandler = async (event) => {
    event.preventDefault();
    if (!file) {
      setError("Please select an audio file first.");
      return;
    }

    setError(null);
    setIsUploading(true);
    try {
      const response = await application.speeches.upload({
        content: await file.arrayBuffer(),
        filename: file.name,
        mediaType: file.type || "audio/mpeg",
      });
      setResult(response);
    } catch (error) {
      if (error instanceof QuotaReached) {
        setError("Analysis quota reached");
      } else {
        setError("Upload failed");
      }
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <main className="px-4 py-10">
      <div className="mx-auto flex max-w-6xl flex-col gap-6">
        <div>
          <p className="text-sm font-medium text-primary">Speech analysis</p>
          <h1 className="text-3xl font-semibold tracking-tight">
            Upload a speech sample
          </h1>
        </div>

        <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <Card>
            <CardHeader>
              <CardTitle>Upload audio</CardTitle>
              <CardDescription>
                Send a short audio clip for transcription and grammar analysis.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <SpeechUploadSection
                fileName={fileName}
                file={file}
                isUploading={isUploading}
                error={error}
                onFileChange={setFile}
                onSubmit={handleUpload}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Latest result</CardTitle>
              <CardDescription>
                Feedback and detected mistakes from your upload.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <SpeechResultCard speech={result} />
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  );
}
