import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "HealthAI Risk Dashboard",
  description: "AI-powered health risk prediction and prevention recommendations.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen">
          <header className="sticky top-0 z-50 border-b border-white/10 bg-[rgba(4,8,20,0.48)] backdrop-blur-lg">
            <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-6 py-5">
              <div className="flex items-center gap-3">
                <div className="grid h-11 w-11 place-items-center rounded-2xl bg-gradient-to-br from-indigo-500 via-sky-400 to-orange-400 shadow-[0_18px_35px_rgba(0,0,0,0.3)]">
                  <span className="text-xl">❤️</span>
                </div>
                <div>
                  <h1 className="text-lg font-semibold tracking-tight text-white">HealthAI</h1>
                  <p className="text-xs text-white/70">Smart risk prediction & prevention</p>
                </div>
              </div>
              <div className="hidden items-center gap-2 rounded-full bg-white/10 px-4 py-2 text-xs text-white/80 sm:flex">
                <span className="inline-flex h-2 w-2 rounded-full bg-emerald-400" />
                Live demo
              </div>
            </div>
          </header>
          <main className="mx-auto max-w-6xl px-6 py-10">{children}</main>
        </div>
      </body>
    </html>
  );
}
