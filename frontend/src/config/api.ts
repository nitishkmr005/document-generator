// Determine the correct API URL based on environment
// - Browser (client-side): use localhost:8000
// - Server (SSR/API routes): use backend:8000 (Docker network)
function getBaseUrl(): string {
  // Check if we're in the browser - must be checked at RUNTIME, not build time
  if (typeof window !== 'undefined') {
    // Browser should use localhost (or the host machine address)
    // Handle both Docker's 'backend' and direct configuration
    const envUrl = process.env.NEXT_PUBLIC_API_URL || '';
    if (envUrl.includes('backend')) {
      return envUrl.replace('backend', 'localhost');
    }
    return envUrl || 'http://localhost:8000';
  }
  // Server-side can use the Docker network hostname
  return process.env.NEXT_PUBLIC_API_URL || 'http://backend:8000';
}

export const API_CONFIG = {
  // NOTE: endpoints are static, but baseUrl must be dynamic
  endpoints: {
    health: "/api/health",
    upload: "/api/upload",
    generate: "/api/unified/generate",
    download: (filePath: string) => `/api/download/${filePath}`,
  },
} as const;

// IMPORTANT: This function is called at RUNTIME to get the correct URL
export function getApiUrl(endpoint: string): string {
  return `${getBaseUrl()}${endpoint}`;
}

export function getDownloadUrl(filePath: string): string {
  return getApiUrl(API_CONFIG.endpoints.download(filePath));
}
