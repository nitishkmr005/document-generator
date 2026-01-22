/**
 * API client for image generation and editing endpoints.
 */

import { getApiUrl } from "@/config/api";
import type {
  ImageGenerateRequest,
  ImageGenerateResponse,
  ImageEditRequest,
  ImageEditResponse,
} from "@/lib/types/image";
import { ApiClientError, formatErrorDetail } from "./client";
import { Provider } from "@/lib/types/requests";

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

/**
 * Generate an image from text description.
 *
 * @param request - Image generation request
 * @param apiKey - Gemini API key
 * @returns Image generation response
 */
export async function generateImage(
  request: ImageGenerateRequest,
  apiKey: string,
  options?: {
    provider?: Provider;
    contentApiKey?: string;
    userId?: string;
  }
): Promise<ImageGenerateResponse> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (apiKey) {
    headers["X-Gemini-API-Key"] = apiKey;
    headers["X-Image-Key"] = apiKey;
  }

  if (options?.provider && options?.contentApiKey) {
    headers[getApiKeyHeader(options.provider)] = options.contentApiKey;
  }

  if (options?.userId) {
    headers["X-User-Id"] = options.userId;
  }

  const response = await fetch(getApiUrl("/api/image/generate"), {
    method: "POST",
    headers,
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const errorMessage =
      formatErrorDetail(errorData.detail) ||
      `Image generation failed: ${response.statusText}`;
    throw new ApiClientError(errorMessage, errorData.code, response.status);
  }

  return response.json();
}

/**
 * Edit an existing image.
 *
 * @param request - Image edit request
 * @param apiKey - Gemini API key
 * @returns Image edit response
 */
export async function editImage(
  request: ImageEditRequest,
  apiKey: string
): Promise<ImageEditResponse> {
  const response = await fetch(getApiUrl("/api/image/edit"), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Gemini-API-Key": apiKey,
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const errorMessage =
      formatErrorDetail(errorData.detail) ||
      `Image editing failed: ${response.statusText}`;
    throw new ApiClientError(errorMessage, errorData.code, response.status);
  }

  return response.json();
}

/**
 * Convert a File to base64 string.
 *
 * @param file - File to convert
 * @returns Base64 encoded string (without data URL prefix)
 */
export function fileToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result as string;
      // Remove the data URL prefix (e.g., "data:image/png;base64,")
      const base64 = result.split(",")[1];
      resolve(base64);
    };
    reader.onerror = () => reject(new Error("Failed to read file"));
    reader.readAsDataURL(file);
  });
}

/**
 * Download image from base64 data.
 *
 * @param base64Data - Base64 encoded image data
 * @param filename - Filename for download
 * @param format - Image format (png or svg)
 */
export function downloadImage(
  base64Data: string,
  filename: string,
  format: "png" | "svg"
): void {
  let blob: Blob;
  let downloadFilename: string;

  if (format === "svg") {
    // SVG is text, not base64
    blob = new Blob([base64Data], { type: "image/svg+xml" });
    downloadFilename = filename.endsWith(".svg") ? filename : `${filename}.svg`;
  } else {
    // Convert base64 to blob for PNG
    const byteCharacters = atob(base64Data);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    blob = new Blob([byteArray], { type: "image/png" });
    downloadFilename = filename.endsWith(".png") ? filename : `${filename}.png`;
  }

  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = downloadFilename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
