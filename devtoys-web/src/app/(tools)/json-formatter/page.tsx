import { Metadata } from "next";
import { JsonFormatterClient } from "@/components/tools/json/JsonFormatterClient";
import { ToolLayout } from "@/components/layout/ToolLayout";

export const metadata: Metadata = {
  title: "JSON Formatter - DevToys",
  description: "Validate, format, minify, and beautify your JSON data with this free online tool.",
};

export default function JsonFormatterPage() {
  return (
    <ToolLayout>
      <div className="flex h-full flex-col">
        {/* Header inside Tool */}
        <div className="flex-shrink-0 h-16 border-b border-white/5 bg-[#1E293B]/20 backdrop-blur-md px-6 flex items-center">
          <div>
            <h1 className="text-xl font-bold tracking-tight text-[#F8FAFC] font-heading">JSON Formatter</h1>
            <p className="text-sm text-[#F8FAFC]/50">Validate, format, and minify JSON data.</p>
          </div>
        </div>
        {/* Full bleed editor area */}
        <div className="flex-1 overflow-hidden">
          <JsonFormatterClient />
        </div>
      </div>
    </ToolLayout>
  );
}
