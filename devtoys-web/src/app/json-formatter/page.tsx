import { Metadata } from "next";
import { JsonFormatterClient } from "@/components/tools/json/JsonFormatterClient";

export const metadata: Metadata = {
  title: "JSON Formatter & Validator - DevToys",
  description: "Validate, format, minity, and beautify your JSON data with this free online tool. Privacy-first, no server-side processing.",
};

export default function JsonFormatterPage() {
  return (
    <div className="flex select-none flex-col">
      <div className="container py-4">
        <h1 className="text-2xl font-bold tracking-tight">JSON Formatter</h1>
        <p className="text-muted-foreground">
          Validate, format, and minify JSON data.
        </p>
      </div>
      <div className="flex-1 border-t border-border/50">
        <JsonFormatterClient />
      </div>
    </div>
  );
}
