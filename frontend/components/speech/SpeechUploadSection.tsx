import type { SubmitEventHandler } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

type SpeechUploadSectionProps = {
  fileName: string;
  file: File | null;
  isUploading: boolean;
  error: string | null;
  onFileChange: (file: File | null) => void;
  onSubmit: SubmitEventHandler;
};

export function SpeechUploadSection({
  fileName,
  file,
  isUploading,
  error,
  onFileChange,
  onSubmit,
}: SpeechUploadSectionProps) {
  return (
    <form className="space-y-4" onSubmit={onSubmit}>
      <div className="space-y-2">
        <Label htmlFor="audio-file">Audio clip</Label>
        <Input
          id="audio-file"
          type="file"
          accept="audio/*"
          onChange={(event) => onFileChange(event.target.files?.[0] ?? null)}
        />
        <p className="text-sm text-muted-foreground">
          Selected file: {fileName}
        </p>
      </div>
      {error ? <p className="text-sm text-destructive">{error}</p> : null}
      <Button type="submit" disabled={isUploading || !file}>
        {isUploading ? "Processing..." : "Upload and analyze"}
      </Button>
    </form>
  );
}
