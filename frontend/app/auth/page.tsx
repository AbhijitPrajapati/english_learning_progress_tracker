"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { authApi } from "@/lib/api";
import { useAuth } from "@/app/providers";

export default function AuthPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      if (mode === "login") {
        const response = await authApi.login({ email, password });
        login(response.access_token, response.user_id);
      } else {
        await authApi.register({ email, password });
        const response = await authApi.login({ email, password });
        login(response.access_token, response.user_id);
      }

      router.push("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Authentication failed");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-50 px-4 py-10">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Welcome back</CardTitle>
          <CardDescription>Use your email and password to sign in or create an account.</CardDescription>
        </CardHeader>
        <CardContent>
          <form className="space-y-4" onSubmit={handleSubmit}>
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input id="password" type="password" value={password} onChange={(event) => setPassword(event.target.value)} required />
            </div>
            {error ? <p className="text-sm text-destructive">{error}</p> : null}
            <Button className="w-full" type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Please wait..." : mode === "login" ? "Sign in" : "Create account"}
            </Button>
          </form>
          <div className="mt-4 flex items-center justify-between text-sm text-muted-foreground">
            <button type="button" className="font-medium text-primary" onClick={() => setMode(mode === "login" ? "register" : "login")}>
              {mode === "login" ? "Need an account?" : "Already have an account?"}
            </button>
            <Link className="font-medium text-primary" href="/">
              Skip for now
            </Link>
          </div>
        </CardContent>
      </Card>
    </main>
  );
}
