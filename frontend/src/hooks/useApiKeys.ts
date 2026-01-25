// frontend/src/hooks/useApiKeys.ts

"use client";

import { useState, useEffect, useCallback } from "react";
import { Provider } from "@/lib/types/requests";

const STORAGE_KEY = "docgen_api_keys";

interface ApiKeyStore {
  provider: Provider;
  contentModel: string;
  contentApiKey: string;
  imageApiKey: string;
  imageModel: string;
  enableImageGeneration: boolean;
}

const DEFAULT_STORE: ApiKeyStore = {
  provider: "gemini",
  contentModel: "gemini-2.5-flash",
  contentApiKey: "",
  imageApiKey: "",
  imageModel: "gemini-2.5-flash-image",
  enableImageGeneration: true,
};

export function useApiKeys() {
  const [store, setStore] = useState<ApiKeyStore>(DEFAULT_STORE);
  const [isLoaded, setIsLoaded] = useState(false);

  // Load from localStorage on mount
  useEffect(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved) as Partial<ApiKeyStore>;
        setStore({ ...DEFAULT_STORE, ...parsed });
      }
    } catch {
      // Ignore parse errors
    }
    setIsLoaded(true);
  }, []);

  // Save to localStorage when store changes
  useEffect(() => {
    if (isLoaded) {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(store));
      } catch {
        // Ignore storage errors
      }
    }
  }, [store, isLoaded]);

  const setProvider = useCallback((provider: Provider) => {
    setStore((prev) => ({ ...prev, provider }));
  }, []);

  const setContentModel = useCallback((contentModel: string) => {
    setStore((prev) => ({ ...prev, contentModel }));
  }, []);

  const setContentApiKey = useCallback((contentApiKey: string) => {
    setStore((prev) => ({ ...prev, contentApiKey }));
  }, []);

  const setImageApiKey = useCallback((imageApiKey: string) => {
    setStore((prev) => ({ ...prev, imageApiKey }));
  }, []);

  const setImageModel = useCallback((imageModel: string) => {
    setStore((prev) => ({ ...prev, imageModel }));
  }, []);

  const setEnableImageGeneration = useCallback((enableImageGeneration: boolean) => {
    setStore((prev) => ({ ...prev, enableImageGeneration }));
  }, []);

  // Computed values
  const hasContentKey = store.contentApiKey.trim().length > 0;
  const effectiveImageKey = store.imageApiKey.trim() || (store.provider === "gemini" ? store.contentApiKey.trim() : "");
  const hasImageKey = effectiveImageKey.length > 0;

  return {
    ...store,
    isLoaded,
    hasContentKey,
    hasImageKey,
    effectiveImageKey,
    setProvider,
    setContentModel,
    setContentApiKey,
    setImageApiKey,
    setImageModel,
    setEnableImageGeneration,
  };
}
