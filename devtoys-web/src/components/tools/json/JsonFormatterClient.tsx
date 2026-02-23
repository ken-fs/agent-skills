"use client";

import * as React from "react";
import Editor from "@monaco-editor/react";
import { toast } from "sonner";
import {
  AlignLeft,
  Copy,
  Download,
  Minimize2,
  Trash2,
  ListTree,
  FileCode2,
  ArrowRightLeft,
  Wrench,
  Link as LinkIcon,
  BookOpen,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuLabel,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu";
import { Badge } from "@/components/ui/badge";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { jsonUtils } from "./json-utils";

export function JsonFormatterClient() {
  const [input, setInput] = React.useState<string>("");
  const [output, setOutput] = React.useState<string>("");
  const [error, setError] = React.useState<string | null>(null);
  const [indentation, setIndentation] = React.useState<string>("2");
  const [isMinified, setIsMinified] = React.useState<boolean>(false);

  // A generalized handler for transformations
  const handleTransform = (
    transformFn: (val: string, indent?: string | number) => string,
    successMsg: string,
    isInputAlreadyJson: boolean = true
  ) => {
    if (!input.trim()) return;
    try {
      if (isInputAlreadyJson) {
        // Validate it's JSON if required by the operation
        JSON.parse(input);
      }
      const result = transformFn(input, indentation === "\\t" ? "\t" : Number(indentation));
      setOutput(result);
    } catch (err) {
      setError((err as Error).message);
      toast.error(`Error: ${(err as Error).message}`, {
        className: "!bg-red-500 !text-white !border-red-600",
      });
    }
  };

  // Specialized operations
  const handleFormat = () => {
    setIsMinified(false);
    handleTransform((val, ind) => jsonUtils.format(val, ind), "JSON Formatted");
  };
  
  const handleMinify = () => {
    if (isMinified) {
      setIsMinified(false);
      handleTransform((val, ind) => jsonUtils.format(val, ind), "JSON Formatted (Minify Disabled)");
    } else {
      setIsMinified(true);
      handleTransform(jsonUtils.minify, "JSON Minified");
    }
  };
  
  const handleEscape = () => handleTransform(jsonUtils.escape, "JSON Escaped", false);
  const handleUnescape = () => handleTransform(jsonUtils.unescape, "JSON Unescaped", false);
  
  const handleUnicodeDecode = () => handleTransform(jsonUtils.unicodeDecode, "Unicode Decoded", false);
  const handleUnicodeEncode = () => handleTransform(jsonUtils.unicodeEncode, "Unicode Encoded", false);
  
  const handleSortAsc = () => handleTransform(jsonUtils.sortAsc, "Keys Sorted (Asc)");
  const handleSortDesc = () => handleTransform(jsonUtils.sortDesc, "Keys Sorted (Desc)");

  const handleJsonToXml = () => handleTransform(jsonUtils.jsonToXml, "Converted JSON to XML");
  const handleXmlToJson = () => handleTransform(jsonUtils.xmlToJson, "Converted XML to JSON", false);
  
  const handleJsonToYaml = () => handleTransform(jsonUtils.jsonToYaml, "Converted JSON to YAML");
  const handleYamlToJson = () => handleTransform(jsonUtils.yamlToJson, "Converted YAML to JSON", false);
  
  const handleJsonToGet = () => handleTransform(jsonUtils.jsonToGet, "Converted JSON to URL Params");
  const handleGetToJson = () => handleTransform(jsonUtils.getToJson, "Converted URL Params to JSON", false);

  // Load Example
  const handleLoadExample = () => {
    const exampleJson = {
      project: "DevToys Web",
      version: "1.0.0",
      description: "Developer Tools Reimagined",
      features: [
        "JSON Formatting",
        "Image Compression",
        "Encoding & Decoding"
      ],
      active: true,
      metadata: {
        theme: "dark",
        color: "#22C55E"
      }
    };
    setInput(JSON.stringify(exampleJson, null, 2));
    toast.success("Loaded English Example");
  };

  // Copy to Clipboard
  const handleCopy = (text: string) => {
    if (!text) return;
    navigator.clipboard.writeText(text);
    toast.success("Copied to clipboard");
  };

  // Clear All
  const handleClear = () => {
    setInput("");
    setOutput("");
    setError(null);
    toast.info("Cleared");
  };

  // Download File
  const handleDownload = () => {
    if (!output) return;
    const blob = new Blob([output], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "devtoys-output.txt";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast.success("File downloaded");
  };

  // Auto-format on input change
  React.useEffect(() => {
    if (!input.trim()) {
      setOutput("");
      setError(null);
      return;
    }
    try {
      if (isMinified) {
        setOutput(jsonUtils.minify(input));
      } else {
        const formatted = jsonUtils.format(input, indentation === "\\t" ? "\t" : Number(indentation));
        setOutput(formatted);
      }
      setError(null);
    } catch (err) {
      // Don't auto-clear output on invalid JSON, just show error
      setError((err as Error).message);
    }
  }, [input, indentation, isMinified]);

  return (
    <div className="flex h-full flex-col overflow-hidden bg-[#0F172A] relative">
      
      {/* Universal Action Toolbar (JSON.cn equivalent features) */}
      <div className="flex-shrink-0 flex items-center gap-2 overflow-x-auto p-2 border-b border-white/5 bg-[#1E293B]/60 backdrop-blur-md px-6 z-30 hide-scrollbar">
        <Button variant="secondary" size="sm" onClick={handleFormat} className="text-xs font-semibold bg-[#22C55E]/10 text-[#22C55E] hover:bg-[#22C55E]/20 border border-[#22C55E]/20">
          <AlignLeft className="w-3 h-3 mr-1"/> Format
        </Button>
        <Button 
          variant="secondary" 
          size="sm" 
          onClick={handleMinify} 
          className={`text-xs font-semibold border transition-all ${
            isMinified 
              ? "bg-[#22C55E]/10 text-[#22C55E] hover:bg-[#22C55E]/20 border-[#22C55E]/30"
              : "bg-white/5 text-[#F8FAFC] hover:bg-white/10 border-white/10"
          }`}
        >
          <Minimize2 className="w-3 h-3 mr-1"/> {isMinified ? "Unminify" : "Minify"}
        </Button>

        <div className="h-4 w-px bg-white/10 mx-1"></div>

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="secondary" size="sm" className="text-xs font-semibold bg-white/5 text-[#F8FAFC] hover:bg-white/10 border border-white/10">
              <FileCode2 className="w-3 h-3 mr-1"/> Encode / Decode
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="bg-[#1E293B] border-white/10 text-[#F8FAFC]">
            <DropdownMenuLabel>String Overrides</DropdownMenuLabel>
            <DropdownMenuItem onClick={handleEscape} className="cursor-pointer focus:bg-[#22C55E]/20">Escape</DropdownMenuItem>
            <DropdownMenuItem onClick={handleUnescape} className="cursor-pointer focus:bg-[#22C55E]/20">Unescape</DropdownMenuItem>
            <DropdownMenuSeparator className="bg-white/10"/>
            <DropdownMenuLabel>Unicode</DropdownMenuLabel>
            <DropdownMenuItem onClick={handleUnicodeDecode} className="cursor-pointer focus:bg-[#22C55E]/20">Unicode Decode</DropdownMenuItem>
            <DropdownMenuItem onClick={handleUnicodeEncode} className="cursor-pointer focus:bg-[#22C55E]/20">Unicode Encode</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="secondary" size="sm" className="text-xs font-semibold bg-white/5 text-[#F8FAFC] hover:bg-white/10 border border-white/10">
              <ListTree className="w-3 h-3 mr-1"/> Sort Keys
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="bg-[#1E293B] border-white/10 text-[#F8FAFC]">
            <DropdownMenuItem onClick={handleSortAsc} className="cursor-pointer focus:bg-[#22C55E]/20">Ascending (A-Z)</DropdownMenuItem>
            <DropdownMenuItem onClick={handleSortDesc} className="cursor-pointer focus:bg-[#22C55E]/20">Descending (Z-A)</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>

        <div className="h-4 w-px bg-white/10 mx-1"></div>

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="secondary" size="sm" className="text-xs font-semibold bg-[#3b82f6]/10 text-[#60a5fa] hover:bg-[#3b82f6]/20 border border-[#3b82f6]/20">
              <ArrowRightLeft className="w-3 h-3 mr-1"/> Convert
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="bg-[#1E293B] border-white/10 text-[#F8FAFC]">
            <DropdownMenuLabel>JSON to...</DropdownMenuLabel>
            <DropdownMenuItem onClick={handleJsonToXml} className="cursor-pointer focus:bg-[#22C55E]/20">JSON → XML</DropdownMenuItem>
            <DropdownMenuItem onClick={handleJsonToYaml} className="cursor-pointer focus:bg-[#22C55E]/20">JSON → YAML</DropdownMenuItem>
            <DropdownMenuItem onClick={handleJsonToGet} className="cursor-pointer focus:bg-[#22C55E]/20">JSON → URL Params</DropdownMenuItem>
            <DropdownMenuSeparator className="bg-white/10"/>
            <DropdownMenuLabel>Reverse to JSON</DropdownMenuLabel>
            <DropdownMenuItem onClick={handleXmlToJson} className="cursor-pointer focus:bg-[#22C55E]/20">XML → JSON</DropdownMenuItem>
            <DropdownMenuItem onClick={handleYamlToJson} className="cursor-pointer focus:bg-[#22C55E]/20">YAML → JSON</DropdownMenuItem>
            <DropdownMenuItem onClick={handleGetToJson} className="cursor-pointer focus:bg-[#22C55E]/20">URL Params → JSON</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      <div className="flex flex-1 flex-col lg:flex-row overflow-hidden relative">
        {/* Input Panel */}
        <div className="flex flex-1 flex-col relative group">
          <div className="flex h-10 items-center justify-between bg-[#1E293B]/20 px-4 border-b border-white/5">
            <div className="flex items-center gap-3">
              <span className="text-xs font-bold tracking-wider text-[#F8FAFC]/50 uppercase">Input</span>
              {error && (
                <span className="text-xs text-red-400 font-medium truncate max-w-[200px]">
                  {error}
                </span>
              )}
            </div>
            <div className="flex items-center gap-1 opacity-50 group-hover:opacity-100 transition-opacity">
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-7 w-7 text-[#F8FAFC]/70 hover:text-[#22C55E] hover:bg-[#22C55E]/20"
                    onClick={handleLoadExample}
                  >
                    <BookOpen className="h-3 w-3" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent side="top" className="bg-[#1E293B] border-white/10 text-[#F8FAFC] text-xs">Load Example</TooltipContent>
              </Tooltip>

              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-7 w-7 text-[#F8FAFC]/70 hover:text-red-400 hover:bg-red-400/20"
                    onClick={handleClear}
                  >
                    <Trash2 className="h-3 w-3" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent side="top" className="bg-[#1E293B] border-white/10 text-[#F8FAFC] text-xs">Clear (Trash)</TooltipContent>
              </Tooltip>

              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-7 w-7 text-[#F8FAFC]/70 hover:text-white hover:bg-white/10"
                    onClick={() => handleCopy(input)}
                  >
                    <Copy className="h-3 w-3" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent side="top" className="bg-[#1E293B] border-white/10 text-[#F8FAFC] text-xs">Copy Input</TooltipContent>
              </Tooltip>
            </div>
          </div>
          <div className="flex-1 relative">
            <Editor
              height="100%"
              defaultLanguage="json"
              theme="vs-dark"
              value={input}
              onChange={(value) => setInput(value || "")}
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                fontFamily: "var(--font-geist-mono)",
                wordWrap: "on",
                automaticLayout: true,
                scrollBeyondLastLine: false,
                padding: { top: 16, bottom: 16 },
                lineNumbersMinChars: 3,
              }}
            />
          </div>
        </div>

        {/* Output Panel */}
        <div className="flex flex-1 flex-col relative group border-t lg:border-t-0 lg:border-l border-white/5">
          <div className="flex h-10 items-center justify-between bg-[#1E293B]/20 px-4 border-b border-white/5">
            <div className="flex items-center gap-4">
              <span className="text-xs font-bold tracking-wider text-[#22C55E] uppercase drop-shadow-[0_0_8px_rgba(34,197,94,0.5)]">Output</span>
              <Select value={indentation} onValueChange={setIndentation}>
                <SelectTrigger className="h-6 w-[90px] text-[11px] bg-black/20 border-white/10 text-[#F8FAFC]/80 focus:ring-1 focus:ring-[#22C55E]">
                  <SelectValue placeholder="Indent" />
                </SelectTrigger>
                <SelectContent className="bg-[#1E293B] border-white/10 text-[#F8FAFC]">
                  <SelectItem value="2" className="focus:bg-[#22C55E]/20 focus:text-white text-xs">2 Spaces</SelectItem>
                  <SelectItem value="4" className="focus:bg-[#22C55E]/20 focus:text-white text-xs">4 Spaces</SelectItem>
                  <SelectItem value="\t" className="focus:bg-[#22C55E]/20 focus:text-white text-xs">Tab</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="flex items-center gap-1 opacity-50 group-hover:opacity-100 transition-opacity">
              <Button
                variant="ghost"
                size="icon"
                className="h-7 w-7 text-[#F8FAFC]/70 hover:text-[#22C55E] hover:bg-[#22C55E]/20"
                onClick={() => handleCopy(output)}
                disabled={!output}
                title="Copy Output"
              >
                <Copy className="h-3 w-3" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                className="h-7 w-7 text-[#F8FAFC]/70 hover:text-cyan-400 hover:bg-cyan-400/20"
                onClick={handleDownload}
                disabled={!output}
                title="Download"
              >
                <Download className="h-3 w-3" />
              </Button>
            </div>
          </div>
          <div className="flex-1 relative">
            <Editor
              height="100%"
              defaultLanguage="json"
              theme="vs-dark"
              value={output}
              options={{
                readOnly: true,
                minimap: { enabled: false },
                fontSize: 14,
                fontFamily: "var(--font-geist-mono)",
                wordWrap: "on",
                automaticLayout: true,
                scrollBeyondLastLine: false,
                padding: { top: 16, bottom: 16 },
                domReadOnly: true,
                lineNumbersMinChars: 3,
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
