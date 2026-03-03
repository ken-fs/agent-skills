"use client";

import * as React from "react";
import Editor from "@monaco-editor/react";
import { toast } from "sonner";
import { Copy, Trash2, KeyRound } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

export function JwtDecoderClient() {
  const [input, setInput] = React.useState<string>("");
  const [header, setHeader] = React.useState<string>("");
  const [payload, setPayload] = React.useState<string>("");
  const [signature, setSignature] = React.useState<string>("");
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    if (!input.trim()) {
      setHeader("");
      setPayload("");
      setSignature("");
      setError(null);
      return;
    }

    try {
      const parts = input.trim().split('.');
      if (parts.length !== 3) {
        throw new Error("Invalid JWT token format. Must have exactly 3 parts separated by dots.");
      }

      const decodeBase64Url = (str: string) => {
        let base64 = str.replace(/-/g, '+').replace(/_/g, '/');
        while (base64.length % 4) {
          base64 += '=';
        }
        return decodeURIComponent(escape(window.atob(base64)));
      };

      const parsedHeader = JSON.parse(decodeBase64Url(parts[0]));
      const parsedPayload = JSON.parse(decodeBase64Url(parts[1]));

      setHeader(JSON.stringify(parsedHeader, null, 2));
      setPayload(JSON.stringify(parsedPayload, null, 2));
      setSignature(parts[2]); // signature is raw
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
  }, [input]);

  const handleClear = () => {
    setInput("");
    toast.info("Cleared");
  };

  const handleCopy = (text: string, title: string) => {
    if (!text) return;
    navigator.clipboard.writeText(text);
    toast.success(`Copied ${title}`);
  };

  return (
    <div className="flex h-full flex-col overflow-hidden bg-[#0F172A] relative">
      <div className="flex-shrink-0 flex items-center gap-2 overflow-x-auto p-2 border-b border-white/5 bg-[#1E293B]/60 backdrop-blur-md px-6 z-30">
        <div className="flex items-center gap-2 text-[#F8FAFC]">
          <KeyRound className="w-4 h-4 text-[#22C55E]" />
          <span className="text-sm font-medium">JWT Decoder</span>
        </div>
      </div>

      <div className="flex flex-1 flex-col lg:flex-row overflow-hidden relative">
        {/* Left Input */}
        <div className="flex flex-1 flex-col relative group">
          <div className="flex h-10 items-center justify-between bg-[#1E293B]/20 px-4 border-b border-white/5">
            <div className="flex items-center gap-3">
              <span className="text-xs font-bold tracking-wider text-[#F8FAFC]/50 uppercase">Encoded Token</span>
              {error && (
                <span className="text-xs text-red-400 font-medium truncate max-w-[200px]" title={error}>
                  {error}
                </span>
              )}
            </div>
            <div className="flex items-center gap-1 opacity-50 group-hover:opacity-100 transition-opacity">
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button variant="ghost" size="icon" className="h-7 w-7 text-[#F8FAFC]/70 hover:text-red-400 hover:bg-red-400/20" onClick={handleClear}>
                    <Trash2 className="h-3 w-3" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent side="top" className="bg-[#1E293B] border-white/10 text-[#F8FAFC] text-xs">Clear (Trash)</TooltipContent>
              </Tooltip>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button variant="ghost" size="icon" className="h-7 w-7 text-[#F8FAFC]/70 hover:text-white hover:bg-white/10" onClick={() => handleCopy(input, "Token")}>
                    <Copy className="h-3 w-3" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent side="top" className="bg-[#1E293B] border-white/10 text-[#F8FAFC] text-xs">Copy Input</TooltipContent>
              </Tooltip>
            </div>
          </div>
          <div className="flex-1 relative bg-black/20 p-4 overflow-auto">
            <textarea
              className="w-full h-full bg-transparent text-[#F8FAFC] placeholder-white/20 resize-none outline-none font-mono text-sm leading-relaxed"
              placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              spellCheck="false"
            />
          </div>
        </div>

        {/* Right Output */}
        <div className="flex flex-1 flex-col relative border-t lg:border-t-0 lg:border-l border-white/5 bg-black/10 overflow-hidden divide-y divide-white/5">
          
          {/* Header */}
          <div className="flex flex-col h-1/3 min-h-[150px]">
            <div className="flex h-10 items-center justify-between bg-[#1E293B]/20 px-4 group">
               <span className="text-xs font-bold tracking-wider text-red-500 uppercase drop-shadow-[0_0_8px_rgba(239,68,68,0.5)]">Header: Algorithm & Token Type</span>
               <div className="opacity-0 group-hover:opacity-100 transition-opacity">
                 <Button variant="ghost" size="icon" className="h-7 w-7 text-[#F8FAFC]/70 hover:text-red-400 hover:bg-red-400/20" onClick={() => handleCopy(header, "Header")}>
                    <Copy className="h-3 w-3" />
                  </Button>
               </div>
            </div>
            <div className="flex-1 relative">
              <Editor
                height="100%"
                defaultLanguage="json"
                theme="vs-dark"
                value={header}
                options={{ readOnly: true, minimap: { enabled: false }, fontSize: 13, scrollBeyondLastLine: false, padding: { top: 10, bottom: 10 }, domReadOnly: true, lineNumbersMinChars: 3 }}
              />
            </div>
          </div>

          {/* Payload */}
          <div className="flex flex-col flex-1 h-1/3 min-h-[200px]">
            <div className="flex h-10 items-center justify-between bg-[#1E293B]/20 px-4 group">
               <span className="text-xs font-bold tracking-wider text-purple-500 uppercase drop-shadow-[0_0_8px_rgba(168,85,247,0.5)]">Payload: Data</span>
               <div className="opacity-0 group-hover:opacity-100 transition-opacity">
                 <Button variant="ghost" size="icon" className="h-7 w-7 text-[#F8FAFC]/70 hover:text-purple-400 hover:bg-purple-400/20" onClick={() => handleCopy(payload, "Payload")}>
                    <Copy className="h-3 w-3" />
                  </Button>
               </div>
            </div>
            <div className="flex-1 relative">
              <Editor
                height="100%"
                defaultLanguage="json"
                theme="vs-dark"
                value={payload}
                options={{ readOnly: true, minimap: { enabled: false }, fontSize: 13, scrollBeyondLastLine: false, padding: { top: 10, bottom: 10 }, domReadOnly: true, lineNumbersMinChars: 3 }}
              />
            </div>
          </div>

          {/* Signature */}
          <div className="flex flex-col h-[100px] flex-shrink-0">
             <div className="flex h-8 items-center justify-between bg-[#1E293B]/20 px-4 group border-b border-white/5">
               <span className="text-xs font-bold tracking-wider text-cyan-500 uppercase drop-shadow-[0_0_8px_rgba(6,182,212,0.5)]">Signature</span>
               <div className="opacity-0 group-hover:opacity-100 transition-opacity">
                 <Button variant="ghost" size="icon" className="h-6 w-6 text-[#F8FAFC]/70 hover:text-cyan-400 hover:bg-cyan-400/20" onClick={() => handleCopy(signature, "Signature")}>
                    <Copy className="h-3 w-3" />
                  </Button>
               </div>
            </div>
            <div className="flex-1 p-3 bg-black/20 font-mono text-xs text-cyan-500 break-all overflow-y-auto">
              {signature || "No signature"}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
