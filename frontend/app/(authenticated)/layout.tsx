"use client";

import { useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { useApplication, useAuth } from "@/app/providers";
import { Button, buttonVariants } from "@/components/ui/button";

const navigation = [
  { href: "/", label: "Upload" },
  { href: "/speeches", label: "Speeches" },
  { href: "/analytics", label: "Analytics" },
  { href: "/account", label: "Account" },
] as const;

export default function AuthenticatedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const application = useApplication();
  const { isAuthenticated, isRestoring } = useAuth();

  useEffect(() => {
    if (!isRestoring && !isAuthenticated) router.replace("/auth");
  }, [isAuthenticated, isRestoring, router]);

  if (isRestoring || !isAuthenticated) return null;

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-3 px-4 py-4">
          <Link href="/" className="font-semibold tracking-tight">
            English learning tracker
          </Link>
          <nav
            className="flex flex-wrap items-center gap-2"
            aria-label="Main navigation"
          >
            {navigation.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={buttonVariants({ variant: "ghost", size: "sm" })}
              >
                {item.label}
              </Link>
            ))}
            <Button
              variant="secondary"
              size="sm"
              onClick={() => void application.auth.logout()}
            >
              Logout
            </Button>
          </nav>
        </div>
      </header>
      {children}
    </div>
  );
}
