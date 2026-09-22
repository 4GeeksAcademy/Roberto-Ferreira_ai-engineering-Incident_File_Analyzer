import "./globals.css";

export const metadata = { title: "Brasaland Operations · Incident Analysis", description: "Brasaland incident report analysis workspace" };

export default function Layout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
