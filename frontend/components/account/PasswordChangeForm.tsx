"use client";

import { useState } from "react";
import type { SubmitEventHandler } from "react";

import { useApplication } from "@/app/providers";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ApplicationError } from "@/lib/application/errors";

export function PasswordChangeForm() {
  const application = useApplication();
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmation, setConfirmation] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit: SubmitEventHandler = async (event) => {
    event.preventDefault();
    setMessage(null);
    setError(null);

    if (newPassword !== confirmation) {
      setError("New passwords do not match.");
      return;
    }

    setIsSubmitting(true);
    try {
      await application.account.changePassword({
        currentPassword,
        newPassword,
      });
      setCurrentPassword("");
      setNewPassword("");
      setConfirmation("");
      setMessage("Password changed.");
    } catch (caught) {
      setError(
        caught instanceof ApplicationError
          ? caught.message
          : "Unable to change your password.",
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form className="space-y-4" onSubmit={handleSubmit}>
      <div className="space-y-2">
        <Label htmlFor="current-password">Current password</Label>
        <Input
          id="current-password"
          type="password"
          autoComplete="current-password"
          minLength={8}
          maxLength={128}
          required
          value={currentPassword}
          onChange={(event) => setCurrentPassword(event.target.value)}
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="new-password">New password</Label>
        <Input
          id="new-password"
          type="password"
          autoComplete="new-password"
          minLength={8}
          maxLength={128}
          required
          value={newPassword}
          onChange={(event) => setNewPassword(event.target.value)}
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="confirm-password">Confirm new password</Label>
        <Input
          id="confirm-password"
          type="password"
          autoComplete="new-password"
          minLength={8}
          maxLength={128}
          required
          value={confirmation}
          onChange={(event) => setConfirmation(event.target.value)}
        />
      </div>
      {error ? <p className="text-sm text-destructive">{error}</p> : null}
      {message ? <p className="text-sm text-emerald-700">{message}</p> : null}
      <Button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Changing password..." : "Change password"}
      </Button>
    </form>
  );
}
