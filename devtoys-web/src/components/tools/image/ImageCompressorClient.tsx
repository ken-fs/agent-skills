"use client";

import * as React from "react";
import { toast } from "sonner";
import {
  UploadCloud,
  Image as ImageIcon,
  Download,
  Settings2,
  ImageDown,
  RefreshCw,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

const formatBytes = (bytes: number) => {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
};

export function ImageCompressorClient() {
  const [file, setFile] = React.useState<File | null>(null);
  const [originalUrl, setOriginalUrl] = React.useState<string>("");
  const [originalSize, setOriginalSize] = React.useState(0);
  
  const [compressedUrl, setCompressedUrl] = React.useState<string>("");
  const [compressedSize, setCompressedSize] = React.useState(0);
  
  const [quality, setQuality] = React.useState([80]);
  const [format, setFormat] = React.useState("image/webp");
  const [isProcessing, setIsProcessing] = React.useState(false);

  // File selection
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      processInitialFile(e.target.files[0]);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.type.startsWith("image/")) {
        processInitialFile(droppedFile);
      } else {
        toast.error("Please drop an image file.");
      }
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };

  const processInitialFile = (newFile: File) => {
    setFile(newFile);
    setOriginalSize(newFile.size);
    const url = URL.createObjectURL(newFile);
    setOriginalUrl(url);
    // Initial compression trigger will happen in useEffect
  };

  // Compression Logic
  const compressImage = React.useCallback(async () => {
    if (!originalUrl || !file) return;
    setIsProcessing(true);

    try {
      const img = new Image();
      img.src = originalUrl;
      await new Promise((resolve, reject) => {
        img.onload = resolve;
        img.onerror = reject;
      });

      const canvas = document.createElement("canvas");
      canvas.width = img.width;
      canvas.height = img.height;
      const ctx = canvas.getContext("2d");
      
      if (!ctx) throw new Error("Could not get 2D context");
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

      canvas.toBlob(
        (blob) => {
          if (blob) {
            setCompressedSize(blob.size);
            if (compressedUrl) URL.revokeObjectURL(compressedUrl);
            setCompressedUrl(URL.createObjectURL(blob));
            setIsProcessing(false);
          }
        },
        format,
        quality[0] / 100
      );
    } catch (err) {
      console.error(err);
      toast.error("Failed to process image");
      setIsProcessing(false);
    }
  }, [originalUrl, file, quality, format]); // eslint-disable-line react-hooks/exhaustive-deps

  // Auto-recompress when settings change
  React.useEffect(() => {
    if (file) {
      const timeoutId = setTimeout(() => compressImage(), 300);
      return () => clearTimeout(timeoutId);
    }
  }, [quality, format, file, compressImage]);

  const handleDownload = () => {
    if (!compressedUrl) return;
    const a = document.createElement("a");
    a.href = compressedUrl;
    const extension = format.split("/")[1];
    const originalName = file?.name.split(".")[0] || "image";
    a.download = `${originalName}-compressed.${extension}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    toast.success("Image downloaded successfully!");
  };

  const handleReset = () => {
    setFile(null);
    if (originalUrl) URL.revokeObjectURL(originalUrl);
    if (compressedUrl) URL.revokeObjectURL(compressedUrl);
    setOriginalUrl("");
    setCompressedUrl("");
  };

  if (!file) {
    return (
      <div 
        className="flex h-full w-full items-center justify-center p-8"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        <div className="flex flex-col items-center justify-center p-12 text-center rounded-3xl border-2 border-dashed border-[#22C55E]/30 bg-[#1E293B]/20 backdrop-blur-md transition-all hover:bg-[#1E293B]/40 hover:border-[#22C55E]/60 max-w-2xl w-full cursor-pointer h-96 group"
             onClick={() => document.getElementById('image-upload')?.click()}>
          <div className="mb-6 rounded-full bg-[#22C55E]/10 p-6 group-hover:scale-110 transition-transform duration-500">
            <UploadCloud className="h-12 w-12 text-[#22C55E]" />
          </div>
          <h3 className="mb-2 text-3xl font-bold tracking-tight text-[#F8FAFC]">Upload Image</h3>
          <p className="mb-8 text-[#F8FAFC]/60 font-medium">Drag and drop an image here, or click to browse.</p>
          <div className="flex gap-4">
             <Badge variant="outline" className="bg-black/20 border-white/10 text-[#F8FAFC]/50">JPG</Badge>
             <Badge variant="outline" className="bg-black/20 border-white/10 text-[#F8FAFC]/50">PNG</Badge>
             <Badge variant="outline" className="bg-black/20 border-white/10 text-[#F8FAFC]/50">WebP</Badge>
          </div>
          <input
            id="image-upload"
            type="file"
            accept="image/*"
            className="hidden"
            onChange={handleFileSelect}
          />
        </div>
      </div>
    );
  }

  const reduction = compressedSize 
    ? ((originalSize - compressedSize) / originalSize * 100).toFixed(1)
    : "0.0";

  return (
    <div className="flex h-full flex-col overflow-hidden bg-[#0F172A] relative">
      <div className="flex h-16 items-center border-b border-white/5 bg-[#1E293B]/40 px-6 backdrop-blur-md justify-between z-20">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-3">
             <span className="text-xs font-bold tracking-wider text-[#F8FAFC]/50 uppercase">Settings</span>
             <Settings2 className="h-4 w-4 text-[#F8FAFC]/50" />
          </div>
          <div className="flex items-center gap-4">
             <span className="text-sm font-medium text-[#F8FAFC]">Format:</span>
             <Select value={format} onValueChange={setFormat}>
                <SelectTrigger className="h-9 w-[120px] bg-black/20 border-white/10 text-[#F8FAFC] focus:ring-1 focus:ring-[#22C55E]">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-[#1E293B] border-white/10 text-[#F8FAFC]">
                  <SelectItem value="image/webp" className="focus:bg-[#22C55E]/20">WebP</SelectItem>
                  <SelectItem value="image/jpeg" className="focus:bg-[#22C55E]/20">JPEG</SelectItem>
                  <SelectItem value="image/png" className="focus:bg-[#22C55E]/20">PNG</SelectItem>
                </SelectContent>
             </Select>
          </div>
          <div className="flex items-center gap-4 hidden md:flex">
             <span className="text-sm font-medium text-[#F8FAFC] w-20">Quality: {quality[0]}%</span>
             <Slider
                value={quality}
                onValueChange={setQuality}
                max={100}
                min={1}
                step={1}
                className="w-48"
                disabled={format === 'image/png'} // PNG canvas native toBlob ignores quality
             />
          </div>
        </div>
        <Button variant="ghost" size="sm" onClick={handleReset} className="text-[#F8FAFC]/70 hover:text-white hover:bg-white/10">
          <RefreshCw className="h-4 w-4 mr-2" /> Reset
        </Button>
      </div>

      <div className="flex flex-1 flex-col lg:flex-row relative">
        {/* Left Pane - Original */}
        <div className="flex-1 flex flex-col border-b lg:border-b-0 lg:border-r border-white/5 relative p-6 items-center justify-center">
            <Badge variant="outline" className="absolute top-6 left-6 bg-[#1E293B] border-white/10 text-[#F8FAFC] z-10">
              Original • {formatBytes(originalSize)}
            </Badge>
            <div className="relative w-full h-full max-h-full flex items-center justify-center p-4">
               {/* eslint-disable-next-line @next/next/no-img-element */}
               <img 
                 src={originalUrl} 
                 alt="Original" 
                 className="max-w-full max-h-full object-contain rounded-lg shadow-2xl drop-shadow-[0_0_15px_rgba(255,255,255,0.05)] border border-white/5"
               />
            </div>
        </div>

        {/* Floating Action Center */}
        <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-30 hidden lg:flex flex-col gap-2 p-2 rounded-2xl glass-panel bg-[#1E293B]/60 shadow-2xl border border-white/10">
           <Button
              onClick={handleDownload}
              size="icon"
              disabled={isProcessing || !compressedUrl}
              className="rounded-xl h-12 w-12 bg-[#22C55E] text-[#0F172A] hover:bg-[#16a34a] shadow-[0_0_15px_rgba(34,197,94,0.4)] transition-all"
              title="Download Compressed Image"
           >
              {isProcessing ? <RefreshCw className="h-5 w-5 animate-spin" /> : <Download className="h-5 w-5" />}
           </Button>
        </div>

        {/* Right Pane - Compressed */}
        <div className="flex-1 flex flex-col relative p-6 items-center justify-center bg-[url('/checkers.svg')] bg-[#0F172A]/80 bg-blend-overlay">
            <div className="absolute top-6 left-6 z-10 flex flex-col gap-2">
              <Badge variant="outline" className="bg-[#22C55E]/10 border-[#22C55E]/30 text-[#22C55E]">
                Compressed • {formatBytes(compressedSize)}
              </Badge>
              {Number(reduction) > 0 && (
                 <Badge variant="default" className="bg-[#22C55E] text-[#0F172A] font-bold border-none w-fit">
                   <ImageDown className="w-3 h-3 mr-1"/> -{reduction}%
                 </Badge>
              )}
            </div>
            <div className="relative w-full h-full max-h-full flex items-center justify-center p-4">
               {compressedUrl && (
                  // eslint-disable-next-line @next/next/no-img-element
                 <img 
                   src={compressedUrl} 
                   alt="Compressed preview" 
                   className={cn(
                     "max-w-full max-h-full object-contain rounded-lg shadow-2xl border transition-opacity duration-300",
                     isProcessing ? "opacity-50 blur-sm border-white/5" : "opacity-100 border-[#22C55E]/30 drop-shadow-[0_0_20px_rgba(34,197,94,0.15)]"
                   )}
                 />
               )}
            </div>
        </div>
      </div>
      
      {/* Mobile Action Bottom Bar */}
      <div className="flex lg:hidden h-16 w-full items-center justify-center gap-4 bg-[#1E293B]/80 backdrop-blur-md z-20 border-t border-white/5 absolute bottom-0">
          <Button
              onClick={handleDownload}
              disabled={isProcessing || !compressedUrl}
              className="w-3/4 rounded-xl bg-[#22C55E] text-[#0F172A] hover:bg-[#16a34a] font-bold"
           >
              {isProcessing ? <RefreshCw className="h-4 w-4 mr-2 animate-spin" /> : <Download className="h-4 w-4 mr-2" />} 
              Download ({formatBytes(compressedSize)})
           </Button>
      </div>

    </div>
  );
}
