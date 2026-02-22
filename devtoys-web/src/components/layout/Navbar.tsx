import Link from "next/link";
import { Command, Github } from "lucide-react";

export function Navbar() {
  return (
    <header className="fixed top-0 z-50 w-full border-b border-white/10 bg-black/20 backdrop-blur-3xl supports-[backdrop-filter]:bg-black/20">
      <div className="container flex h-16 max-w-screen-2xl items-center">
        <Link href="/" className="mr-6 flex items-center space-x-2">
          <Command className="h-6 w-6 text-white drop-shadow-md" />
          <span className="hidden font-bold sm:inline-block text-white text-lg tracking-tight drop-shadow-md">
            DevToys
          </span>
        </Link>
        <nav className="flex flex-1 items-center space-x-6 text-sm font-medium">
          <Link
            href="/docs"
            className="transition-colors hover:text-white text-white/70"
          >
            Docs
          </Link>
          <Link
            href="/tools"
            className="transition-colors hover:text-white text-white/70"
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
                className="inline-flex items-center justify-center whitespace-nowrap rounded-lg text-sm font-medium transition-colors hover:bg-white/20 hover:text-white text-white/70 h-10 w-10 px-0"
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
