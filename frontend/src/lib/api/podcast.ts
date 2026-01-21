// frontend/src/lib/api/podcast.ts

import { getApiUrl } from "@/config/api";
import { PodcastRequest, PodcastEvent } from "@/lib/types/podcast";
import { Provider } from "@/lib/types/requests";

export interface GeneratePodcastOptions {
  request: PodcastRequest;
  apiKey: string;
  /**
   * Gemini API key for TTS synthesis. Required for podcast generation
   * even when using a different provider for script generation.
   * Falls back to apiKey if not provided (works when provider is Gemini).
   */
  geminiApiKey?: string;
  userId?: string;
  onEvent: (event: PodcastEvent) => void;
  onError: (error: Error) => void;
}

function getApiKeyHeader(provider: Provider): string {
  switch (provider) {
    case "gemini":
    case "google":
      return "X-Google-Key";
    case "openai":
      return "X-OpenAI-Key";
    case "anthropic":
      return "X-Anthropic-Key";
    default:
      return "X-Google-Key";
  }
}

export async function generatePodcast(options: GeneratePodcastOptions): Promise<void> {
  const { request, apiKey, geminiApiKey, userId, onEvent, onError } = options;

  const providerKeyHeader = getApiKeyHeader(request.provider);
  
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    // Provider-specific key for script generation
    [providerKeyHeader]: apiKey,
    // Gemini key for TTS - use provided geminiApiKey or fall back to apiKey
    // (works when user's provider is already Gemini)
    "X-Google-Key": geminiApiKey || apiKey,
  };

  if (userId) {
    headers["X-User-Id"] = userId;
  }

  const url = getApiUrl("/api/unified/generate/podcast");

  try {
    const response = await fetch(url, {
      method: "POST",
      headers,
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorText = await response.text();
      // Parse error for better message
      try {
        const errorJson = JSON.parse(errorText);
        throw new Error(errorJson.detail || `Podcast generation failed: ${errorText}`);
      } catch {
        throw new Error(`Podcast generation failed: ${errorText}`);
      }
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error("No response body");
    }

    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const data = line.slice(6).trim();
          if (data && data !== "[DONE]") {
            try {
              const event = JSON.parse(data) as PodcastEvent;
              onEvent(event);
            } catch {
              // Ignore parse errors for partial data
            }
          }
        }
      }
    }
  } catch (error) {
    onError(error instanceof Error ? error : new Error(String(error)));
  }
}
