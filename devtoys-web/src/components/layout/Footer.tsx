export function Footer() {
  return (
    <footer className="py-6 md:px-8 md:py-0 border-t border-white/5 mt-auto bg-[#0F172A]/50 backdrop-blur-xl z-10 w-full relative">
      <div className="container flex flex-col items-center justify-between gap-4 md:h-16 md:flex-row">
        <p className="text-balance text-center text-sm leading-loose text-[#F8FAFC]/50 md:text-left transition-colors">
          Built by{" "}
          <a
            href="https://github.com/wangzf"
            target="_blank"
            rel="noreferrer"
            className="font-medium text-[#F8FAFC]/80 underline underline-offset-4 hover:text-[#22C55E] transition-colors duration-200"
          >
            Ken
          </a>
          . The source code is available on{" "}
          <a
            href="https://github.com/wangzf/devtoys-web"
            target="_blank"
            rel="noreferrer"
            className="font-medium text-[#F8FAFC]/80 underline underline-offset-4 hover:text-[#22C55E] transition-colors duration-200"
          >
            GitHub
          </a>
          .
        </p>
      </div>
    </footer>
  );
}
