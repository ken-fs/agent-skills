import { Metadata } from "next";
import { ImageCompressorClient } from "@/components/tools/image/ImageCompressorClient";
import { ToolLayout } from "@/components/layout/ToolLayout";

export const metadata: Metadata = {
  title: "Image Compressor & Converter - DevToys",
  description: "Compress images and convert formats (WebP, JPG, PNG) locally in your browser. Privacy-first, no server uploads.",
};

export default function ImageCompressorPage() {
  return (
    <ToolLayout>
      <div className="flex h-full flex-col">
        {/* Header inside Tool */}
        <div className="flex-shrink-0 h-16 border-b border-white/5 bg-[#1E293B]/20 backdrop-blur-md px-6 flex items-center shrink-0">
          <div>
            <h1 className="text-xl font-bold tracking-tight text-[#F8FAFC] font-heading">Image Compressor</h1>
            <p className="text-sm text-[#F8FAFC]/50">Resize, compress, and convert images locally.</p>
          </div>
        </div>
        {/* Full bleed processing area */}
        <div className="flex-1 overflow-hidden">
          <ImageCompressorClient />
        </div>
      </div>
    </ToolLayout>
  );
}
