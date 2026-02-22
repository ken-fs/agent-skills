import Link from "next/link";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Code2, FileJson, Binary, Link as LinkIcon, KeyRound, Fingerprint, FileText, ImageIcon, Search, ArrowRight } from "lucide-react";

// Categorized tools list matching the original concept
const tools = [
  {
    category: "Media & Graphic",
    items: [
      {
        title: "Image Compressor & Converter",
        description: "Resize, compress, and convert (WebP, JPG, PNG) strictly locally. Zero server uploads.",
        icon: ImageIcon,
        href: "/image-compressor",
      },
    ],
  },
  {
    category: "Formatters",
    items: [
      {
        title: "JSON Formatter",
        description: "Validate, format, minify, and beautify your JSON data instantly.",
        icon: FileJson,
        href: "/json-formatter",
      },
    ],
  },
  {
    category: "Encoders / Decoders",
    items: [
      {
        title: "Base64 Encoder/Decoder",
        description: "Encode and decode text or images to Base64 format.",
        icon: Binary,
        href: "/base64",
      },
      {
        title: "URL Encoder/Decoder",
        description: "Convert characters to their corresponding URL-encoded values.",
        icon: LinkIcon,
        href: "/url-encoder",
      },
    ],
  },
  {
    category: "Generators",
    items: [
      {
        title: "UUID Generator",
        description: "Generate universally unique identifiers (UUIDs) version 1 or 4.",
        icon: Fingerprint,
        href: "/uuid",
      },
      {
        title: "Lorem Ipsum",
        description: "Generate placeholder text for varying lengths.",
        icon: FileText,
        href: "/lorem-ipsum",
      },
    ],
  },
  {
    category: "Text",
    items: [
      {
        title: "JWT Debugger",
        description: "Decode and inspect JSON Web Tokens safely in the browser.",
        icon: KeyRound,
        href: "/jwt-debugger",
      },
      {
        title: "Text Diff",
        description: "Compare two texts and highlight the differences.",
        icon: Code2,
        href: "/text-diff",
      },
    ],
  },
];

export default function Home() {
  return (
    <div className="container mx-auto relative flex flex-col items-center justify-center py-16 space-y-16 md:py-24 lg:py-32">
      {/* Deep Dark Ambient Background */}
      <div className="fixed inset-0 -z-10 h-full w-full bg-[#0F172A] overflow-hidden">
        {/* Subtle glowing orbs for Glassmorphism Depth */}
        <div className="absolute top-[-20%] left-[-10%] w-[70vw] h-[70vw] rounded-full bg-[#1E293B]/60 mix-blend-screen blur-[120px] animate-blob" />
        <div className="absolute bottom-[-20%] right-[-10%] w-[70vw] h-[70vw] rounded-full bg-[#22C55E]/10 mix-blend-screen blur-[120px] animate-blob animation-delay-2000" />
      </div>

      <section className="mx-auto flex max-w-[980px] flex-col items-center gap-6 text-center z-10">
        <div className="inline-flex items-center rounded-full border border-white/10 bg-white/5 px-3 py-1 text-sm font-medium text-[#F8FAFC]/80 backdrop-blur-md mb-4">
          ✨ The ultimate tool suite for developers
        </div>
        <h1 className="text-5xl font-extrabold tracking-tight text-[#F8FAFC] sm:text-6xl md:text-7xl lg:text-8xl drop-shadow-xl font-heading leading-tight">
          Tools for <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-[#22C55E]">Builders</span>
        </h1>
        <p className="max-w-[700px] text-lg font-medium text-[#F8FAFC]/70 sm:text-xl drop-shadow-md">
          A minimalist, privacy-first developer companion. Build, debug, and ship faster.
        </p>

        <div className="relative w-full max-w-2xl mt-8">
          <div className="relative group">
            {/* Glowing input border effect */}
            <div className="absolute -inset-0.5 bg-gradient-to-r from-[#1E293B] to-[#22C55E]/30 rounded-2xl blur opacity-30 group-hover:opacity-100 transition duration-500"></div>
            <div className="relative flex items-center glass-panel rounded-2xl group-hover:bg-[#1E293B]/50">
              <Search className="ml-4 h-6 w-6 text-[#F8FAFC]/50" />
              <Input
                type="text"
                placeholder="Search tools (Press ⌘K)"
                className="border-0 shadow-none focus-visible:ring-0 pl-4 h-16 text-lg bg-transparent text-[#F8FAFC] placeholder:text-[#F8FAFC]/40"
              />
              <div className="pr-4 hidden sm:block">
                <kbd className="pointer-events-none inline-flex h-8 select-none items-center gap-1 rounded-[6px] border border-white/10 bg-black/20 px-2 font-mono text-[12px] font-medium text-[#F8FAFC]/60 backdrop-blur-md">
                  <span className="text-sm">⌘</span>K
                </kbd>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Bento Grid layout */}
      <section className="mx-auto grid max-w-6xl grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 w-full px-4 z-10">
        {tools.flatMap(c => c.items).map((tool) => (
          <Link href={tool.href} key={tool.title} className="group">
            <div className="relative h-full overflow-hidden rounded-3xl glass-panel glass-panel-hover p-8 group-hover:cursor-pointer flex flex-col justify-between">
              {/* Internal Glass Highlight */}
              <div className="absolute inset-0 z-[-1] bg-gradient-to-br from-white/5 to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100 rounded-3xl" />
              
              <div>
                <div
                  className={`mb-6 inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-[#0F172A] text-[#F8FAFC] border border-white/5 shadow-inner group-hover:text-[#22C55E] group-hover:bg-[#1E293B] transition-all duration-300`}
                >
                  <tool.icon className="h-7 w-7 drop-shadow-md" />
                </div>
                <h3 className="mb-3 text-2xl font-bold tracking-tight text-[#F8FAFC] drop-shadow-sm font-heading">
                  {tool.title}
                </h3>
                <p className="text-base text-[#F8FAFC]/60 mb-6 font-medium leading-relaxed">
                  {tool.description}
                </p>
              </div>
              <div className="flex items-center text-sm font-bold text-[#22C55E] opacity-0 -translate-x-4 transition-all duration-300 group-hover:opacity-100 group-hover:translate-x-0 mt-auto">
                Launch <ArrowRight className="ml-2 h-5 w-5" />
              </div>
            </div>
          </Link>
        ))}
      </section>
    </div>
  );
}
