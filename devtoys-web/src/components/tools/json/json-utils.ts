import yaml from "yaml";
import { XMLParser, XMLBuilder } from "fast-xml-parser";

export const jsonUtils = {
  format: (input: string, indent: number | string = 2): string => {
    return JSON.stringify(JSON.parse(input), null, Number(indent));
  },
  minify: (input: string): string => {
    return JSON.stringify(JSON.parse(input));
  },
  escape: (input: string): string => {
    // Escapes a JSON string (turns {"a":"b"} into \{\"a\":\"b\"\} essentially)
    // Often utilized for placing JSON inside another JSON string payload.
    const str = JSON.stringify(input);
    if (str.startsWith('"') && str.endsWith('"')) {
      return str.substring(1, str.length - 1);
    }
    return str;
  },
  unescape: (input: string): string => {
    try {
      const parsed = JSON.parse(`"${input}"`);
      // It might be double stringified, let's try to format it if it's JSON
      if (typeof parsed === 'string' && (parsed.startsWith('{') || parsed.startsWith('['))) {
         return JSON.stringify(JSON.parse(parsed), null, 2);
      }
      return parsed;
    } catch {
      return input.replace(/\\"/g, '"').replace(/\\\\/g, "\\");
    }
  },
  unicodeDecode: (input: string): string => {
    return unescape(input.replace(/\\u/g, "%u"));
  },
  unicodeEncode: (input: string): string => {
    return input.replace(/[\u007F-\uFFFF]/g, function (chr) {
      return "\\u" + ("0000" + chr.charCodeAt(0).toString(16)).slice(-4);
    });
  },
  sortAsc: (input: string): string => {
    const obj = JSON.parse(input);
    const sortObject = (o: any): any => {
      if (Array.isArray(o)) return o.map(sortObject);
      if (o !== null && typeof o === "object") {
        return Object.keys(o)
          .sort()
          .reduce((acc, key) => {
            acc[key] = sortObject(o[key]);
            return acc;
          }, {} as any);
      }
      return o;
    };
    return JSON.stringify(sortObject(obj), null, 2);
  },
  sortDesc: (input: string): string => {
    const obj = JSON.parse(input);
    const sortObject = (o: any): any => {
      if (Array.isArray(o)) return o.map(sortObject);
      if (o !== null && typeof o === "object") {
        return Object.keys(o)
          .sort()
          .reverse()
          .reduce((acc, key) => {
            acc[key] = sortObject(o[key]);
            return acc;
          }, {} as any);
      }
      return o;
    };
    return JSON.stringify(sortObject(obj), null, 2);
  },
  jsonToXml: (input: string): string => {
    const obj = JSON.parse(input);
    const builder = new XMLBuilder({ ignoreAttributes: false, format: true });
    return builder.build(obj);
  },
  xmlToJson: (input: string): string => {
    const parser = new XMLParser({ ignoreAttributes: false });
    const obj = parser.parse(input);
    return JSON.stringify(obj, null, 2);
  },
  jsonToYaml: (input: string): string => {
    const obj = JSON.parse(input);
    return yaml.stringify(obj);
  },
  yamlToJson: (input: string): string => {
    const obj = yaml.parse(input);
    return JSON.stringify(obj, null, 2);
  },
  jsonToGet: (input: string): string => {
    const obj = JSON.parse(input);
    if (typeof obj !== "object" || Array.isArray(obj)) {
      throw new Error("Require a flat JSON object for GET params");
    }
    return new URLSearchParams(obj as any).toString();
  },
  getToJson: (input: string): string => {
    const params = new URLSearchParams(input);
    const obj: Record<string, string> = {};
    params.forEach((value, key) => {
      obj[key] = value;
    });
    return JSON.stringify(obj, null, 2);
  },
};
