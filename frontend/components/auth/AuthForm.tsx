import type { SubmitEventHandler } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

type AuthFormProps = {
  mode: "login" | "register";
  email: string;
  password: string;
  error: string | null;
  isSubmitting: boolean;
  onEmailChange: (email: string) => void;
  onPasswordChange: (password: string) => void;
  onToggleMode: () => void;
  onSubmit: SubmitEventHandler;
};

export function AuthForm({
  mode,
  email,
  password,
  error,
  isSubmitting,
  onEmailChange,
  onPasswordChange,
  onToggleMode,
  onSubmit,
}: AuthFormProps) {
  return (
    <form className="space-y-4" onSubmit={onSubmit}>
      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          value={email}
          onChange={(event) => onEmailChange(event.target.value)}
          required
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="password">Password</Label>
        <Input
          id="password"
          type="password"
          value={password}
          onChange={(event) => onPasswordChange(event.target.value)}
          required
        />
      </div>
      {error ? <p className="text-sm text-destructive">{error}</p> : null}
      <Button className="w-full" type="submit" disabled={isSubmitting}>
        {isSubmitting
          ? "Please wait..."
          : mode === "login"
            ? "Sign in"
            : "Create account"}
      </Button>
      <div className="flex items-center justify-between text-sm text-muted-foreground">
        <button
          type="button"
          className="font-medium text-primary"
          onClick={onToggleMode}
        >
          {mode === "login" ? "Need an account?" : "Already have an account?"}
        </button>
      </div>
    </form>
  );
}
