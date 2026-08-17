"use client";

import { useEffect, useState } from "react";

import { useApplication } from "@/app/providers";
import { SpeechTable } from "@/components/speech/SpeechTable";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type { Speech } from "@/lib/domain/speech";

export default function SpeechesPage() {
  const application = useApplication();
  const [speeches, setSpeeches] = useState<Speech[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    application.speeches
      .list()
      .then((items) => {
        if (!cancelled) setSpeeches(items);
      })
      .catch(() => {
        if (!cancelled) setError("Unable to load saved speeches.");
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [application]);

  const deleteSpeech = async (speech: Speech) => {
    if (!window.confirm("Delete this saved speech?")) return;

    setError(null);
    setDeletingId(speech.id);
    try {
      await application.speeches.delete(speech.id);
      setSpeeches((items) => items.filter((item) => item.id !== speech.id));
    } catch {
      setError("Unable to delete the speech.");
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <main className="px-4 py-10">
      <div className="mx-auto flex max-w-6xl flex-col gap-6">
        <div>
          <p className="text-sm font-medium text-primary">Speeches</p>
          <h1 className="text-3xl font-semibold tracking-tight">
            Manage saved speeches
          </h1>
        </div>

        {error ? <p className="text-sm text-destructive">{error}</p> : null}

        <Card>
          <CardHeader>
            <CardTitle>Speech history</CardTitle>
            <CardDescription>
              Review your latest saved transcripts and remove entries you no
              longer need.
            </CardDescription>
          </CardHeader>
          <CardContent className="px-0">
            {isLoading ? (
              <p className="px-6 py-8 text-center text-sm text-muted-foreground">
                Loading speeches...
              </p>
            ) : (
              <SpeechTable
                speeches={speeches}
                deletingId={deletingId}
                onDelete={(speech) => void deleteSpeech(speech)}
              />
            )}
          </CardContent>
        </Card>
      </div>
    </main>
  );
}
