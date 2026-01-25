// frontend/src/components/idea-canvas/ApproachTabs.tsx

"use client";

import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Approach, RefinementTarget } from "@/lib/types/idea-canvas";
import { ApproachPanel } from "./ApproachPanel";

interface ApproachTabsProps {
  approaches: Approach[];
  onElementClick?: (target: RefinementTarget) => void;
  refinementTarget?: RefinementTarget;
  isLoading?: boolean;
}

export function ApproachTabs({
  approaches,
  onElementClick,
  refinementTarget,
  isLoading = false,
}: ApproachTabsProps) {
  const [activeTab, setActiveTab] = useState(approaches[0]?.id || "");

  if (isLoading) {
    return (
      <div className="h-full flex flex-col items-center justify-center p-8">
        <div className="w-12 h-12 border-3 border-primary border-t-transparent rounded-full animate-spin mb-4" />
        <p className="text-sm text-muted-foreground">Generating implementation approaches...</p>
        <p className="text-xs text-muted-foreground/70 mt-1">This may take a moment</p>
      </div>
    );
  }

  if (approaches.length === 0) {
    return (
      <div className="h-full flex flex-col items-center justify-center p-8 text-center">
        <div className="w-16 h-16 rounded-full bg-muted/50 flex items-center justify-center mb-4">
          <svg className="w-8 h-8 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-muted-foreground mb-2">No Approaches Yet</h3>
        <p className="text-sm text-muted-foreground/70 max-w-xs">
          Complete the Q&A to see implementation approaches
        </p>
      </div>
    );
  }

  return (
    <Tabs value={activeTab} onValueChange={setActiveTab} className="h-full flex flex-col">
      <div className="px-4 pt-3 shrink-0">
        <TabsList className="w-full grid grid-cols-4 h-10 bg-muted/50">
          {approaches.map((approach) => (
            <TabsTrigger
              key={approach.id}
              value={approach.id}
              className="text-xs font-medium data-[state=active]:bg-background data-[state=active]:shadow-sm"
            >
              {approach.name}
            </TabsTrigger>
          ))}
        </TabsList>
      </div>

      {approaches.map((approach, index) => (
        <TabsContent
          key={approach.id}
          value={approach.id}
          className="flex-1 min-h-0 m-0 mt-0 data-[state=inactive]:hidden"
        >
          <ApproachPanel
            approach={approach}
            approachIndex={index}
            onElementClick={onElementClick}
            refinementTarget={refinementTarget}
          />
        </TabsContent>
      ))}
    </Tabs>
  );
}
