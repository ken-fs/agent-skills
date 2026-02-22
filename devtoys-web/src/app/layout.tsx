import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { Toaster } from "@/components/ui/sonner";
import { cn } from "@/lib/utils";
import { TooltipProvider } from "@/components/ui/tooltip";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "DevToys - Developer Tools Reimagined",
  description: "A modern, privacy-first developer tool suite.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning className="dark">
      <body
        className={cn(
          "min-h-screen bg-[#0F172A] text-[#F8FAFC] font-sans antialiased selection:bg-[#22C55E]/30",
          geistSans.variable,
          geistMono.variable
        )}
      >
        <TooltipProvider delayDuration={100}>
          {children}
        </TooltipProvider>
        <Toaster 
          toastOptions={{
            classNames: {
              error: '!bg-red-500 !text-white !border-red-600',
            }
          }}
        />
      </body>
    </html>
  );
}
