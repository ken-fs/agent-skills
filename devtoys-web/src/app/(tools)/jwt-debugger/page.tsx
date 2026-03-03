import { Metadata } from "next";
import { JwtDecoderClient } from "@/components/tools/jwt/JwtDecoderClient";
import { ToolLayout } from "@/components/layout/ToolLayout";

export const metadata: Metadata = {
  title: "Free Online JWT Decoder and Debugger",
  description: "Decode, verify, and inspect JSON Web Tokens (JWT) easily and securely. Free online developer tool. Everything runs locally in your browser.",
  keywords: ["JWT Decoder", "JWT Debugger", "JSON Web Token", "Decode JWT", "Verify JWT", "Online JWT Tool", "Developer Tools"],
  alternates: {
    canonical: "/jwt-debugger",
  },
};

export default function JwtDebuggerPage() {
  return (
    <ToolLayout>
      <div className="flex h-full flex-col">
        <div className="flex-shrink-0 h-16 border-b border-white/5 bg-[#1E293B]/20 backdrop-blur-md px-6 flex items-center">
          <div>
            <h1 className="text-xl font-bold tracking-tight text-[#F8FAFC] font-heading">JWT Decoder / Debugger</h1>
            <p className="text-sm text-[#F8FAFC]/50">Decode and inspect JSON Web Tokens instantly.</p>
          </div>
        </div>
        <div className="flex-1 overflow-hidden">
          <JwtDecoderClient />
        </div>
      </div>
    </ToolLayout>
  );
}
