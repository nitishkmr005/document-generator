// frontend/src/components/mindmap/MindMapForm.tsx

"use client";

import { useState, useCallback, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Provider, SourceItem } from "@/lib/types/requests";
import { MindMapMode } from "@/lib/types/mindmap";
import { useUpload, UploadedFile } from "@/hooks/useUpload";

interface MindMapFormProps {
  onSubmit: (
    sources: SourceItem[],
    options: {
      mode: MindMapMode;
      provider: Provider;
      model: string;
    },
    apiKey: string
  ) => void;
  isGenerating?: boolean;
}

const contentModelOptions: Record<Provider, { value: string; label: string }[]> = {
  gemini: [
    { value: "gemini-2.5-flash", label: "gemini-2.5-flash" },
    { value: "gemini-2.5-flash-lite", label: "gemini-2.5-flash-lite" },
    { value: "gemini-2.5-pro", label: "gemini-2.5-pro" },
  ],
  openai: [
    { value: "gpt-4.1-mini", label: "gpt-4.1-mini" },
    { value: "gpt-4.1", label: "gpt-4.1" },
  ],
  anthropic: [
    { value: "claude-haiku-4-5-20251001", label: "claude-haiku-4-5" },
    { value: "claude-sonnet-4-5-20250929", label: "claude-sonnet-4-5" },
  ],
  google: [
    { value: "gemini-2.5-flash", label: "gemini-2.5-flash" },
  ],
};

