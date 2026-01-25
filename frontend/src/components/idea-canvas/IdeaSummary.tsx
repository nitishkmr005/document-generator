// frontend/src/components/idea-canvas/IdeaSummary.tsx

"use client";

import { QuestionHistoryItem } from "@/hooks/useIdeaCanvas";

interface IdeaSummaryProps {
  idea: string;
  questionHistory: QuestionHistoryItem[];
}

export function IdeaSummary({ idea, questionHistory }: IdeaSummaryProps) {
  return (
    <div className="h-full flex flex-col p-6">
      <div className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Your Idea Summary</h2>
        <p className="text-sm text-muted-foreground leading-relaxed">
          {idea}
        </p>
      </div>

      <div className="border-t pt-4 flex-1 overflow-auto">
        <h3 className="text-sm font-medium mb-3 text-muted-foreground">Answers:</h3>
        <ul className="space-y-2">
          {questionHistory.map((item, index) => {
            const answerText = Array.isArray(item.answer)
              ? item.answer.join(", ")
              : item.answer;
            return (
              <li key={index} className="flex items-start gap-2 text-sm">
                <span className="text-primary font-medium shrink-0">•</span>
                <span className="text-foreground">{answerText}</span>
              </li>
            );
          })}
        </ul>
      </div>

      <div className="mt-4 pt-4 border-t">
        <p className="text-xs text-muted-foreground text-center">
          Click any element in the approaches to refine it.
        </p>
      </div>
    </div>
  );
}
