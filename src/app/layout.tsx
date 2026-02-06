import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "pump.notdump.fun — Anti-Rug Launchpad for AI Agent Tokens",
  description:
    "The first launchpad where rug-pulls are structurally impossible. Smart contracts enforce vesting, liquidity locks, and revenue buybacks. Built on Solana.",
  keywords: [
    "solana",
    "token launchpad",
    "anti-rug",
    "AI agent tokens",
    "crypto",
    "pump.fun",
    "defi",
  ],
  openGraph: {
    title: "pump.notdump.fun — Anti-Rug Launchpad",
    description:
      "98.6% of meme tokens are rugs. We're building the other 1.4%. Smart contract enforced trust.",
    url: "https://pumpnotdump.fun",
    siteName: "pump.notdump.fun",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "pump.notdump.fun — Anti-Rug Launchpad",
    description:
      "98.6% of meme tokens are rugs. We're building the other 1.4%.",
    creator: "@SkipperAGI",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="antialiased">{children}</body>
    </html>
  );
}
