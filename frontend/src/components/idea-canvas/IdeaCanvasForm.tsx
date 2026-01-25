// frontend/src/components/idea-canvas/IdeaCanvasForm.tsx

"use client";

import { useState, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  CanvasTemplate,
  StartCanvasRequest,
  CANVAS_TEMPLATES,
} from "@/lib/types/idea-canvas";
import { useApiKeys } from "@/hooks/useApiKeys";

interface IdeaCanvasFormProps {
  onSubmit: (
    request: StartCanvasRequest,
    contentApiKey: string,
    imageApiKey: string | null,
    includeReportImage: boolean
  ) => void;
  isStarting?: boolean;
  onConfigureKeys?: () => void;
}

const templateIcons: Record<string, React.ReactNode> = {
  rocket: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15.59 14.37a6 6 0 01-5.84 7.38v-4.8m5.84-2.58a14.98 14.98 0 006.16-12.12A14.98 14.98 0 009.631 8.41m5.96 5.96a14.926 14.926 0 01-5.841 2.58m-.119-8.54a6 6 0 00-7.381 5.84h4.8m2.581-5.84a14.927 14.927 0 00-2.58 5.84m2.699 2.7c-.103.021-.207.041-.311.06a15.09 15.09 0 01-2.448-2.448 14.9 14.9 0 01.06-.312m-2.24 2.39a4.493 4.493 0 00-1.757 4.306 4.493 4.493 0 004.306-1.758M16.5 9a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0z" />
    </svg>
  ),
  code: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17.25 6.75L22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3l-4.5 16.5" />
    </svg>
  ),
  bot: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8.25 3v1.5M4.5 8.25H3m18 0h-1.5M4.5 12H3m18 0h-1.5m-15 3.75H3m18 0h-1.5M8.25 19.5V21M12 3v1.5m0 15V21m3.75-18v1.5m0 15V21m-9-1.5h10.5a2.25 2.25 0 002.25-2.25V6.75a2.25 2.25 0 00-2.25-2.25H6.75A2.25 2.25 0 004.5 6.75v10.5a2.25 2.25 0 002.25 2.25zm.75-12h9v9h-9v-9z" />
    </svg>
  ),
  clipboard: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z" />
    </svg>
  ),
  layers: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M6.429 9.75L2.25 12l4.179 2.25m0-4.5l5.571 3 5.571-3m-11.142 0L2.25 7.5 12 2.25l9.75 5.25-4.179 2.25m0 0L21.75 12l-4.179 2.25m0 0l4.179 2.25L12 21.75 2.25 16.5l4.179-2.25m11.142 0l-5.571 3-5.571-3" />
    </svg>
  ),
  sparkles: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
    </svg>
  ),
  wrench: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21.75 6.75a4.5 4.5 0 01-4.884 4.484c-1.076-.091-2.264.071-2.95.904l-7.152 8.684a2.548 2.548 0 11-3.586-3.586l8.684-7.152c.833-.686.995-1.874.904-2.95a4.5 4.5 0 016.336-4.486l-3.276 3.276a3.004 3.004 0 002.25 2.25l3.276-3.276c.256.565.398 1.192.398 1.852z" />
    </svg>
  ),
  lightbulb: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 18v-5.25m0 0a6.01 6.01 0 001.5-.189m-1.5.189a6.01 6.01 0 01-1.5-.189m3.75 7.478a12.06 12.06 0 01-4.5 0m3.75 2.383a14.406 14.406 0 01-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 10-7.517 0c.85.493 1.509 1.333 1.509 2.316V18" />
    </svg>
  ),
  zap: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
    </svg>
  ),
  "trending-up": (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941" />
    </svg>
  ),
  shield: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
    </svg>
  ),
  "folder-tree": (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3.75 9.776c.112-.017.227-.026.344-.026h15.812c.117 0 .232.009.344.026m-16.5 0a2.25 2.25 0 00-1.883 2.542l.857 6a2.25 2.25 0 002.227 1.932H19.05a2.25 2.25 0 002.227-1.932l.857-6a2.25 2.25 0 00-1.883-2.542m-16.5 0V6A2.25 2.25 0 016 3.75h3.879a1.5 1.5 0 011.06.44l2.122 2.12a1.5 1.5 0 001.06.44H18A2.25 2.25 0 0120.25 9v.776" />
    </svg>
  ),
};

