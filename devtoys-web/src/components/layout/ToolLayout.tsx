import Link from "next/link";
import {
  FileJson,
  Binary,
  Link as LinkIcon,
  KeyRound,
  Fingerprint,
  FileText,
  Command,
  Home,
  Image as ImageIcon,
} from "lucide-react";
import { cn } from "@/lib/utils";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

const tools = [
  { href: "/", icon: Home, label: "Home" },
  { href: "/json-formatter", icon: FileJson, label: "JSON Formatter" },
  { href: "/image-compressor", icon: ImageIcon, label: "Image Compressor" },
  { href: "/base64", icon: Binary, label: "Base64 Encoder" },
  { href: "/url-encoder", icon: LinkIcon, label: "URL Encoder" },
  { href: "/jwt-debugger", icon: KeyRound, label: "JWT Debugger" },
  { href: "/uuid", icon: Fingerprint, label: "UUID Generator" },
  { href: "/lorem-ipsum", icon: FileText, label: "Lorem Ipsum" },
];

export function ToolLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen w-full bg-[#0F172A] overflow-hidden text-[#F8FAFC]">
      {/* Left Arc-style Dock Sidebar */}
      <aside className="w-16 flex-shrink-0 glass-panel border-r border-white/5 flex flex-col items-center py-6 gap-6 z-20">
        <Link href="/" className="mb-4" title="Home">
          <Command className="h-7 w-7 text-[#F8FAFC] drop-shadow-md hover:scale-110 transition-transform" />
        </Link>
        <nav className="flex flex-col gap-4">
          {tools.map((tool) => (
            <Tooltip key={tool.href}>
              <TooltipTrigger asChild>
                <Link
                  href={tool.href}
                  className="relative group p-2 rounded-xl hover:bg-[#1E293B]/80 transition-all duration-300"
                >
                  <tool.icon className="h-6 w-6 text-[#F8FAFC]/50 group-hover:text-[#22C55E]" />
                </Link>
              </TooltipTrigger>
              <TooltipContent side="right" sideOffset={10} className="bg-[#1E293B] border-white/10 text-[#F8FAFC] font-medium tracking-wide">
                {tool.label}
              </TooltipContent>
            </Tooltip>
          ))}
        </nav>
      </aside>

      {/* Main Tool Content Area */}
      <main className="flex-1 overflow-hidden relative z-10">
        {/* Subtle glowing orbs for Glassmorphism Depth in tool views */}
        <div className="absolute top-[-20%] right-[-10%] w-[50vw] h-[50vw] rounded-full bg-[#22C55E]/5 mix-blend-screen blur-[120px] pointer-events-none" />
        <div className="absolute bottom-[-20%] left-[-10%] w-[50vw] h-[50vw] rounded-full bg-[#1E293B]/40 mix-blend-screen blur-[120px] pointer-events-none" />
        
        {children}
      </main>
    </div>
  );
}
