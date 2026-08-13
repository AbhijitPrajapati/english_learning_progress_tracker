"use client";

import { useState } from "react";
import type { SubmitEventHandler } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useUseCases } from "@/app/providers";
import { AuthForm } from "@/components/auth/AuthForm";
import { AuthCredentials } from "@/lib/application/models";
import { ApplicationError } from "@/lib/application/errors";

export default function AuthPage() {
  const router = useRouter();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { register, login } = useUseCases();

  const handleSubmit: SubmitEventHandler = async (event) => {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);

    const credentials: AuthCredentials = { email, password };

    try {
      if (mode === "register") {
        await register(credentials);
      }
      await login(credentials);
      router.push("/");
    } catch (err) {
      if (err instanceof ApplicationError) {
        setError(err.message);
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-50 px-4 py-10">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Welcome back</CardTitle>
          <CardDescription>
            Use your email and password to sign in or create an account.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <AuthForm
            mode={mode}
            email={email}
            password={password}
            error={error}
            isSubmitting={isSubmitting}
            onEmailChange={setEmail}
            onPasswordChange={setPassword}
            onToggleMode={() =>
              setMode(mode === "login" ? "register" : "login")
            }
            onSubmit={handleSubmit}
          />
          <div className="mt-4 flex items-center justify-between text-sm text-muted-foreground">
            <Link className="font-medium text-primary" href="/">
              Skip for now
            </Link>
          </div>
        </CardContent>
      </Card>
    </main>
  );
}