export function IdeaCanvasForm({ onSubmit, isStarting = false, onConfigureKeys }: IdeaCanvasFormProps) {
  const [selectedTemplate, setSelectedTemplate] = useState<CanvasTemplate | null>(null);
  const [idea, setIdea] = useState("");

  const {
    provider,
    contentModel,
    contentApiKey,
    effectiveImageKey,
    hasContentKey,
    enableImageGeneration,
    isLoaded
  } = useApiKeys();

  const handleTemplateClick = useCallback((template: CanvasTemplate) => {
    setSelectedTemplate(template);
  }, []);

  const handleSubmit = useCallback(
    (e: React.FormEvent) => {
      e.preventDefault();
      if (!contentApiKey.trim() || !idea.trim()) return;

      const request: StartCanvasRequest = {
        template: selectedTemplate || "custom",
        idea: idea.trim(),
        provider,
        model: contentModel,
      };

      onSubmit(
        request,
        contentApiKey,
        enableImageGeneration ? effectiveImageKey : null,
        enableImageGeneration
      );
    },
    [selectedTemplate, idea, provider, contentModel, contentApiKey, enableImageGeneration, effectiveImageKey, onSubmit]
  );

  const getPlaceholderText = () => {
    if (!selectedTemplate) return "Describe your idea, project, or what you want to build...";
    switch (selectedTemplate) {
      case "startup":
        return "Describe your startup idea... e.g., 'A platform that helps remote teams collaborate better'";
      case "web_app":
        return "Describe the web app you want to build... e.g., 'A task management app with team collaboration'";
      case "ai_agent":
        return "Describe the AI agent you want to create... e.g., 'A research assistant that summarizes papers'";
      case "project_spec":
        return "Describe your project... e.g., 'Build a customer feedback system for our product'";
      case "tech_stack":
        return "Describe what you're building and your constraints... e.g., 'E-commerce site, need to handle 10k users'";
      case "implement_feature":
        return "Describe the feature you want to implement... e.g., 'Add user authentication with OAuth and email login'";
      case "solve_problem":
        return "Describe the problem you're trying to solve... e.g., 'Need to handle file uploads for large files efficiently'";
      case "performance":
        return "Describe the performance issue... e.g., 'API response times are slow, p95 is 2s'";
      case "scaling":
        return "Describe what you need to scale... e.g., 'Database hitting limits at 10k concurrent users'";
      case "security_review":
        return "Describe what you want to secure... e.g., 'Review authentication system for vulnerabilities'";
      case "code_architecture":
        return "Describe your codebase situation... e.g., 'Monolith becoming hard to maintain, considering refactor'";
      default:
        return "Describe your idea...";
    }
  };

  if (!isLoaded) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="w-6 h-6 border-2 border-amber-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-8">
      {/* API Key Status */}
      {!hasContentKey && (
        <div className="p-4 rounded-2xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800">
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-100 dark:bg-amber-900/50 flex items-center justify-center shrink-0">
              <svg className="w-5 h-5 text-amber-600 dark:text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
              </svg>
            </div>
            <div className="flex-1">
              <h4 className="font-semibold text-amber-800 dark:text-amber-200 text-sm">API Key Required</h4>
              <p className="text-sm text-amber-700 dark:text-amber-300 mt-0.5">
                Configure your API keys in the Studio settings to start exploring ideas.
              </p>
              {onConfigureKeys && (
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={onConfigureKeys}
                  className="mt-3 border-amber-300 dark:border-amber-700 text-amber-700 dark:text-amber-300 hover:bg-amber-100 dark:hover:bg-amber-900/50"
                >
                  Configure API Keys
                </Button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Template Selection */}
      <section>
        <div className="mb-4">
          <h3 className="text-lg font-semibold text-foreground">Choose a Starting Point</h3>
          <p className="text-sm text-muted-foreground mt-0.5">Select a template to guide your exploration</p>
        </div>
        <div className="grid grid-cols-2 gap-2">
          {CANVAS_TEMPLATES.slice(0, 6).map((template) => (
            <button
              key={template.id}
              type="button"
              onClick={() => handleTemplateClick(template.id)}
              className={`group relative flex items-center gap-3 p-3 rounded-xl border text-left transition-all duration-200 ${
                selectedTemplate === template.id
                  ? "border-amber-400 bg-amber-50 dark:bg-amber-950/30 ring-1 ring-amber-400/50"
                  : "border-border/60 hover:border-amber-300 hover:bg-amber-50/50 dark:hover:bg-amber-950/20"
              }`}
            >
              <div className={`shrink-0 p-2 rounded-lg transition-all duration-200 ${
                selectedTemplate === template.id
                  ? "bg-amber-500 text-white"
                  : "bg-muted/50 text-muted-foreground group-hover:bg-amber-100 group-hover:text-amber-600 dark:group-hover:bg-amber-900/50 dark:group-hover:text-amber-400"
              }`}>
                {templateIcons[template.icon]}
              </div>
              <div className="min-w-0 flex-1">
                <div className="font-medium text-sm">{template.title}</div>
                <div className="text-xs text-muted-foreground mt-0.5 line-clamp-1">
                  {template.description}
                </div>
              </div>
            </button>
          ))}
        </div>
      </section>

      {/* Idea Input */}
      <section>
        <div className="mb-3">
          <h3 className="text-lg font-semibold text-foreground">Your Idea</h3>
          <p className="text-sm text-muted-foreground mt-0.5">Describe what you want to explore</p>
        </div>
        <Textarea
          placeholder={getPlaceholderText()}
          rows={4}
          value={idea}
          onChange={(e) => setIdea(e.target.value)}
          className="resize-none text-base bg-background border-border/60 focus:border-amber-400 focus:ring-amber-400/20 rounded-xl"
        />
      </section>

      {/* Submit Button */}
      <Button
        type="submit"
        size="lg"
        className="w-full h-14 text-base font-semibold bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white shadow-lg shadow-amber-500/25 hover:shadow-amber-500/40 transition-all duration-200 rounded-xl"
        disabled={isStarting || !idea.trim() || !hasContentKey}
      >
        {isStarting ? (
          <>
            <svg className="w-5 h-5 mr-2 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            Starting Exploration...
          </>
        ) : (
          <>
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Start Exploring
          </>
        )}
      </Button>

      {/* Model Info */}
      {hasContentKey && (
        <p className="text-center text-xs text-muted-foreground">
          Using <span className="font-medium">{contentModel}</span> via {provider}
        </p>
      )}
    </form>
  );
}
