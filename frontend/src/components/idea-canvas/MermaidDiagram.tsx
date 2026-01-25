// frontend/src/components/idea-canvas/MermaidDiagram.tsx

"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import mermaid from "mermaid";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

interface MermaidDiagramProps {
  code: string;
  title?: string;
  onElementClick?: (elementId: string) => void;
  highlightedElement?: string;
}

export function MermaidDiagram({
  code,
  title,
  onElementClick,
  highlightedElement,
}: MermaidDiagramProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const fullscreenContainerRef = useRef<HTMLDivElement>(null);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);

  useEffect(() => {
    mermaid.initialize({
      startOnLoad: false,
      theme: "base",
      securityLevel: "loose",
      fontFamily: "inherit",
      themeVariables: {
        primaryColor: "#f59e0b",
        primaryTextColor: "#111827",
        primaryBorderColor: "#d97706",
        lineColor: "#9ca3af",
        secondaryColor: "#ecfeff",
        tertiaryColor: "#fff7ed",
        fontFamily: "inherit",
      },
    });
  }, []);

  const sanitizeMermaidCode = useCallback((raw: string): string => {
    const normalized = raw.replace(/\r\n/g, "\n").trim();
    if (!normalized) return normalized;

    const firstLine = normalized.split("\n")[0].trim();
    const hasKnownPrefix = /^(flowchart|graph|sequenceDiagram|classDiagram|stateDiagram|erDiagram|gantt|pie|journey)\b/i.test(firstLine);
    let nextCode = hasKnownPrefix ? normalized : `flowchart TD\n${normalized}`;

    const flowPrefix = nextCode.split("\n")[0].trim();
    const isFlowchart = /^(flowchart|graph)\b/i.test(flowPrefix);

    if (!isFlowchart) return nextCode;

    // Clean up common syntax pitfalls from LLM output.
    nextCode = nextCode
      .replace(/[–—]/g, "-")
      .replace(/--\s*>/g, "-->")
      .replace(/\s+\|\s+/g, " - ")
      .replace(/^\s*[-*]\s+/gm, "    ");

    const sanitizeLabel = (label: string) =>
      label
        .replace(/[()[\]{}]/g, "")
        .replace(/[|]/g, "-")
        .replace(/[,;:]/g, " ")
        .replace(/\s+/g, " ")
        .trim()
        .slice(0, 36);

    nextCode = nextCode.replace(/\[([^\]]+)\]/g, (_match, label) => {
      const cleaned = sanitizeLabel(label);
      return `[${cleaned || "Node"}]`;
    });

    // Ensure node ids are simple tokens (no spaces or punctuation).
    const idMap = new Map<string, string>();
    const idRegex = /(^|\s)([A-Za-z0-9][A-Za-z0-9 _-]*)\s*\[[^\]]+\]/gm;
    let match: RegExpExecArray | null;
    let idCounter = 1;
    while ((match = idRegex.exec(nextCode)) !== null) {
      const original = match[2].trim();
      if (!original || idMap.has(original)) continue;
      const safe = original.replace(/[^A-Za-z0-9_]/g, "_");
      const safeId = safe || `N${idCounter++}`;
      idMap.set(original, safeId);
    }

    if (idMap.size === 0) return nextCode;

    const escapeRegex = (value: string) => value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const replacements = Array.from(idMap.entries()).sort((a, b) => b[0].length - a[0].length);
    for (const [original, safe] of replacements) {
      const pattern = new RegExp(`(^|[^A-Za-z0-9_])${escapeRegex(original)}(?=[^A-Za-z0-9_]|$)`, "g");
      nextCode = nextCode.replace(pattern, (_m, prefix) => `${prefix}${safe}`);
    }

    return nextCode;
  }, []);

  const renderToContainer = useCallback(async (container: HTMLDivElement, idSuffix: string) => {
    if (!container || !code) return;

    let rendered = false;
    let lastError: unknown = null;

    try {
      const attemptRender = async (diagramCode: string) => {
        const id = `mermaid-${idSuffix}-${Date.now()}`;
        const { svg } = await mermaid.render(id, diagramCode);
        container.innerHTML = svg;
      };

      try {
        setError(null);
        await attemptRender(code);
        rendered = true;
      } catch (err) {
        lastError = err;
      }

      try {
        const sanitized = sanitizeMermaidCode(code);
        if (!rendered && sanitized) {
          const id = `mermaid-${idSuffix}-sanitized-${Date.now()}`;
          const { svg } = await mermaid.render(id, sanitized);
          container.innerHTML = svg;
          rendered = true;
        }
      } catch (err) {
        lastError = lastError || err;
      }

      if (!rendered) {
        const err = lastError;
        setError(err instanceof Error ? err.message : "Failed to render diagram");
        return;
      }

      // Add click handlers to nodes
      if (onElementClick) {
        const nodes = container.querySelectorAll(".node, .cluster");
        nodes.forEach((node) => {
          const nodeId = node.id || node.getAttribute("data-id");
          if (nodeId) {
            (node as HTMLElement).style.cursor = "pointer";
            node.addEventListener("click", () => onElementClick(nodeId));
          }
        });
      }

      // Highlight element if specified
      if (highlightedElement) {
        const element = container.querySelector(
          `#${highlightedElement}, [data-id="${highlightedElement}"]`
        );
        if (element) {
          (element as HTMLElement).style.outline = "3px solid #3b82f6";
          (element as HTMLElement).style.outlineOffset = "2px";
        }
      }
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to render diagram");
    }
  }, [code, onElementClick, highlightedElement, sanitizeMermaidCode]);

  useEffect(() => {
    if (containerRef.current) {
      renderToContainer(containerRef.current, "main");
    }
  }, [renderToContainer]);

  useEffect(() => {
    if (!isFullscreen) return;
    let cancelled = false;
    let rafId = 0;
    let attempts = 0;

    const tryRender = () => {
      if (cancelled) return;
      if (fullscreenContainerRef.current) {
        renderToContainer(fullscreenContainerRef.current, "fullscreen");
        return;
      }
      if (attempts < 10) {
        attempts += 1;
        rafId = window.requestAnimationFrame(tryRender);
      }
    };

    rafId = window.requestAnimationFrame(tryRender);
    return () => {
      cancelled = true;
      window.cancelAnimationFrame(rafId);
    };
  }, [isFullscreen, renderToContainer]);

  const handleCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      // Fallback for older browsers
      const textarea = document.createElement("textarea");
      textarea.value = code;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand("copy");
      document.body.removeChild(textarea);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    }
  }, [code]);

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-full p-4 text-center">
        <div className="w-10 h-10 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center mb-3">
          <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p className="text-sm text-red-600 dark:text-red-400 mb-2">Failed to render diagram</p>
        <p className="text-xs text-muted-foreground">{error}</p>
      </div>
    );
  }

  return (
    <>
      <div className="relative h-full flex flex-col">
        <div
          ref={containerRef}
          className="flex-1 overflow-auto p-4 flex items-center justify-center [&_svg]:max-w-full [&_svg]:h-auto"
        />
        <div className="absolute bottom-3 right-3 flex gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setIsFullscreen(true)}
            className="h-8 text-xs bg-background/80 backdrop-blur-sm"
          >
            <svg className="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
            </svg>
            Fullscreen
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={handleCopy}
            className="h-8 text-xs bg-background/80 backdrop-blur-sm"
          >
            {copied ? (
              <>
                <svg className="w-3.5 h-3.5 mr-1.5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                Copied!
              </>
            ) : (
              <>
                <svg className="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                Copy
              </>
            )}
          </Button>
        </div>
      </div>

      {/* Fullscreen Modal */}
      <Dialog open={isFullscreen} onOpenChange={setIsFullscreen}>
        <DialogContent className="max-w-[95vw] w-[95vw] max-h-[95vh] h-[95vh] flex flex-col">
          <DialogHeader className="shrink-0">
            <DialogTitle className="flex items-center justify-between">
              <span>{title || "Diagram View"}</span>
              <Button
                variant="outline"
                size="sm"
                onClick={handleCopy}
                className="h-8 text-xs"
              >
                {copied ? (
                  <>
                    <svg className="w-3.5 h-3.5 mr-1.5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    Copied!
                  </>
                ) : (
                  <>
                    <svg className="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                    Copy Mermaid Code
                  </>
                )}
              </Button>
            </DialogTitle>
          </DialogHeader>
          <div
            ref={fullscreenContainerRef}
            className="flex-1 overflow-auto flex items-center justify-center bg-white dark:bg-slate-900 rounded-lg border [&_svg]:max-w-full [&_svg]:max-h-full"
          />
        </DialogContent>
      </Dialog>
    </>
  );
}
