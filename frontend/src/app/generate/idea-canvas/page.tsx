"use client";

import { useCallback, useState, useEffect, useMemo } from "react";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { IdeaCanvasForm, QuestionCard, ApproachTabs } from "@/components/idea-canvas";
import { MindMapViewer } from "@/components/mindmap";
import { useIdeaCanvas } from "@/hooks/useIdeaCanvas";
import { useAuth } from "@/hooks/useAuth";
import { useApiKeys } from "@/hooks/useApiKeys";
import { AuthModal } from "@/components/auth/AuthModal";
import { ApiKeysModal } from "@/components/studio";
import { StartCanvasRequest, RefinementTarget } from "@/lib/types/idea-canvas";
import { generateCanvasReport, generateCanvasMindmap, CanvasMindmapResult, generateApproaches, Approach } from "@/lib/api/idea-canvas";
import { generateImage, downloadImage } from "@/lib/api/image";

export default function IdeaCanvasPage() {
  const { isAuthenticated, isLoading: authLoading, user } = useAuth();
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [showApiKeyModal, setShowApiKeyModal] = useState(false);

  // API Keys from shared store
  const apiKeys = useApiKeys();

  const {
    state: canvasState,
    sessionId: canvasSessionId,
    canvas,
    currentQuestion,
    questionHistory,
    progressMessage: canvasProgressMessage,
    error: canvasError,
    provider: canvasProvider,
    apiKey: canvasApiKey,
    imageApiKey: canvasImageApiKey,
    includeReportImage,
    start: startCanvas,
    answer: submitCanvasAnswer,
    reset: resetCanvas,
  } = useIdeaCanvas();

  // Report generation state
  const [isGeneratingReport, setIsGeneratingReport] = useState(false);
  const [reportData, setReportData] = useState<{
    title: string;
    markdown_content: string;
    pdf_base64?: string;
    image_base64?: string;
    image_format?: "png" | "svg";
  } | null>(null);
  const [reportError, setReportError] = useState<string | null>(null);
  const [exitedToSummary, setExitedToSummary] = useState(false);
  const [markdownCopied, setMarkdownCopied] = useState(false);

  // Image generation from report state
  const [isGeneratingImage, setIsGeneratingImage] = useState(false);
  const [generatedImage, setGeneratedImage] = useState<{ data: string; format: string } | null>(null);
  const [imageGenError, setImageGenError] = useState<string | null>(null);

  // Canvas mind map state
  const [canvasMindMap, setCanvasMindMap] = useState<CanvasMindmapResult | null>(null);
  const [isGeneratingCanvasMindMap, setIsGeneratingCanvasMindMap] = useState(false);
  const [canvasMindMapError, setCanvasMindMapError] = useState<string | null>(null);

  // Approach generation state
  const [approaches, setApproaches] = useState<Approach[]>([]);
  const [isGeneratingApproaches, setIsGeneratingApproaches] = useState(false);
  const [refinementTarget, setRefinementTarget] = useState<RefinementTarget | null>(null);
  const [workspaceTab, setWorkspaceTab] = useState("approaches");

  const resetLocalState = useCallback(() => {
    setReportData(null);
    setReportError(null);
    setIsGeneratingReport(false);
    setMarkdownCopied(false);
    setGeneratedImage(null);
    setIsGeneratingImage(false);
    setImageGenError(null);
    setCanvasMindMap(null);
    setCanvasMindMapError(null);
    setIsGeneratingCanvasMindMap(false);
    setApproaches([]);
    setRefinementTarget(null);
    setExitedToSummary(false);
    setWorkspaceTab("approaches");
  }, []);

  const handleExitToSummary = useCallback(() => {
    setExitedToSummary(true);
  }, []);

  const handleCanvasSubmit = useCallback(
    (
      request: StartCanvasRequest,
      contentApiKey: string,
      imageApiKey: string | null,
      includeImage: boolean
    ) => {
      resetLocalState();
      startCanvas(request, contentApiKey, imageApiKey, includeImage, user?.id);
    },
    [resetLocalState, startCanvas, user?.id]
  );

  const handleCanvasAnswer = useCallback(
    (answer: string | string[]) => {
      submitCanvasAnswer(answer, user?.id);
    },
    [submitCanvasAnswer, user?.id]
  );

  const handleGenerateCanvasMindMap = useCallback(async () => {
    if (!canvasSessionId || !canvasApiKey) return;

    setIsGeneratingCanvasMindMap(true);
    setCanvasMindMapError(null);

    try {
      const result = await generateCanvasMindmap({
        sessionId: canvasSessionId,
        provider: canvasProvider,
        apiKey: canvasApiKey,
      });
      setCanvasMindMap(result);
    } catch (err) {
      setCanvasMindMapError(err instanceof Error ? err.message : "Failed to generate mind map");
    } finally {
      setIsGeneratingCanvasMindMap(false);
    }
  }, [canvasSessionId, canvasApiKey, canvasProvider]);

  const handleGenerateApproaches = useCallback(async () => {
    if (!canvasSessionId || !canvasApiKey) return;

    setIsGeneratingApproaches(true);
    try {
      const result = await generateApproaches({
        sessionId: canvasSessionId,
        provider: canvasProvider,
        apiKey: canvasApiKey,
      });
      setApproaches(result.approaches);
    } catch (err) {
      console.error('Failed to generate approaches:', err);
    } finally {
      setIsGeneratingApproaches(false);
    }
  }, [canvasSessionId, canvasApiKey, canvasProvider]);

  const handleElementClick = useCallback((target: RefinementTarget) => {
    setRefinementTarget(target);
  }, []);

  const generateImageFromReportContent = useCallback(
    async (reportTitle: string, reportMarkdown: string) => {
      if (!canvasImageApiKey) {
        setImageGenError("No image API key available");
        return;
      }

      setIsGeneratingImage(true);
      setImageGenError(null);
      setGeneratedImage(null);

      try {
        const summaryPrompt = `Create a beautiful hand-drawn style infographic that visually summarizes this implementation plan:

Title: ${reportTitle}

Key points to visualize:
${reportMarkdown.slice(0, 1500)}

Style: Hand-drawn, sketch-like, warm colors, clean whiteboard aesthetic with icons and arrows connecting concepts. Include the main title at the top.`;

        const result = await generateImage(
          {
            prompt: summaryPrompt,
            style_category: "handwritten_and_human",
            style: "whiteboard_handwritten",
            output_format: "raster",
            free_text_mode: false,
          },
          canvasImageApiKey
        );

        if (result.success && result.image_data) {
          setGeneratedImage({
            data: result.image_data,
            format: result.format,
          });
        } else {
          setImageGenError(result.error || "Failed to generate image");
        }
      } catch (err) {
        setImageGenError(err instanceof Error ? err.message : "Image generation failed");
      } finally {
        setIsGeneratingImage(false);
      }
    },
    [canvasImageApiKey]
  );

  const handleGenerateReport = useCallback(async () => {
    if (!canvasSessionId || !canvasApiKey) {
      setReportError("No active canvas session");
      return;
    }

    setIsGeneratingReport(true);
    setReportError(null);
    setImageGenError(null);
    setMarkdownCopied(false);
    setGeneratedImage(null);

    try {
      const reportImageApiKey = includeReportImage ? canvasImageApiKey : undefined;
      const result = await generateCanvasReport({
        sessionId: canvasSessionId,
        outputFormat: "both",
        provider: canvasProvider,
        apiKey: canvasApiKey,
        imageApiKey: reportImageApiKey,
      });

      setReportData({
        title: result.title,
        markdown_content: result.markdown_content || "",
        pdf_base64: result.pdf_base64,
        image_base64: result.image_base64,
        image_format: result.image_format,
      });
      if (result.image_base64 && result.image_format) {
        setGeneratedImage({
          data: result.image_base64,
          format: result.image_format,
        });
      } else if (includeReportImage) {
        void generateImageFromReportContent(result.title, result.markdown_content || "");
      }
    } catch (err) {
      setReportError(err instanceof Error ? err.message : "Failed to generate report");
    } finally {
      setIsGeneratingReport(false);
    }
  }, [
    canvasSessionId,
    canvasApiKey,
    canvasProvider,
    canvasImageApiKey,
    includeReportImage,
    generateImageFromReportContent,
  ]);

  const handleDownloadMarkdown = useCallback(() => {
    if (!reportData) return;

    const blob = new Blob([reportData.markdown_content], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${reportData.title.replace(/[^a-z0-9]/gi, "_").toLowerCase()}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }, [reportData]);

  const createPdfBlob = useCallback((pdfBase64: string) => {
    const byteCharacters = atob(pdfBase64);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: "application/pdf" });
  }, []);

  const handleDownloadPdf = useCallback(() => {
    if (!reportData?.pdf_base64) return;

    const blob = createPdfBlob(reportData.pdf_base64);

    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${reportData.title.replace(/[^a-z0-9]/gi, "_").toLowerCase()}.pdf`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }, [reportData, createPdfBlob]);

  const handleOpenPdfPreview = useCallback(() => {
    if (!reportData?.pdf_base64) return;

    const blob = createPdfBlob(reportData.pdf_base64);
    const url = URL.createObjectURL(blob);
    window.open(url, "_blank", "noopener,noreferrer");
    setTimeout(() => URL.revokeObjectURL(url), 60000);
  }, [reportData, createPdfBlob]);

  const handleCopyMarkdown = useCallback(async () => {
    if (!reportData?.markdown_content) return;

    try {
      await navigator.clipboard.writeText(reportData.markdown_content);
      setMarkdownCopied(true);
      setTimeout(() => setMarkdownCopied(false), 1500);
    } catch {
      const textarea = document.createElement("textarea");
      textarea.value = reportData.markdown_content;
      textarea.style.position = "fixed";
      textarea.style.opacity = "0";
      document.body.appendChild(textarea);
      textarea.focus();
      textarea.select();
      document.execCommand("copy");
      document.body.removeChild(textarea);
      setMarkdownCopied(true);
      setTimeout(() => setMarkdownCopied(false), 1500);
    }
  }, [reportData]);

  // Auto-generate approaches when Q&A completes
  useEffect(() => {
    if (canvasState === 'suggest_complete' && approaches.length === 0 && !isGeneratingApproaches) {
      handleGenerateApproaches();
    }
  }, [canvasState, approaches.length, isGeneratingApproaches, handleGenerateApproaches]);

  const isCanvasStarting = canvasState === "starting";

  // Check if canvas is in workspace mode
  const isCanvasWorkspace =
    canvasState === "suggest_complete" || reportData || exitedToSummary;

  const answeredCount = questionHistory.length;
  const activeQuestionNumber = currentQuestion ? answeredCount + 1 : answeredCount;
  const estimatedTotalQuestions = Math.max(activeQuestionNumber + 2, 8);
  const progressFraction = Math.min(activeQuestionNumber / estimatedTotalQuestions, 1);
  const progressDasharray = `${Math.round(progressFraction * 283)} 283`;

  const modalLayer = (
    <>
      <AuthModal isOpen={showAuthModal} onClose={() => setShowAuthModal(false)} />
      <ApiKeysModal
        isOpen={showApiKeyModal}
        onOpenChange={setShowApiKeyModal}
        provider={apiKeys.provider}
        contentModel={apiKeys.contentModel}
        onProviderChange={apiKeys.setProvider}
        onContentModelChange={apiKeys.setContentModel}
        contentApiKey={apiKeys.contentApiKey}
        onContentApiKeyChange={apiKeys.setContentApiKey}
        enableImageGeneration={apiKeys.enableImageGeneration}
        onEnableImageGenerationChange={apiKeys.setEnableImageGeneration}
        allowImageGenerationToggle={true}
        requireImageKey={false}
        imageModel={apiKeys.imageModel}
        onImageModelChange={apiKeys.setImageModel}
        imageApiKey={apiKeys.imageApiKey}
        onImageApiKeyChange={apiKeys.setImageApiKey}
        canClose={true}
      />
    </>
  );

  const renderMarkdownAsHtml = useCallback((md: string): string => {
    const escapeHtml = (value: string) =>
      value.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    const isTableSeparator = (line: string) =>
      /^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$/.test(line);
    const parseRow = (line: string) => {
      let trimmed = line.trim();
      if (trimmed.startsWith("|")) trimmed = trimmed.slice(1);
      if (trimmed.endsWith("|")) trimmed = trimmed.slice(0, -1);
      return trimmed.split("|").map((cell) => cell.trim());
    };

    const tableBlocks: string[] = [];
    const lines = md.split("\n");
    const outputLines: string[] = [];

    let i = 0;
    while (i < lines.length) {
      const line = lines[i];
      const nextLine = lines[i + 1];
      if (line && nextLine && line.includes("|") && isTableSeparator(nextLine)) {
        const headerCells = parseRow(line);
        const alignHints = parseRow(nextLine);
        const aligns = headerCells.map((_, idx) => {
          const hint = (alignHints[idx] || "").trim();
          if (hint.startsWith(":") && hint.endsWith(":")) return "center";
          if (hint.endsWith(":")) return "right";
          return "left";
        });
        const bodyRows: string[][] = [];
        i += 2;
        while (i < lines.length && lines[i].includes("|") && lines[i].trim() !== "") {
          bodyRows.push(parseRow(lines[i]));
          i += 1;
        }

        const headerHtml = headerCells
          .map((cell, idx) => {
            const align = aligns[idx] || "left";
            return `<th class="border border-border bg-muted/40 px-2 py-1 text-left align-top" style="text-align:${align}">${escapeHtml(cell)}</th>`;
          })
          .join("");
        const bodyHtml = bodyRows
          .map((row) => {
            const cells = headerCells.map((_, idx) => {
              const align = aligns[idx] || "left";
              const cell = row[idx] || "";
              return `<td class="border border-border px-2 py-1 align-top" style="text-align:${align}">${escapeHtml(cell)}</td>`;
            });
            return `<tr>${cells.join("")}</tr>`;
          })
          .join("");
        const tableHtml = `<div class="overflow-x-auto my-4"><table class="w-full border-collapse text-sm"><thead><tr>${headerHtml}</tr></thead><tbody>${bodyHtml}</tbody></table></div>`;
        const token = `__TABLE_BLOCK_${tableBlocks.length}__`;
        tableBlocks.push(tableHtml);
        outputLines.push(token);
        continue;
      }
      outputLines.push(line);
      i += 1;
    }

    let html = escapeHtml(outputLines.join("\n"))
      .replace(/^### (.+)$/gm, '<h3 class="text-base font-semibold mt-4 mb-2">$1</h3>')
      .replace(/^## (.+)$/gm, '<h2 class="text-lg font-bold mt-5 mb-2">$1</h2>')
      .replace(/^# (.+)$/gm, '<h1 class="text-xl font-bold mt-6 mb-3">$1</h1>')
      .replace(/\*\*\*(.+?)\*\*\*/g, "<strong><em>$1</em></strong>")
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(.+?)\*/g, "<em>$1</em>")
      .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre class="bg-muted/60 p-3 rounded-lg overflow-x-auto my-3 text-sm"><code>$2</code></pre>')
      .replace(/`([^`]+)`/g, '<code class="bg-muted px-1.5 py-0.5 rounded text-sm">$1</code>')
      .replace(/^- (.+)$/gm, '<li class="ml-4 list-disc">$1</li>')
      .replace(/^• (.+)$/gm, '<li class="ml-4 list-disc">$1</li>')
      .replace(/^\d+\. (.+)$/gm, '<li class="ml-4 list-decimal">$1</li>')
      .replace(/^> (.+)$/gm, '<blockquote class="border-l-4 border-amber-300/60 pl-4 italic text-muted-foreground my-2">$1</blockquote>')
      .replace(/^---$/gm, '<hr class="my-4 border-border"/>')
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-amber-700 underline underline-offset-2" target="_blank" rel="noopener noreferrer">$1</a>')
      .replace(/\n\n/g, '</p><p class="my-2">')
      .replace(/\n/g, "<br/>");

    html = html.replace(/__TABLE_BLOCK_(\d+)__/g, (_match, idx) => {
      const table = tableBlocks[Number(idx)];
      return table || "";
    });
    html = html.replace(/<p class="my-2">\s*(<div class="overflow-x-auto[\s\S]*?<\/div>)\s*<\/p>/g, "$1");

    return `<div class="max-w-none text-sm leading-6"><p class="my-2">${html}</p></div>`;
  }, []);

  const reportMarkdownHtml = useMemo(() => {
    if (!reportData?.markdown_content) return "";
    return renderMarkdownAsHtml(reportData.markdown_content);
  }, [reportData, renderMarkdownAsHtml]);

  const orderedApproaches = useMemo(() => {
    if (!approaches.length) return [];
    const indexMap = new Map<string, number>();
    approaches.forEach((approach, index) => {
      indexMap.set(approach.id, index);
    });

    const rankApproach = (name: string) => {
      const lower = name.toLowerCase();
      if (/(simple|minimal|mvp|basic|starter)/.test(lower)) return 0;
      if (/(standard|balanced|pragmatic|core|typical)/.test(lower)) return 1;
      if (/(scale|scalable|enterprise|advanced|robust)/.test(lower)) return 2;
      if (/(modern|innovative|frontier|ai-native|reactive|cutting)/.test(lower)) return 3;
      return 1;
    };

    return [...approaches].sort((a, b) => {
      const rankDiff = rankApproach(a.name) - rankApproach(b.name);
      if (rankDiff !== 0) return rankDiff;
      return (indexMap.get(a.id) || 0) - (indexMap.get(b.id) || 0);
    });
  }, [approaches]);

  const snapshotThemes = useMemo(() => {
    if (!questionHistory.length) return [];

    const shorten = (value: string, max = 92) =>
      value.length > max ? `${value.slice(0, max - 1)}...` : value;

    const normalizeQuestion = (value: string) => {
      const cleaned = value.replace(/\s+/g, " ").trim();
      const withoutQuestionMark = cleaned.endsWith("?")
        ? cleaned.slice(0, -1)
        : cleaned;
      return shorten(withoutQuestionMark, 72);
    };

    const normalizeAnswer = (value: string | string[]) => {
      const text = Array.isArray(value) ? value.join(", ") : value;
      return shorten(text.replace(/\s+/g, " ").trim(), 104);
    };

    const themeDefs = [
      {
        key: "problem",
        label: "Problem",
        keywords: ["problem", "purpose", "goal", "why", "solve", "pain", "main task", "use case"],
      },
      {
        key: "users",
        label: "Users",
        keywords: ["user", "audience", "customer", "persona", "stakeholder", "who"],
      },
      {
        key: "inputs",
        label: "Inputs",
        keywords: ["input", "data", "source", "document", "file", "knowledge", "context", "information"],
      },
      {
        key: "outputs",
        label: "Outputs",
        keywords: ["output", "result", "deliver", "response", "answer", "experience", "interface", "voice", "channel"],
      },
      {
        key: "constraints",
        label: "Constraints",
        keywords: ["constraint", "limit", "budget", "timeline", "deadline", "scale", "performance", "latency", "security", "privacy", "compliance", "risk"],
      },
      {
        key: "success",
        label: "Success",
        keywords: ["success", "metric", "kpi", "measure", "validation", "quality", "accuracy", "target", "benchmark"],
      },
      {
        key: "details",
        label: "Key Detail",
        keywords: [],
      },
    ] as const;

    const classifyTheme = (questionText: string) => {
      const lower = questionText.toLowerCase();
      const match = themeDefs.find(
        (theme) =>
          theme.key !== "details" &&
          theme.keywords.some((keyword) => lower.includes(keyword))
      );
      return match?.key ?? "details";
    };

    const captured = new Map<string, { label: string; question: string; answer: string }>();
    for (let i = questionHistory.length - 1; i >= 0; i -= 1) {
      const item = questionHistory[i];
      const themeKey = classifyTheme(item.question.question);
      if (captured.has(themeKey)) continue;
      const themeMeta = themeDefs.find((theme) => theme.key === themeKey);
      captured.set(themeKey, {
        label: themeMeta?.label ?? "Key Detail",
        question: normalizeQuestion(item.question.question),
        answer: normalizeAnswer(item.answer),
      });
      if (captured.size >= 5) break;
    }

    return themeDefs
      .map((theme) => captured.get(theme.key))
      .filter((item): item is { label: string; question: string; answer: string } => Boolean(item))
      .slice(0, 5);
  }, [questionHistory]);

  // ============================================================================
  // VIEW 1: Initial Form View
  // ============================================================================
  if (canvasState === "idle" || canvasState === "starting") {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50/50 via-white to-orange-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-amber-950/20">
        {modalLayer}

        <header className="border-b border-amber-200/50 dark:border-amber-900/30 bg-white/60 dark:bg-slate-900/60 backdrop-blur-md sticky top-0 z-40">
          <div className="container mx-auto px-4 h-14 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <a href="/generate" className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                Back to Studio
              </a>
              <div className="h-6 w-px bg-amber-200 dark:bg-amber-800" />
              <span className="font-bold text-lg bg-gradient-to-r from-amber-600 to-orange-600 bg-clip-text text-transparent">
                Idea Canvas
              </span>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="ghost" size="sm" onClick={() => setShowApiKeyModal(true)}>
                <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                </svg>
                API Keys
              </Button>
              {!authLoading && !isAuthenticated && (
                <Button size="sm" variant="outline" onClick={() => setShowAuthModal(true)}>
                  Sign In
                </Button>
              )}
            </div>
          </div>
        </header>

        <main className="container mx-auto px-4 py-12">
          <div className="max-w-xl mx-auto">
            <div className="text-center mb-10">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-amber-400 to-orange-500 shadow-lg shadow-amber-500/25 mb-6">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456z" />
                </svg>
              </div>
              <h1 className="text-3xl font-bold mb-3">Explore Your Idea</h1>
              <p className="text-muted-foreground max-w-md mx-auto">
                Guided Q&A to deeply understand your idea, then get implementation approaches and specs.
              </p>
            </div>

            <div className="bg-white dark:bg-slate-900 rounded-3xl shadow-xl shadow-amber-500/5 border border-amber-100 dark:border-amber-900/30 p-8">
              <IdeaCanvasForm
                onSubmit={handleCanvasSubmit}
                isStarting={isCanvasStarting}
                onConfigureKeys={() => setShowApiKeyModal(true)}
              />
            </div>
          </div>
        </main>
      </div>
    );
  }

  // ============================================================================
  // VIEW 2: Error View
  // ============================================================================
  if (canvasState === "error") {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50/50 via-white to-orange-50/30 dark:from-slate-950 dark:via-slate-900 dark:to-amber-950/20">
        {modalLayer}
        <header className="border-b border-amber-200/50 dark:border-amber-900/30 bg-white/60 dark:bg-slate-900/60 backdrop-blur-md sticky top-0 z-40">
          <div className="container mx-auto px-4 h-14 flex items-center">
            <a href="/generate" className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Back to Studio
            </a>
          </div>
        </header>

        <main className="container mx-auto px-4 py-12">
          <div className="max-w-md mx-auto">
            <div className="flex flex-col items-center justify-center p-10 rounded-3xl border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-950/30">
              <div className="w-16 h-16 rounded-2xl bg-red-100 dark:bg-red-900/50 flex items-center justify-center mb-6">
                <svg className="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-red-800 dark:text-red-200 mb-2">Something went wrong</h3>
              <p className="text-sm text-red-600 dark:text-red-300 text-center mb-6">{canvasError}</p>
              <Button
                onClick={() => {
                  resetLocalState();
                  resetCanvas();
                }}
                className="bg-red-600 hover:bg-red-700"
              >
                Try Again
              </Button>
            </div>
          </div>
        </main>
      </div>
    );
  }

  // ============================================================================
  // VIEW 3: Workspace View (After Q&A Complete)
  // ============================================================================
  if (isCanvasWorkspace) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
        {modalLayer}
        <header className="border-b bg-white dark:bg-slate-900 sticky top-0 z-40">
          <div className="container mx-auto px-4 h-14 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <a href="/generate" className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                Back
              </a>
              <div className="h-6 w-px bg-border" />
              <span className="font-semibold text-amber-600 dark:text-amber-400">Idea Canvas</span>
              <span className="text-sm text-muted-foreground truncate max-w-[300px]">
                {canvas?.idea}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="ghost" size="sm" onClick={() => setShowApiKeyModal(true)}>
                <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                </svg>
                API Keys
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  resetLocalState();
                  resetCanvas();
                }}
              >
                New Canvas
              </Button>
            </div>
          </div>
        </header>

        <main className="container mx-auto px-4 py-6">
          <div className="rounded-2xl border bg-white dark:bg-slate-900 h-[calc(100vh-8rem)] flex flex-col overflow-hidden">
            <Tabs value={workspaceTab} onValueChange={setWorkspaceTab} className="flex flex-col h-full">
              <div className="px-5 py-4 border-b bg-gradient-to-r from-amber-50 via-white to-emerald-50/80 dark:from-slate-900 dark:via-slate-900 dark:to-slate-900 space-y-3">
                <div className="flex flex-col gap-2 lg:flex-row lg:items-center lg:justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center shadow-sm">
                      <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </div>
                    <div>
                      <h2 className="font-semibold">Idea Workspace</h2>
                      <p className="text-xs text-muted-foreground">Move from approaches to spec pack to presentation assets</p>
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-2 text-xs">
                    <span className="px-2.5 py-1 rounded-full border bg-white/80 dark:bg-slate-900">
                      {questionHistory.length} answers
                    </span>
                    <span className="px-2.5 py-1 rounded-full border bg-white/80 dark:bg-slate-900">
                      {orderedApproaches.length || approaches.length} approaches
                    </span>
                    <span className={`px-2.5 py-1 rounded-full border ${
                      reportData ? "bg-emerald-600 text-white border-emerald-600" : "bg-white/80 dark:bg-slate-900"
                    }`}>
                      Report {reportData ? "ready" : "pending"}
                    </span>
                  </div>
                </div>
                <TabsList className="w-full grid grid-cols-4 h-11 bg-muted/40 border">
                  <TabsTrigger value="approaches" className="font-medium">Approaches</TabsTrigger>
                  <TabsTrigger value="report" className="font-medium">Report Pack</TabsTrigger>
                  <TabsTrigger value="visual" className="font-medium">Visual Summary</TabsTrigger>
                  <TabsTrigger value="mindmap" className="font-medium">Mind Map</TabsTrigger>
                </TabsList>
              </div>

              <TabsContent value="approaches" className="flex-1 min-h-0 m-0">
                <div className="h-full flex flex-col">
                  <div className="px-6 py-4 border-b bg-amber-50/60 dark:bg-amber-950/20 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                    <div className="flex items-start gap-3">
                      <div className="w-9 h-9 rounded-lg bg-amber-100 dark:bg-amber-900/40 flex items-center justify-center shrink-0">
                        <svg className="w-4 h-4 text-amber-600 dark:text-amber-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                      </div>
                      <div>
                        <p className="text-sm font-semibold">Basic to advanced implementation paths</p>
                        <p className="text-xs text-muted-foreground">Use the subtabs to compare architectures and tasks tier by tier.</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={handleGenerateApproaches}
                        disabled={isGeneratingApproaches}
                      >
                        {isGeneratingApproaches ? "Regenerating..." : "Regenerate"}
                      </Button>
                    </div>
                  </div>
                  <div className="flex-1 min-h-0">
                    {isGeneratingApproaches ? (
                      <div className="flex flex-col items-center justify-center h-full p-8">
                        <div className="w-12 h-12 border-3 border-amber-500 border-t-transparent rounded-full animate-spin mb-4" />
                        <p className="text-sm text-muted-foreground">Generating approaches...</p>
                      </div>
                    ) : orderedApproaches.length > 0 ? (
                      <ApproachTabs
                        approaches={orderedApproaches}
                        onElementClick={handleElementClick}
                        refinementTarget={refinementTarget || undefined}
                        isLoading={false}
                      />
                    ) : (
                      <div className="flex flex-col items-center justify-center h-full p-8">
                        <Button onClick={handleGenerateApproaches}>Generate Approaches</Button>
                      </div>
                    )}
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="report" className="flex-1 min-h-0 m-0">
                <div className="h-full overflow-auto p-6 space-y-5 bg-slate-50/60 dark:bg-slate-950/40">
                  {reportError && (
                    <div className="p-3 rounded-lg bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-800 text-sm text-red-600 dark:text-red-400">
                      {reportError}
                    </div>
                  )}

                  {!reportData ? (
                    <div className="max-w-2xl">
                      <div className="rounded-2xl border bg-white dark:bg-slate-900 p-6 space-y-4 shadow-sm">
                        <div className="flex items-start gap-3">
                          <div className="w-11 h-11 rounded-xl bg-emerald-100 dark:bg-emerald-900/40 flex items-center justify-center shrink-0">
                            <svg className="w-5 h-5 text-emerald-600 dark:text-emerald-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                          </div>
                          <div>
                            <h3 className="font-semibold">Generate your implementation report pack</h3>
                            <p className="text-sm text-muted-foreground mt-1">
                              Create a polished spec document (PDF + Markdown) that is ready to share with teammates.
                            </p>
                          </div>
                        </div>
                        <div className="flex flex-wrap gap-2 text-xs">
                          <span className="px-2.5 py-1 rounded-full border bg-muted/30">Executive summary</span>
                          <span className="px-2.5 py-1 rounded-full border bg-muted/30">Architecture guidance</span>
                          <span className="px-2.5 py-1 rounded-full border bg-muted/30">Task breakdown</span>
                        </div>
                        <div className="flex flex-wrap gap-2 pt-2">
                          <Button
                            onClick={handleGenerateReport}
                            disabled={isGeneratingReport}
                            className="bg-emerald-600 hover:bg-emerald-700"
                          >
                            {isGeneratingReport ? (
                              <>
                                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                                Generating report...
                              </>
                            ) : (
                              <>
                                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                                Generate Report Pack
                              </>
                            )}
                          </Button>
                          <Button onClick={() => handleCanvasAnswer("continue")} variant="outline">
                            Continue Exploring
                          </Button>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <>
                      <div className="rounded-2xl border border-emerald-200/80 dark:border-emerald-900/60 bg-emerald-50/80 dark:bg-emerald-950/30 p-5 space-y-4">
                        <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
                          <div>
                            <p className="text-xs uppercase tracking-wide text-emerald-700 dark:text-emerald-300 font-medium mb-1">
                              Implementation Plan
                            </p>
                            <h3 className="text-lg font-semibold text-emerald-900 dark:text-emerald-100">
                              {reportData.title}
                            </h3>
                            <p className="text-xs text-emerald-800/80 dark:text-emerald-200/80 mt-1">
                              Generated from {questionHistory.length} exploration answers
                            </p>
                          </div>
                          <div className="flex flex-wrap gap-2">
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={handleGenerateReport}
                              disabled={isGeneratingReport}
                              className="bg-white/80"
                            >
                              {isGeneratingReport ? "Refreshing..." : "Regenerate"}
                            </Button>
                            <Button variant="outline" size="sm" onClick={handleOpenPdfPreview} disabled={!reportData.pdf_base64}>
                              Open PDF
                            </Button>
                          </div>
                        </div>
                        <div className="flex flex-wrap gap-2 text-xs">
                          <span className={`px-2.5 py-1 rounded-full border ${reportData.pdf_base64 ? "bg-white dark:bg-slate-900" : "opacity-70"}`}>
                            PDF {reportData.pdf_base64 ? "ready" : "pending"}
                          </span>
                          <span className="px-2.5 py-1 rounded-full border bg-white dark:bg-slate-900">
                            Markdown ready
                          </span>
                          <span className={`px-2.5 py-1 rounded-full border ${includeReportImage ? "bg-white dark:bg-slate-900" : "opacity-70"}`}>
                            Visual {includeReportImage ? "enabled" : "off"}
                          </span>
                        </div>
                      </div>

                      <div className="grid gap-5 lg:grid-cols-[minmax(0,1.1fr)_minmax(0,0.9fr)]">
                        <div className="rounded-2xl border bg-white dark:bg-slate-900 overflow-hidden">
                          <div className="px-5 py-4 border-b bg-muted/20 dark:bg-slate-800/60 flex items-center justify-between">
                            <div>
                              <p className="text-sm font-medium">Markdown Preview</p>
                              <p className="text-xs text-muted-foreground">Rendered view of your report</p>
                            </div>
                            <div className="flex items-center gap-2">
                              <Button onClick={handleCopyMarkdown} variant="ghost" size="sm" className="border">
                                {markdownCopied ? "Copied!" : "Copy Markdown"}
                              </Button>
                              <Button onClick={handleDownloadMarkdown} variant="outline" size="sm">
                                Markdown
                              </Button>
                            </div>
                          </div>
                          <div className="max-h-[520px] overflow-auto px-5 py-4">
                            {reportMarkdownHtml ? (
                              <div dangerouslySetInnerHTML={{ __html: reportMarkdownHtml }} />
                            ) : (
                              <p className="text-sm text-muted-foreground">Markdown preview is unavailable.</p>
                            )}
                          </div>
                        </div>

                        <div className="space-y-4">
                          <div className="rounded-2xl border bg-white dark:bg-slate-900 p-4 space-y-3">
                            <div className="flex items-center justify-between">
                              <div>
                                <p className="text-sm font-medium">Export Pack</p>
                                <p className="text-xs text-muted-foreground">Download or open the full report</p>
                              </div>
                            </div>
                            <div className="grid grid-cols-2 gap-2">
                              <Button onClick={handleDownloadPdf} disabled={!reportData.pdf_base64} size="sm">
                                <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                                </svg>
                                Download PDF
                              </Button>
                              <Button variant="outline" size="sm" onClick={handleOpenPdfPreview} disabled={!reportData.pdf_base64}>
                                Open PDF
                              </Button>
                              <Button onClick={handleDownloadMarkdown} variant="outline" size="sm">
                                Markdown
                              </Button>
                              <Button onClick={handleCopyMarkdown} variant="ghost" size="sm" className="border">
                                {markdownCopied ? "Copied!" : "Copy"}
                              </Button>
                            </div>
                          </div>

                          <div className="rounded-2xl border bg-white dark:bg-slate-900 p-4 space-y-3">
                            <div className="flex items-center justify-between">
                              <div>
                                <p className="text-sm font-medium">What this pack includes</p>
                                <p className="text-xs text-muted-foreground">Use this as a slide-ready outline</p>
                              </div>
                            </div>
                            <div className="grid grid-cols-2 gap-2 text-xs">
                              <div className="rounded-lg border p-3 bg-muted/20">
                                Executive summary
                              </div>
                              <div className="rounded-lg border p-3 bg-muted/20">
                                Architecture guidance
                              </div>
                              <div className="rounded-lg border p-3 bg-muted/20">
                                Implementation roadmap
                              </div>
                              <div className="rounded-lg border p-3 bg-muted/20">
                                Risks and tradeoffs
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </>
                  )}
                </div>
              </TabsContent>

              <TabsContent value="visual" className="flex-1 min-h-0 m-0">
                <div className="h-full overflow-auto p-6 bg-slate-50/60 dark:bg-slate-950/40">
                  {!reportData ? (
                    <div className="max-w-2xl">
                      <div className="rounded-2xl border bg-white dark:bg-slate-900 p-6 space-y-4">
                        <h3 className="font-semibold">Visual summary needs the report pack first</h3>
                        <p className="text-sm text-muted-foreground">
                          Generate the report pack to create an infographic-style summary that looks great in slides.
                        </p>
                        <Button
                          onClick={handleGenerateReport}
                          disabled={isGeneratingReport}
                          className="bg-emerald-600 hover:bg-emerald-700"
                        >
                          {isGeneratingReport ? "Generating..." : "Generate Report Pack"}
                        </Button>
                      </div>
                    </div>
                  ) : includeReportImage ? (
                    <div className="space-y-4">
                      <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                        <div>
                          <h3 className="font-semibold">Slide-ready visual summary</h3>
                          <p className="text-sm text-muted-foreground">
                            Use this as a hero visual in presentations or project briefs.
                          </p>
                        </div>
                        <div className="flex flex-wrap gap-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => generateImageFromReportContent(reportData.title, reportData.markdown_content)}
                            disabled={isGeneratingImage}
                          >
                            {isGeneratingImage ? "Generating..." : "Regenerate"}
                          </Button>
                          <Button
                            size="sm"
                            disabled={!generatedImage}
                            onClick={() => {
                              if (generatedImage) {
                                downloadImage(
                                  generatedImage.data,
                                  `${reportData.title.replace(/[^a-z0-9]/gi, "_").toLowerCase() || "infographic"}`,
                                  generatedImage.format as "png" | "svg"
                                );
                              }
                            }}
                          >
                            Download
                          </Button>
                        </div>
                      </div>

                      <div className="rounded-2xl border bg-white dark:bg-slate-900 p-4">
                        <div className="rounded-xl border bg-muted/20 dark:bg-slate-800/60 min-h-[420px] flex items-center justify-center overflow-hidden">
                          {isGeneratingImage ? (
                            <div className="flex flex-col items-center gap-2 text-sm text-muted-foreground">
                              <div className="w-10 h-10 border-2 border-amber-500 border-t-transparent rounded-full animate-spin" />
                              <span>Designing your visual...</span>
                            </div>
                          ) : generatedImage ? (
                            <Image
                              src={`data:image/${generatedImage.format};base64,${generatedImage.data}`}
                              alt="Report visual summary"
                              width={1200}
                              height={720}
                              unoptimized
                              className="w-full h-full object-contain"
                            />
                          ) : (
                            <div className="text-sm text-muted-foreground text-center px-8">
                              Generate the visual summary to produce a presentation-friendly infographic.
                            </div>
                          )}
                        </div>
                        {imageGenError && (
                          <p className="text-xs text-red-600 dark:text-red-400 mt-3">{imageGenError}</p>
                        )}
                      </div>
                    </div>
                  ) : (
                    <div className="max-w-2xl">
                      <div className="rounded-2xl border border-dashed bg-white dark:bg-slate-900 p-6 space-y-2">
                        <h3 className="font-semibold">Visual summaries are disabled</h3>
                        <p className="text-sm text-muted-foreground">
                          Turn on image generation in the API key settings to enable slide-ready visuals.
                        </p>
                        <Button variant="outline" onClick={() => setShowApiKeyModal(true)}>
                          Open API Key Settings
                        </Button>
                      </div>
                    </div>
                  )}
                </div>
              </TabsContent>

              <TabsContent value="mindmap" className="flex-1 min-h-0 m-0">
                <div className="h-full flex flex-col">
                  <div className="px-6 py-4 border-b flex flex-col gap-2 lg:flex-row lg:items-center lg:justify-between bg-muted/20 dark:bg-slate-800/40">
                    <div>
                      <p className="text-sm font-semibold">Idea mind map</p>
                      <p className="text-xs text-muted-foreground">See the exploration structure and key branches.</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={handleGenerateCanvasMindMap}
                        disabled={isGeneratingCanvasMindMap}
                      >
                        {isGeneratingCanvasMindMap ? "Generating..." : canvasMindMap ? "Regenerate" : "Generate"}
                      </Button>
                    </div>
                  </div>
                  <div className="flex-1 min-h-0">
                    {isGeneratingCanvasMindMap ? (
                      <div className="flex items-center justify-center h-full">
                        <div className="w-10 h-10 border-2 border-primary border-t-transparent rounded-full animate-spin" />
                      </div>
                    ) : canvasMindMapError ? (
                      <div className="flex flex-col items-center justify-center h-full p-6 text-center">
                        <p className="text-sm text-red-600 mb-3">{canvasMindMapError}</p>
                        <Button variant="outline" size="sm" onClick={handleGenerateCanvasMindMap}>
                          Retry
                        </Button>
                      </div>
                    ) : canvasMindMap ? (
                      <MindMapViewer
                        tree={{
                          title: canvasMindMap.title,
                          summary: canvasMindMap.summary,
                          source_count: canvasMindMap.source_count,
                          mode: canvasMindMap.mode,
                          nodes: canvasMindMap.nodes as import("@/lib/types/mindmap").MindMapNode,
                        }}
                        onReset={() => setCanvasMindMap(null)}
                      />
                    ) : (
                      <div className="flex items-center justify-center h-full text-muted-foreground text-sm">
                        Click Generate to create mind map
                      </div>
                    )}
                  </div>
                </div>
              </TabsContent>
            </Tabs>
          </div>
        </main>
      </div>
    );
  }

  // ============================================================================
  // VIEW 4: Q&A View (Active Questioning)
  // ============================================================================
  return (
    <div className="fixed inset-0 z-50 bg-gradient-to-br from-amber-50/30 via-white to-orange-50/20 dark:from-slate-950 dark:via-slate-900 dark:to-amber-950/10">
      {modalLayer}
      <div className="h-14 border-b bg-white/80 dark:bg-slate-900/80 backdrop-blur-md flex items-center justify-between px-6">
        <div className="flex items-center gap-4">
          <button
            onClick={handleExitToSummary}
            className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            Finish & Continue
          </button>
          <div className="h-6 w-px bg-border" />
          <span className="font-medium text-amber-600 dark:text-amber-400">
            {canvas?.idea.slice(0, 40)}{(canvas?.idea.length || 0) > 40 ? "..." : ""}
          </span>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm" onClick={() => setShowApiKeyModal(true)}>
            <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
            </svg>
            API Keys
          </Button>
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber-100 dark:bg-amber-900/50">
            <div className="w-2 h-2 rounded-full bg-amber-500 animate-pulse" />
            <span className="text-sm font-medium text-amber-700 dark:text-amber-300">
              Question {Math.max(activeQuestionNumber, 1)} of ~{estimatedTotalQuestions}
            </span>
          </div>
        </div>
      </div>

      <div className="h-[calc(100vh-3.5rem)] flex flex-col lg:flex-row">
        {/* Left Panel - Questions */}
        <div className="w-full lg:flex-[0_0_70%] border-b lg:border-b-0 lg:border-r bg-gradient-to-b from-white to-amber-50/30 dark:from-slate-900 dark:to-slate-900 flex flex-col">
          <div className="px-6 lg:px-8 pt-5 pb-4 border-b bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm">
            <div className="mx-auto w-full max-w-4xl">
              <div className="flex items-center justify-between text-xs text-muted-foreground mb-2">
                <span className="font-medium text-foreground/80">Exploration Progress</span>
                <span>
                  {Math.max(activeQuestionNumber, 1)} / ~{estimatedTotalQuestions}
                </span>
              </div>
              <div className="h-1.5 rounded-full bg-amber-100 dark:bg-amber-900/40 overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-amber-400 to-orange-500 transition-all duration-500"
                  style={{ width: `${Math.max(progressFraction * 100, 6)}%` }}
                />
              </div>
            </div>
          </div>
          <div className="flex-1 overflow-y-auto p-6 lg:p-10">
            {currentQuestion ? (
              <div className="mx-auto w-full max-w-4xl">
                <QuestionCard
                  question={currentQuestion}
                  onAnswer={handleCanvasAnswer}
                  onSkip={currentQuestion.allow_skip ? () => handleCanvasAnswer("Skipped") : undefined}
                  isAnswering={canvasState === "answering"}
                />
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-full">
                <div className="w-10 h-10 border-3 border-amber-500 border-t-transparent rounded-full animate-spin mb-4" />
                <p className="text-sm text-muted-foreground">{canvasProgressMessage || "Loading..."}</p>
              </div>
            )}
          </div>
        </div>

        {/* Right Panel - Progress Visualization */}
        <div className="w-full lg:flex-[0_0_30%] min-h-[300px] lg:min-h-0 border-t lg:border-t-0 bg-gradient-to-br from-amber-50/80 via-orange-50/40 to-white dark:from-slate-900 dark:via-slate-900 dark:to-amber-950/20 p-6 lg:p-10 flex items-center justify-center">
          <div className="w-full max-w-xl lg:max-w-none">
            <div className="relative rounded-3xl border border-amber-200/70 dark:border-amber-800/40 bg-white/90 dark:bg-slate-900/90 shadow-[0_20px_60px_-30px_rgba(245,158,11,0.35)] p-6 lg:p-9 text-center overflow-hidden">
              <div className="pointer-events-none absolute -top-16 -right-16 w-48 h-48 rounded-full bg-gradient-to-br from-amber-200/60 to-orange-200/40 blur-3xl" />
              {/* Visual Progress Indicator */}
              <div className="relative mb-9">
                <div className="w-36 h-36 mx-auto relative">
                  {/* Outer ring */}
                  <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
                    <circle
                      cx="50"
                      cy="50"
                      r="45"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="6"
                      className="text-amber-100 dark:text-amber-900/30"
                    />
                    <circle
                      cx="50"
                      cy="50"
                      r="45"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="6"
                      strokeLinecap="round"
                      className="text-amber-500"
                      strokeDasharray={progressDasharray}
                      style={{ transition: "stroke-dasharray 0.5s ease" }}
                    />
                  </svg>
                  {/* Center content */}
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-4xl font-bold text-amber-600 dark:text-amber-400">{Math.max(activeQuestionNumber, 1)}</span>
                    <span className="text-xs text-muted-foreground">of ~{estimatedTotalQuestions}</span>
                  </div>
                </div>
              </div>

              <h2 className="text-xl font-semibold mb-2.5">Understanding Your Idea</h2>
              <p className="text-muted-foreground text-sm mb-7">
                Answer the questions to help us understand your idea better.
                Once we have enough context, we will generate implementation approaches.
              </p>

              <div className="mt-6 text-left rounded-2xl border border-amber-200/70 dark:border-amber-800/40 bg-white/95 dark:bg-slate-800/95 p-4 shadow-sm">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="text-xs font-semibold uppercase tracking-wide text-amber-700 dark:text-amber-300">
                    Idea Snapshot
                  </h4>
                  <span className="text-[11px] text-muted-foreground">
                    {questionHistory.length} captured
                  </span>
                </div>
                {snapshotThemes.length > 0 ? (
                  <div className="space-y-3">
                    {snapshotThemes.map((item, i) => (
                      <div key={`${item.label}-${i}`} className="rounded-xl border border-amber-100/80 dark:border-amber-900/40 bg-amber-50/40 dark:bg-slate-900/40 p-3 text-sm">
                        <div className="flex items-center justify-between mb-1.5">
                          <span className="text-[11px] font-semibold uppercase tracking-wide text-amber-700 dark:text-amber-300">
                            {item.label}
                          </span>
                        </div>
                        <p className="text-xs text-muted-foreground mb-1">{item.question}</p>
                        <p className="text-foreground leading-snug break-words">{item.answer}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-muted-foreground">
                    Your answers will appear here as we learn more about the idea.
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
