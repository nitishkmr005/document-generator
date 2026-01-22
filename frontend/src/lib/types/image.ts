/**
 * TypeScript types for image generation and editing features.
 */

import type { StyleCategory } from "@/data/imageStyles";
import type { Provider, SourceItem } from "@/lib/types/requests";

// Output format for generated images
export type OutputFormat = "raster" | "svg";

// Edit mode for image editing
export type EditMode = "basic" | "style_transfer" | "region";

// Region coordinates for regional editing (normalized 0-1)
export interface Region {
  x: number;
  y: number;
  width: number;
  height: number;
}

// Request for image generation
export interface ImageGenerateRequest {
  prompt?: string;
  sources?: SourceItem[];
  provider?: Provider;
  model?: string;
  style_category?: StyleCategory | null;
  style?: string | null;
  output_format: OutputFormat;
  free_text_mode: boolean;
}

// Request for image editing
export interface ImageEditRequest {
  image: string; // Base64 encoded
  prompt: string;
  edit_mode: EditMode;
  style_category?: StyleCategory | null;
  style?: string | null;
  region?: Region | null;
}

// Response for image generation
export interface ImageGenerateResponse {
  success: boolean;
  image_data: string | null;
  format: "png" | "svg";
  prompt_used: string;
  error: string | null;
}

// Response for image editing
export interface ImageEditResponse {
  success: boolean;
  image_data: string | null;
  format: "png";
  error: string | null;
}

// State for image generation/editing operations
export type ImageOperationState =
  | "idle"
  | "generating"
  | "editing"
  | "success"
  | "error";

// Generation result
export interface ImageResult {
  imageData: string;
  format: "png" | "svg";
  promptUsed: string;
}

// Edit result
export interface ImageEditResult {
  imageData: string;
  format: "png";
}
