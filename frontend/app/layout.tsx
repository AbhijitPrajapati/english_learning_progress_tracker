import type { Metadata } from "next";
import "./globals.css";
import { ApplicationProvider, AuthProvider } from "./providers";

export const metadata: Metadata = {
  title: "Grammar Tracker",
  description: "Upload speech samples and review grammar analytics",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full font-sans antialiased">
      <body className="min-h-full flex flex-col">
        <ApplicationProvider>
          <AuthProvider>{children}</AuthProvider>
        </ApplicationProvider>
      </body>
    </html>
  );
}
