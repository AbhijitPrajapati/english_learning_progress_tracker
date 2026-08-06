"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/app/providers";
import { speechApi } from "@/lib/api";

export default function HomePage() {
  const router = useRouter();
  const { token, logout } = useAuth();
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [result, setResult] = useState<Awaited<ReturnType<typeof speechApi.upload>> | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      router.replace("/auth");
    }
  }, [router, token]);

  const fileName = useMemo(() => file?.name ?? "No file selected", [file]);

  async function handleUpload(event: React.FormEvent) {
    event.preventDefault();
    if (!file) {
      setError("Please select an audio file first.");
      return;
    }

    setError(null);
    setIsUploading(true);

    try {
      const response = await speechApi.upload(file);
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed.");
    } finally {
      setIsUploading(false);
    }
  }

  if (!token) {
    return null;
  }

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-10">
      <div className="mx-auto flex max-w-6xl flex-col gap-6">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="text-sm font-medium text-primary">English learning tracker</p>
            <h1 className="text-3xl font-semibold tracking-tight">Upload a speech sample</h1>
          </div>
          <div className="flex items-center gap-2">
            <Link href="/analytics">
              <Button variant="outline">Analytics</Button>
            </Link>
            <Button variant="secondary" onClick={logout}>Logout</Button>
          </div>
        </div>

        <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <Card>
            <CardHeader>
              <CardTitle>Upload audio</CardTitle>
              <CardDescription>Send a short audio clip to the backend for transcription and grammar analysis.</CardDescription>
            </CardHeader>
            <CardContent>
              <form className="space-y-4" onSubmit={handleUpload}>
                <div className="space-y-2">
                  <Label htmlFor="audio-file">Audio clip</Label>
                  <Input id="audio-file" type="file" accept="audio/*" onChange={(event) => setFile(event.target.files?.[0] ?? null)} />
                  <p className="text-sm text-muted-foreground">Selected file: {fileName}</p>
                </div>
                {error ? <p className="text-sm text-destructive">{error}</p> : null}
                <Button type="submit" disabled={isUploading}>
                  {isUploading ? "Processing..." : "Upload and analyze"}
                </Button>
              </form>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Latest result</CardTitle>
              <CardDescription>Feedback and detected mistakes returned by the speech endpoint.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {!result ? (
                <p className="text-sm text-muted-foreground">No speech has been processed yet.</p>
              ) : (
                <>
                  <div>
                    <p className="text-sm font-medium">Transcript</p>
                    <p className="text-sm text-muted-foreground">{result.transcript}</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium">Feedback</p>
                    <p className="text-sm text-muted-foreground">{result.analysis.feedback}</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium">Detected mistakes</p>
                    <ul className="mt-2 space-y-2 text-sm text-muted-foreground">
                      {result.analysis.mistakes.map((mistake, index) => (
                        <li key={`${mistake.category}-${index}`} className="rounded-md border p-3">
                          <p className="font-medium text-foreground">{mistake.category}</p>
                          <p>Original: {mistake.original_text}</p>
                          <p>Correction: {mistake.correction}</p>
                          <p>Explanation: {mistake.explanation}</p>
                        </li>
                      ))}
                    </ul>
                  </div>
                </>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  );
}