export function MindMapForm({ onSubmit, isGenerating = false }: MindMapFormProps) {
  const [sourceTab, setSourceTab] = useState<"url" | "upload" | "text">("url");
  const [urlInput, setUrlInput] = useState("");
  const [urls, setUrls] = useState<string[]>([]);
  const [textContent, setTextContent] = useState("");
  const { uploading, uploadedFiles, error: uploadError, uploadFile, removeFile } = useUpload();
  const hasFile = uploadedFiles.length > 0;
  const hasUrl = urls.length > 0;
  const hasText = textContent.trim().length > 0;
  const hasSources = hasFile || hasUrl || hasText;

  const [mode, setMode] = useState<MindMapMode>("summarize");
  const [provider, setProvider] = useState<Provider>("gemini");
  const [model, setModel] = useState("gemini-2.5-flash");
  const [apiKey, setApiKey] = useState("");

  // Update model when provider changes
  useEffect(() => {
    const options = contentModelOptions[provider] || [];
    if (options.length > 0 && !options.some(opt => opt.value === model)) {
      setModel(options[0].value);
    }
  }, [provider, model]);

  const handleFileChange = useCallback(
    async (e: React.ChangeEvent<HTMLInputElement>) => {
      if (hasSources) {
        return;
      }
      const file = e.target.files?.[0];
      if (!file) {
        return;
      }
      await uploadFile(file);
    },
    [hasSources, uploadFile]
  );

  const handleAddUrl = useCallback(() => {
    if (hasSources) {
      return;
    }
    const trimmed = urlInput.trim();
    if (trimmed) {
      setUrls([trimmed]);
      setUrlInput("");
    }
  }, [hasSources, urlInput]);

  const handleRemoveUrl = useCallback((url: string) => {
    setUrls((prev) => prev.filter((u) => u !== url));
  }, []);

  const handleSubmit = useCallback(
    (e: React.FormEvent) => {
      e.preventDefault();

      if (!apiKey.trim()) return;

      const sources: SourceItem[] = [];

      uploadedFiles.forEach((f: UploadedFile) => {
        sources.push({ type: "file", file_id: f.fileId });
      });

      urls.forEach((url) => {
        sources.push({ type: "url", url });
      });

      if (textContent.trim()) {
        sources.push({ type: "text", content: textContent.trim() });
      }

      if (sources.length === 0) return;

      onSubmit(sources, { mode, provider, model }, apiKey);
    },
    [apiKey, uploadedFiles, urls, textContent, mode, provider, model, onSubmit]
  );

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Sources</CardTitle>
          <CardDescription>
            Add one source to generate a mind map from (file, URL, or text).
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Tabs value={sourceTab} onValueChange={(v) => setSourceTab(v as typeof sourceTab)}>
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="url">URL</TabsTrigger>
              <TabsTrigger value="upload">Upload</TabsTrigger>
              <TabsTrigger value="text">Text</TabsTrigger>
            </TabsList>

            <TabsContent value="url" className="space-y-3">
              <div className="flex gap-2">
                <Input
                  type="url"
                  placeholder="https://example.com/article"
                  value={urlInput}
                  onChange={(e) => setUrlInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();
                      handleAddUrl();
                    }
                  }}
                  disabled={hasSources}
                />
                <Button type="button" variant="secondary" onClick={handleAddUrl} disabled={hasSources}>
                  Add
                </Button>
              </div>
              {urls.length > 0 && (
                <div className="space-y-2">
                  {urls.map((url) => (
                    <div
                      key={url}
                      className="flex items-center justify-between rounded-md border px-3 py-2 text-sm"
                    >
                      <span className="truncate max-w-[300px]">{url}</span>
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={() => handleRemoveUrl(url)}
                      >
                        ×
                      </Button>
                    </div>
                  ))}
                </div>
              )}
            </TabsContent>

            <TabsContent value="upload" className="space-y-3">
              <Input
                type="file"
                onChange={handleFileChange}
                disabled={uploading || hasSources}
                accept=".pdf,.md,.txt,.docx"
              />
              {uploading && <p className="text-sm text-muted-foreground">Uploading...</p>}
              {uploadError && <p className="text-sm text-red-500">{uploadError}</p>}
              {uploadedFiles.length > 0 && (
                <div className="space-y-2">
                  {uploadedFiles.map((f) => (
                    <div
                      key={f.fileId}
                      className="flex items-center justify-between rounded-md border px-3 py-2 text-sm"
                    >
                      <span className="truncate max-w-[300px]">{f.filename}</span>
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={() => removeFile(f.fileId)}
                      >
                        ×
                      </Button>
                    </div>
                  ))}
                </div>
              )}
            </TabsContent>

            <TabsContent value="text" className="space-y-3">
              <Textarea
                placeholder="Paste your content here..."
                rows={6}
                value={textContent}
                onChange={(e) => setTextContent(e.target.value)}
                disabled={hasSources && !hasText}
              />
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Generation Mode</CardTitle>
          <CardDescription>Choose how you want to transform your content</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {/* Understand Fast (Summarize) */}
            <button
              type="button"
              onClick={() => setMode("summarize")}
              className={`group flex flex-col items-start p-4 rounded-xl border text-left transition-all ${
                mode === "summarize"
                  ? "border-primary bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/40 dark:to-indigo-950/40 ring-2 ring-primary shadow-md"
                  : "border-border hover:border-primary/50 hover:shadow-sm hover:bg-muted/50"
              }`}
            >
              <div className={`p-2.5 rounded-lg mb-3 ${mode === "summarize" ? "bg-blue-100 dark:bg-blue-900/50" : "bg-muted"}`}>
                <span className="text-xl">📘</span>
              </div>
              <div className="font-semibold text-sm mb-1.5">Understand Fast</div>
              <div className="text-xs text-muted-foreground leading-relaxed">
                Turn PDFs, articles, or URLs into a clean map of key ideas
              </div>
              <div className="flex flex-wrap gap-1 mt-3">
                <span className="px-2 py-0.5 text-[10px] rounded-full bg-muted text-muted-foreground">Research papers</span>
                <span className="px-2 py-0.5 text-[10px] rounded-full bg-muted text-muted-foreground">Articles</span>
              </div>
            </button>

            {/* Brainstorm Ideas */}
            <button
              type="button"
              onClick={() => setMode("brainstorm")}
              className={`group flex flex-col items-start p-4 rounded-xl border text-left transition-all ${
                mode === "brainstorm"
                  ? "border-primary bg-gradient-to-br from-amber-50 to-yellow-50 dark:from-amber-950/40 dark:to-yellow-950/40 ring-2 ring-primary shadow-md"
                  : "border-border hover:border-primary/50 hover:shadow-sm hover:bg-muted/50"
              }`}
            >
              <div className={`p-2.5 rounded-lg mb-3 ${mode === "brainstorm" ? "bg-amber-100 dark:bg-amber-900/50" : "bg-muted"}`}>
                <span className="text-xl">💡</span>
              </div>
              <div className="font-semibold text-sm mb-1.5">Brainstorm Ideas</div>
              <div className="text-xs text-muted-foreground leading-relaxed">
                Expand a topic into use cases, variations & possibilities
              </div>
              <div className="flex flex-wrap gap-1 mt-3">
                <span className="px-2 py-0.5 text-[10px] rounded-full bg-muted text-muted-foreground">Startup ideas</span>
                <span className="px-2 py-0.5 text-[10px] rounded-full bg-muted text-muted-foreground">Features</span>
              </div>
            </button>

            {/* Create Action Plan (Goal Planning) */}
            <button
              type="button"
              onClick={() => setMode("goal_planning")}
              className={`group flex flex-col items-start p-4 rounded-xl border text-left transition-all ${
                mode === "goal_planning"
                  ? "border-primary bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-emerald-950/40 dark:to-teal-950/40 ring-2 ring-primary shadow-md"
                  : "border-border hover:border-primary/50 hover:shadow-sm hover:bg-muted/50"
              }`}
            >
              <div className={`p-2.5 rounded-lg mb-3 ${mode === "goal_planning" ? "bg-emerald-100 dark:bg-emerald-900/50" : "bg-muted"}`}>
                <span className="text-xl">🎯</span>
              </div>
              <div className="font-semibold text-sm mb-1.5">Create Action Plan</div>
              <div className="text-xs text-muted-foreground leading-relaxed">
                Turn an idea into phases, steps & milestones
              </div>
              <div className="flex flex-wrap gap-1 mt-3">
                <span className="px-2 py-0.5 text-[10px] rounded-full bg-muted text-muted-foreground">Projects</span>
                <span className="px-2 py-0.5 text-[10px] rounded-full bg-muted text-muted-foreground">Learning paths</span>
              </div>
            </button>

            {/* Analyze Pros & Cons */}
            <button
              type="button"
              onClick={() => setMode("pros_cons")}
              className={`group flex flex-col items-start p-4 rounded-xl border text-left transition-all ${
                mode === "pros_cons"
                  ? "border-primary bg-gradient-to-br from-violet-50 to-purple-50 dark:from-violet-950/40 dark:to-purple-950/40 ring-2 ring-primary shadow-md"
                  : "border-border hover:border-primary/50 hover:shadow-sm hover:bg-muted/50"
              }`}
            >
              <div className={`p-2.5 rounded-lg mb-3 ${mode === "pros_cons" ? "bg-violet-100 dark:bg-violet-900/50" : "bg-muted"}`}>
                <span className="text-xl">⚖️</span>
              </div>
              <div className="font-semibold text-sm mb-1.5">Analyze Pros & Cons</div>
              <div className="text-xs text-muted-foreground leading-relaxed">
                See tradeoffs, benefits & risks for better decisions
              </div>
              <div className="flex flex-wrap gap-1 mt-3">
                <span className="px-2 py-0.5 text-[10px] rounded-full bg-muted text-muted-foreground">Tech choices</span>
                <span className="px-2 py-0.5 text-[10px] rounded-full bg-muted text-muted-foreground">Decisions</span>
              </div>
            </button>

            {/* Presentation Structure */}
            <button
              type="button"
              onClick={() => setMode("presentation_structure")}
              className={`group flex flex-col items-start p-4 rounded-xl border text-left transition-all ${
                mode === "presentation_structure"
                  ? "border-primary bg-gradient-to-br from-rose-50 to-pink-50 dark:from-rose-950/40 dark:to-pink-950/40 ring-2 ring-primary shadow-md"
                  : "border-border hover:border-primary/50 hover:shadow-sm hover:bg-muted/50"
              }`}
            >
              <div className={`p-2.5 rounded-lg mb-3 ${mode === "presentation_structure" ? "bg-rose-100 dark:bg-rose-900/50" : "bg-muted"}`}>
                <span className="text-xl">📊</span>
              </div>
              <div className="font-semibold text-sm mb-1.5">Presentation Outline</div>
              <div className="text-xs text-muted-foreground leading-relaxed">
                Create logical structure for slides or documents
              </div>
              <div className="flex flex-wrap gap-1 mt-3">
                <span className="px-2 py-0.5 text-[10px] rounded-full bg-muted text-muted-foreground">Slides</span>
                <span className="px-2 py-0.5 text-[10px] rounded-full bg-muted text-muted-foreground">Articles</span>
              </div>
            </button>

            {/* Document Structure (keeping original) */}
            <button
              type="button"
              onClick={() => setMode("structure")}
              className={`group flex flex-col items-start p-4 rounded-xl border text-left transition-all ${
                mode === "structure"
                  ? "border-primary bg-gradient-to-br from-slate-50 to-gray-50 dark:from-slate-950/40 dark:to-gray-950/40 ring-2 ring-primary shadow-md"
                  : "border-border hover:border-primary/50 hover:shadow-sm hover:bg-muted/50"
              }`}
            >
              <div className={`p-2.5 rounded-lg mb-3 ${mode === "structure" ? "bg-slate-100 dark:bg-slate-900/50" : "bg-muted"}`}>
                <span className="text-xl">📋</span>
              </div>
              <div className="font-semibold text-sm mb-1.5">Document Structure</div>
              <div className="text-xs text-muted-foreground leading-relaxed">
                Visualize how a document is organized
              </div>
              <div className="flex flex-wrap gap-1 mt-3">
                <span className="px-2 py-0.5 text-[10px] rounded-full bg-muted text-muted-foreground">Documents</span>
                <span className="px-2 py-0.5 text-[10px] rounded-full bg-muted text-muted-foreground">Reports</span>
              </div>
            </button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>AI Settings</CardTitle>
          <CardDescription>Configure the AI model</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label>Provider</Label>
            <Select value={provider} onValueChange={(v) => setProvider(v as Provider)}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="gemini">Google Gemini</SelectItem>
                <SelectItem value="openai">OpenAI</SelectItem>
                <SelectItem value="anthropic">Anthropic</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label>Model</Label>
            <Select value={model} onValueChange={setModel}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {(contentModelOptions[provider] || []).map((opt) => (
                  <SelectItem key={opt.value} value={opt.value}>
                    {opt.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>API Key</CardTitle>
          <CardDescription>
            Enter your API key for the selected provider
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-2">
          <div className="flex items-center justify-between">
            <Label htmlFor="mindmap-api-key">API Key *</Label>
            {provider === "gemini" && (
              <a
                href="https://aistudio.google.com/apikey"
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-primary hover:underline flex items-center gap-1"
              >
                Get Gemini API Key
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </a>
            )}
            {provider === "openai" && (
              <a
                href="https://platform.openai.com/api-keys"
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-primary hover:underline flex items-center gap-1"
              >
                Get OpenAI API Key
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </a>
            )}
            {provider === "anthropic" && (
              <a
                href="https://console.anthropic.com/settings/keys"
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-primary hover:underline flex items-center gap-1"
              >
                Get Claude API Key
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </a>
            )}
          </div>
          <Input
            id="mindmap-api-key"
            type="password"
            placeholder={`Enter your ${provider === "gemini" ? "Gemini" : provider === "openai" ? "OpenAI" : "Claude"} API key`}
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            autoComplete="off"
          />
        </CardContent>
      </Card>

      <Button
        type="submit"
        size="lg"
        className="w-full"
        disabled={isGenerating || !hasSources || !apiKey.trim()}
      >
        {isGenerating ? "Generating..." : "Generate Mind Map"}
      </Button>
    </form>
  );
}
