"use client";

import { useEffect, useMemo, useState } from "react";
import type { SubmitEventHandler } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useAuth, useDependencies } from "@/app/providers";
import { SpeechUploadSection } from "@/components/speech/SpeechUploadSection";
import { SpeechResultCard } from "@/components/speech/SpeechResultCard";
import type { Speech } from "@/lib/domain/speech";

export default function HomePage() {
  const router = useRouter();
  const { session, logout } = useAuth();
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [result, setResult] = useState<Speech | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { uploadSpeech } = useDependencies();

  useEffect(() => {
    if (!session) {
      router.replace("/auth");
    }
  }, [router, session]);

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
      const response = await uploadSpeech(file);
      setResult(response);
    } catch {
      setError("Upload failed");
    } finally {
      setIsUploading(false);
    }
  };

  if (!session) {
    return null;
  }

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-10">
      <div className="mx-auto flex max-w-6xl flex-col gap-6">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="text-sm font-medium text-primary">
              English learning tracker
            </p>
            <h1 className="text-3xl font-semibold tracking-tight">
              Upload a speech sample
            </h1>
          </div>
          <div className="flex items-center gap-2">
            <Link href="/analytics">
              <Button variant="outline">Analytics</Button>
            </Link>
            <Button variant="secondary" onClick={logout}>
              Logout
            </Button>
          </div>
        </div>

        <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <Card>
            <CardHeader>
              <CardTitle>Upload audio</CardTitle>
              <CardDescription>
                Send a short audio clip to the backend for transcription and
                grammar analysis.
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
                Feedback and detected mistakes returned by the speech endpoint.
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
