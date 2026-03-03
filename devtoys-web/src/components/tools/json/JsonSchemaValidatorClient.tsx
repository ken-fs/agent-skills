"use client";

import * as React from "react";
import Editor from "@monaco-editor/react";
import { toast } from "sonner";
import { Play, Trash2, ShieldCheck, Copy } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import Ajv from "ajv";
import addFormats from "ajv-formats";

export function JsonSchemaValidatorClient() {
  const [schemaInput, setSchemaInput] = React.useState<string>("{\n  \"type\": \"object\",\n  \"properties\": {\n    \"name\": { \"type\": \"string\" }\n  },\n  \"required\": [\"name\"]\n}");
  const [dataInput, setDataInput] = React.useState<string>("{\n  \"name\": \"DevToys\"\n}");
  const [validationResult, setValidationResult] = React.useState<{ valid: boolean; message: string; errors?: any[] } | null>(null);

  const handleValidate = () => {
    if (!schemaInput.trim() || !dataInput.trim()) {
      toast.error("Both Schema and Data are required.");
      return;
    }

    try {
      const schema = JSON.parse(schemaInput);
      const data = JSON.parse(dataInput);

      const ajv = new Ajv({ allErrors: true, strict: false });
      addFormats(ajv);

      let validate;
      try {
        validate = ajv.compile(schema);
      } catch (compileError) {
        setValidationResult({
          valid: false,
          message: "Invalid JSON Schema",
          errors: [{ message: (compileError as Error).message }],
        });
        toast.error("Invalid JSON Schema structure.");
        return;
      }

      const valid = validate(data);
      if (valid) {
        setValidationResult({ valid: true, message: "Valid JSON! The data complies with the schema." });
        toast.success("JSON is valid against the schema");
      } else {
        setValidationResult({
          valid: false,
          message: "Validation Failed",
          errors: validate.errors || [],
        });
        toast.error("JSON data does not match the schema");
      }
    } catch (parseError) {
      setValidationResult({
        valid: false,
        message: "Parsing Error",
        errors: [{ message: "Ensure both Schema and Data are valid JSON strings before validating. " + (parseError as Error).message }],
      });
      toast.error("Invalid JSON format in input fields");
    }
  };

  const handleClear = () => {
    setSchemaInput("");
    setDataInput("");
    setValidationResult(null);
    toast.info("Cleared");
  };

  const loadExample = () => {
    setSchemaInput(JSON.stringify({
      "$schema": "http://json-schema.org/draft-07/schema#",
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "format": "uuid"
        },
        "price": {
          "type": "number",
          "minimum": 0
        }
      },
      "required": ["id", "price"]
    }, null, 2));
    
    setDataInput(JSON.stringify({
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "price": 29.99
    }, null, 2));

    setValidationResult(null);
    toast.success("Example Loaded");
  };

  return (
    <div className="flex h-full flex-col overflow-hidden bg-[#0F172A] relative">
      <div className="flex-shrink-0 flex justify-between items-center overflow-x-auto p-2 border-b border-white/5 bg-[#1E293B]/60 backdrop-blur-md px-6 z-30">
        <div className="flex items-center gap-2 text-[#F8FAFC]">
          <ShieldCheck className="w-4 h-4 text-[#22C55E]" />
          <span className="text-sm font-medium">JSON Schema Validator</span>
        </div>
        <div className="flex items-center gap-2">
           <Button variant="secondary" size="sm" onClick={loadExample} className="text-xs font-semibold bg-white/5 text-[#F8FAFC] hover:bg-white/10 border border-white/10">
            Load Example
          </Button>
          <Button variant="secondary" size="sm" onClick={handleClear} className="text-xs font-semibold bg-red-500/10 text-red-500 hover:bg-red-500/20 border border-red-500/20">
            <Trash2 className="w-3 h-3 mr-1" /> Clear
          </Button>
          <Button size="sm" onClick={handleValidate} className="text-xs font-bold bg-[#22C55E] hover:bg-[#22C55E]/90 text-black border border-[#22C55E] shadow-[0_0_15px_rgba(34,197,94,0.3)]">
            <Play className="w-3 h-3 mr-1" /> Validate
          </Button>
        </div>
      </div>

      <div className="flex flex-1 flex-col lg:flex-row overflow-hidden relative">
        {/* Schema Input */}
        <div className="flex flex-col flex-1 relative group">
          <div className="flex h-10 items-center justify-between bg-[#1E293B]/20 px-4 border-b border-white/5">
            <span className="text-xs font-bold tracking-wider text-purple-500 uppercase drop-shadow-[0_0_8px_rgba(168,85,247,0.5)]">JSON Schema</span>
            <Tooltip>
               <TooltipTrigger asChild>
                 <Button variant="ghost" size="icon" className="h-7 w-7 text-[#F8FAFC]/70 hover:text-white hover:bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity" onClick={() => { navigator.clipboard.writeText(schemaInput); toast.success("Schema copied"); }}>
                    <Copy className="h-3 w-3" />
                  </Button>
               </TooltipTrigger>
               <TooltipContent side="top" className="bg-[#1E293B] border-white/10 text-[#F8FAFC] text-xs">Copy Schema</TooltipContent>
            </Tooltip>
          </div>
          <div className="flex-1 relative">
            <Editor
              height="100%"
              defaultLanguage="json"
              theme="vs-dark"
              value={schemaInput}
              onChange={(val) => setSchemaInput(val || "")}
              options={{ minimap: { enabled: false }, fontSize: 13, fontFamily: "var(--font-geist-mono)", wordWrap: "on", padding: { top: 16, bottom: 16 } }}
            />
          </div>
        </div>

        {/* Data Input */}
        <div className="flex flex-col flex-1 relative border-t lg:border-t-0 lg:border-l border-white/5 group">
          <div className="flex h-10 items-center justify-between bg-[#1E293B]/20 px-4 border-b border-white/5">
            <span className="text-xs font-bold tracking-wider text-cyan-500 uppercase drop-shadow-[0_0_8px_rgba(6,182,212,0.5)]">JSON Data</span>
            <Tooltip>
               <TooltipTrigger asChild>
                 <Button variant="ghost" size="icon" className="h-7 w-7 text-[#F8FAFC]/70 hover:text-white hover:bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity" onClick={() => { navigator.clipboard.writeText(dataInput); toast.success("Data copied"); }}>
                    <Copy className="h-3 w-3" />
                  </Button>
               </TooltipTrigger>
               <TooltipContent side="top" className="bg-[#1E293B] border-white/10 text-[#F8FAFC] text-xs">Copy Data</TooltipContent>
            </Tooltip>
          </div>
          <div className="flex-1 relative">
            <Editor
              height="100%"
              defaultLanguage="json"
              theme="vs-dark"
              value={dataInput}
              onChange={(val) => setDataInput(val || "")}
              options={{ minimap: { enabled: false }, fontSize: 13, fontFamily: "var(--font-geist-mono)", wordWrap: "on", padding: { top: 16, bottom: 16 } }}
            />
          </div>
        </div>
      </div>

      {/* Results Panel */}
      <div className={`flex-shrink-0 transition-all duration-300 ${validationResult ? "h-[200px]" : "h-0"} overflow-hidden bg-black/40 border-t border-white/5`}>
        {validationResult && (
          <div className="flex flex-col h-full w-full p-4 overflow-y-auto">
            <h3 className={`text-sm font-bold mb-2 flex items-center gap-2 ${validationResult.valid ? "text-[#22C55E]" : "text-red-500"}`}>
              {validationResult.valid ? <ShieldCheck className="w-4 h-4" /> : <ShieldCheck className="w-4 h-4 opacity-50" />}
              {validationResult.message}
            </h3>
            
            {!validationResult.valid && validationResult.errors && (
              <div className="flex-1 bg-red-500/5 border border-red-500/20 rounded-md p-3 text-sm font-mono text-red-200 overflow-y-auto">
                <ul className="list-disc pl-5 space-y-1">
                  {validationResult.errors.map((err, i) => (
                    <li key={i}>
                      {err.instancePath && <span className="font-bold text-red-400">{err.instancePath}</span>}
                      {err.instancePath ? ": " : ""}
                      {err.message}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            {validationResult.valid && (
               <div className="flex-1 bg-[#22C55E]/5 border border-[#22C55E]/20 rounded-md p-3 text-sm font-mono text-[#22C55E] flex items-center justify-center">
                 ✓ Data structurally validates against the provided schema.
               </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
