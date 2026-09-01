import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Talent Pipeline Tracker",
  description: "Internal recruiting frontend scaffold for the typed API client."
};

type RootLayoutProps = Readonly<{
  children: React.ReactNode;
}>;

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}