import Link from "next/link";
import { Command, Github } from "lucide-react";

export function Navbar() {
  return (
    <header className="fixed top-0 z-50 w-full border-b border-white/5 bg-[#0F172A]/50 backdrop-blur-xl supports-[backdrop-filter]:bg-[#0F172A]/50 transition-colors duration-300">
      <div className="container flex h-16 max-w-screen-2xl items-center">
        <Link href="/" className="mr-6 flex items-center space-x-2">
          <Command className="h-6 w-6 text-[#F8FAFC] drop-shadow-md transition-transform hover:scale-110" />
          <span className="hidden font-bold sm:inline-block text-[#F8FAFC] text-lg tracking-tight drop-shadow-md font-heading">
            DevToys
          </span>
        </Link>
        <nav className="flex flex-1 items-center space-x-6 text-sm font-medium">
          <Link
            href="/docs"
            className="transition-colors duration-300 hover:text-[#22C55E] text-[#F8FAFC]/70"
          >
            Docs
          </Link>
          <Link
            href="/tools"
            className="transition-colors duration-300 hover:text-[#22C55E] text-[#F8FAFC]/70"
          >
            Tools
          </Link>
        </nav>
        <div className="flex flex-1 items-center justify-end space-x-2">
          <nav className="flex items-center">
            <Link
              href="https://github.com/wangzf/devtoys-web"
              target="_blank"
              rel="noreferrer"
            >
              <div
                className="inline-flex items-center justify-center whitespace-nowrap rounded-lg text-sm font-medium transition-all duration-300 hover:bg-[#1E293B]/80 hover:text-[#22C55E] text-[#F8FAFC]/70 h-10 w-10 px-0 hover:shadow-[0_0_15px_rgba(34,197,94,0.3)]"
              >
                <Github className="h-5 w-5" />
                <span className="sr-only">GitHub</span>
              </div>
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
}
