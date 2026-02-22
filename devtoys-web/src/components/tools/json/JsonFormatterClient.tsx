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
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";

export function JsonFormatterClient() {
  const [input, setInput] = React.useState<string>("");
  const [output, setOutput] = React.useState<string>("");
  const [error, setError] = React.useState<string | null>(null);
  const [indentation, setIndentation] = React.useState<string>("2");

  // Format JSON
  const handleFormat = React.useCallback(() => {
    if (!input.trim()) return;
    try {
      const parsed = JSON.parse(input);
      const formatted = JSON.stringify(parsed, null, Number(indentation));
      setOutput(formatted);
      setError(null);
      toast.success("JSON Formatted");
    } catch (err) {
      setError((err as Error).message);
      toast.error("Invalid JSON");
    }
  }, [input, indentation]);

  // Minify JSON
  const handleMinify = React.useCallback(() => {
    if (!input.trim()) return;
    try {
      const parsed = JSON.parse(input);
      const minified = JSON.stringify(parsed);
      setOutput(minified);
      setError(null);
      toast.success("JSON Minified");
    } catch (err) {
      setError((err as Error).message);
      toast.error("Invalid JSON");
    }
  }, [input]);

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
    const blob = new Blob([output], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "formatted.json";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast.success("File downloaded");
  };

  // Auto-format on input change (optional, can be toggleable)
  React.useEffect(() => {
    if (!input.trim()) {
      setOutput("");
      setError(null);
      return;
    }
    // Simple validation on type
    try {
      JSON.parse(input);
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
  }, [input]);

  return (
    <div className="flex h-[calc(100vh-3.5rem)] flex-col lg:flex-row overflow-hidden">
      {/* Input Panel */}
      <div className="flex flex-1 flex-col border-r border-border/50">
        <div className="flex h-12 items-center justify-between border-b border-border/50 bg-muted/30 px-4">
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="bg-background">
              Input
            </Badge>
            {error && (
              <span className="text-xs text-red-500 font-medium truncate max-w-[200px]">
                {error}
              </span>
            )}
          </div>
          <div className="flex items-center gap-1">
            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8"
              onClick={handleClear}
              title="Clear"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8"
              onClick={() => handleCopy(input)}
              title="Copy Input"
            >
              <Copy className="h-4 w-4" />
            </Button>
          </div>
        </div>
        <div className="flex-1 relative">
          <Editor
            height="100%"
            defaultLanguage="json"
            value={input}
            onChange={(value) => setInput(value || "")}
            options={{
              minimap: { enabled: false },
              fontSize: 14,
              wordWrap: "on",
              automaticLayout: true,
              scrollBeyondLastLine: false,
              padding: { top: 16, bottom: 16 },
            }}
          />
        </div>
      </div>

      {/* Toolbar (Middle on Desktop, Top on Mobile - handled by flex-col lg:flex-row) */}
      <div className="flex h-14 lg:h-auto lg:w-14 flex-row lg:flex-col items-center justify-center gap-2 border-b lg:border-b-0 lg:border-r border-border/50 bg-muted/10 p-2 z-10">
        <Button
          variant="secondary"
          size="icon"
          onClick={handleFormat}
          disabled={!!error || !input}
          title="Format"
          className="rounded-xl shadow-sm"
        >
          <AlignLeft className="h-5 w-5" />
        </Button>
        <Button
          variant="secondary"
          size="icon"
          onClick={handleMinify}
          disabled={!!error || !input}
          title="Minify"
          className="rounded-xl shadow-sm"
        >
          <Minimize2 className="h-5 w-5" />
        </Button>
      </div>

      {/* Output Panel */}
      <div className="flex flex-1 flex-col bg-muted/5">
        <div className="flex h-12 items-center justify-between border-b border-border/50 bg-muted/30 px-4">
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="bg-background text-primary border-primary/20">
              Output
            </Badge>
            <Select value={indentation} onValueChange={setIndentation}>
              <SelectTrigger className="h-7 w-[100px] text-xs">
                <SelectValue placeholder="Indent" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="2">2 Spaces</SelectItem>
                <SelectItem value="4">4 Spaces</SelectItem>
                <SelectItem value="\t">Tab</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="flex items-center gap-1">
             <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8"
              onClick={() => handleCopy(output)}
              disabled={!output}
              title="Copy Output"
            >
              <Copy className="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8"
              onClick={handleDownload}
              disabled={!output}
              title="Download"
            >
              <Download className="h-4 w-4" />
            </Button>
          </div>
        </div>
        <div className="flex-1 relative">
          <Editor
            height="100%"
            defaultLanguage="json"
            value={output}
            options={{
              readOnly: true,
              minimap: { enabled: false },
              fontSize: 14,
              wordWrap: "on",
              automaticLayout: true,
              scrollBeyondLastLine: false,
              padding: { top: 16, bottom: 16 },
              domReadOnly: true,
            }}
          />
        </div>
      </div>
      
      {/* Right Sidebar (Ads) */}
      <div className="hidden w-[300px] flex-col border-l border-border/50 bg-muted/10 p-4 xl:flex">
         <div className="rounded-lg border border-border/50 bg-background/50 p-4 text-center">
            <span className="text-xs text-muted-foreground">Sponsor</span>
            <div className="mt-2 flex h-[250px] items-center justify-center rounded bg-muted/20">
              <span className="text-xs text-muted-foreground/50">Ad Space 300x250</span>
            </div>
         </div>
      </div>
    </div>
  );
}
