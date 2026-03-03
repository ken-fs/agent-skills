import { Metadata } from "next";
import { JsonSchemaValidatorClient } from "@/components/tools/json/JsonSchemaValidatorClient";
import { ToolLayout } from "@/components/layout/ToolLayout";

export const metadata: Metadata = {
  title: "Free Online JSON Schema Validator",
  description: "Validate your JSON data against JSON Schema instantly. Supports multiple drafts. Free online developer tool. Everything runs locally in your browser for total privacy.",
  keywords: ["JSON Schema Validator", "JSON Validator", "JSON Schema", "Online JSON Schema Tool", "AJV Validator", "Developer Tools"],
  alternates: {
    canonical: "/json-schema-validator",
  },
};

export default function JsonSchemaValidatorPage() {
  return (
    <ToolLayout>
      <div className="flex h-full flex-col">
        <div className="flex-shrink-0 h-16 border-b border-white/5 bg-[#1E293B]/20 backdrop-blur-md px-6 flex items-center">
          <div>
            <h1 className="text-xl font-bold tracking-tight text-[#F8FAFC] font-heading">JSON Schema Validator</h1>
            <p className="text-sm text-[#F8FAFC]/50">Verify your JSON data against a defined Schema.</p>
          </div>
        </div>
        <div className="flex-1 overflow-hidden">
          <JsonSchemaValidatorClient />
        </div>
      </div>
    </ToolLayout>
  );
}
