"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { useApplication } from "@/app/providers";
import { Button } from "@/components/ui/button";

export function DeleteAccountButton() {
  const router = useRouter();
  const application = useApplication();
  const [isDeleting, setIsDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const deleteAccount = async () => {
    if (!window.confirm("Delete your account and all saved speeches?")) return;

    setError(null);
    setIsDeleting(true);
    try {
      await application.account.delete();
      router.replace("/auth");
    } catch {
      setError("Unable to delete your account.");
      setIsDeleting(false);
    }
  };

  return (
    <div className="space-y-3">
      <Button
        variant="destructive"
        disabled={isDeleting}
        onClick={() => void deleteAccount()}
      >
        {isDeleting ? "Deleting account..." : "Delete account"}
      </Button>
      {error ? <p className="text-sm text-destructive">{error}</p> : null}
    </div>
  );
}
