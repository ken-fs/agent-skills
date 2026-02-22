import Link from "next/link";
import {
  FileJson,
  Binary,
  Link as LinkIcon,
  KeyRound,
  Fingerprint,
  FileText,
  Search,
  ArrowRight,
} from "lucide-react";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

const tools = [
  {
    title: "JSON Formatter",
    description: "Validate, format, and minify JSON data automatically.",
    href: "/json-formatter",
    icon: FileJson,
    color: "text-white",
    bgColor: "bg-white/10 dark:bg-white/5",
  },
  {
    title: "Base64 Encoder",
    description: "Encode and decode data using Base64 standard.",
    href: "/base64",
    icon: Binary,
    color: "text-white",
    bgColor: "bg-white/10 dark:bg-white/5",
  },
  {
    title: "URL Encoder",
    description: "Encode and decode URLs for safe transmission.",
    href: "/url-encoder",
    icon: LinkIcon,
    color: "text-white",
    bgColor: "bg-white/10 dark:bg-white/5",
  },
  {
    title: "JWT Debugger",
    description: "Decode, verify, and inspect JSON Web Tokens.",
    href: "/jwt-debugger",
    icon: KeyRound,
    color: "text-white",
    bgColor: "bg-white/10 dark:bg-white/5",
  },
  {
    title: "UUID Generator",
    description: "Generate unique identifiers (UUID/GUID) in bulk.",
    href: "/uuid",
    icon: Fingerprint,
    color: "text-white",
    bgColor: "bg-white/10 dark:bg-white/5",
  },
  {
    title: "Lorem Ipsum",
    description: "Generate placeholder text for your designs.",
    href: "/lorem-ipsum",
    icon: FileText,
    color: "text-white",
    bgColor: "bg-white/10 dark:bg-white/5",
  },
];

export default function Home() {
  return (
    <div className="container relative flex flex-col items-center justify-center py-12 space-y-12 md:py-24 lg:py-32">
      {/* iOS Liquid Glass Mesh Background */}
      <div className="fixed inset-0 -z-10 h-full w-full bg-black overflow-hidden">
        {/* Animated Orbs for Liquid Effect */}
        <div className="absolute top-[-10%] left-[-10%] w-[60vw] h-[60vw] rounded-full bg-purple-600/40 mix-blend-screen blur-[120px] animate-blob" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[60vw] h-[60vw] rounded-full bg-blue-600/40 mix-blend-screen blur-[120px] animate-blob animation-delay-2000" />
        <div className="absolute top-[30%] left-[20%] w-[50vw] h-[50vw] rounded-full bg-cyan-500/30 mix-blend-screen blur-[100px] animate-blob animation-delay-4000" />
      </div>

      <section className="mx-auto flex max-w-[980px] flex-col items-center gap-6 text-center">
        <h1 className="text-5xl font-extrabold tracking-tight text-white sm:text-6xl md:text-7xl lg:text-8xl drop-shadow-xl">
          Developer Tools
        </h1>
        <p className="max-w-[700px] text-lg font-medium text-white/80 sm:text-xl drop-shadow-md">
          Build. Debug. Ship. Faster.
        </p>

        <div className="relative w-full max-w-2xl mt-8">
          <div className="relative group">
            {/* Glowing input border effect */}
            <div className="absolute -inset-0.5 bg-gradient-to-r from-white/20 to-white/0 rounded-2xl blur opacity-50 group-hover:opacity-100 transition duration-500"></div>
            <div className="relative flex items-center bg-white/10 hover:bg-white/15 backdrop-blur-3xl rounded-2xl border border-white/20 shadow-[0_8px_32px_0_rgba(0,0,0,0.3)] transition-all duration-300">
              <Search className="ml-4 h-6 w-6 text-white/70" />
              <Input
                type="text"
                placeholder="Search tools (Press ⌘K)"
                className="border-0 shadow-none focus-visible:ring-0 pl-4 h-16 text-lg bg-transparent text-white placeholder:text-white/50"
              />
              <div className="pr-4 hidden sm:block">
                <kbd className="pointer-events-none inline-flex h-8 select-none items-center gap-1 rounded-[6px] border border-white/20 bg-white/10 px-2 font-mono text-[12px] font-medium text-white/80 backdrop-blur-md">
                  <span className="text-sm">⌘</span>K
                </kbd>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto grid max-w-6xl grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 w-full px-4">
        {tools.map((tool) => (
          <Link href={tool.href} key={tool.title} className="group">
            <div className="relative h-full overflow-hidden rounded-3xl bg-white/10 backdrop-blur-[40px] border border-white/20 p-8 shadow-[0_8px_32px_0_rgba(0,0,0,0.2)] transition-all duration-500 hover:-translate-y-2 hover:bg-white/20 hover:border-white/40 hover:shadow-[0_16px_48px_0_rgba(0,0,0,0.4)]">
              {/* Internal Glass Highlight */}
              <div className="absolute inset-0 z-[-1] bg-gradient-to-br from-white/20 to-transparent opacity-0 transition-opacity duration-500 group-hover:opacity-100 rounded-3xl" />
              
              <div
                className={`mb-6 inline-flex h-16 w-16 items-center justify-center rounded-2xl ${tool.bgColor} ${tool.color} border border-white/10 shadow-inner`}
              >
                <tool.icon className="h-8 w-8 drop-shadow-md" />
              </div>
              <h3 className="mb-3 text-2xl font-semibold tracking-tight text-white drop-shadow-sm">
                {tool.title}
              </h3>
              <p className="text-base text-white/70 mb-6 font-medium leading-relaxed">
                {tool.description}
              </p>
              <div className="flex items-center text-sm font-bold text-white opacity-0 -translate-x-4 transition-all duration-300 group-hover:opacity-100 group-hover:translate-x-0">
                Open Tool <ArrowRight className="ml-2 h-5 w-5" />
              </div>
            </div>
          </Link>
        ))}
      </section>
    </div>
  );
}
