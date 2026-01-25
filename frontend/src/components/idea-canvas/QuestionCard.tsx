// frontend/src/components/idea-canvas/QuestionCard.tsx

"use client";

import { useState, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  CanvasQuestion,
  QuestionOption,
  ApproachOption,
} from "@/lib/types/idea-canvas";

interface QuestionCardProps {
  question: CanvasQuestion;
  onAnswer: (answer: string | string[]) => void;
  onSkip?: () => void;
  isAnswering?: boolean;
}

export function QuestionCard({
  question,
  onAnswer,
  onSkip,
  isAnswering = false,
}: QuestionCardProps) {
  const [selectedOptions, setSelectedOptions] = useState<string[]>([]);
  const [textInput, setTextInput] = useState("");
  const [showCustomInput, setShowCustomInput] = useState(false);
  const [customInput, setCustomInput] = useState("");

  const handleOptionClick = useCallback(
    (optionId: string) => {
      if (question.type === "single_choice") {
        // Find the option label
        const option = question.options.find((opt) => opt.id === optionId);
        const label = option?.label || optionId;
        // Single selection - submit immediately
        onAnswer(label);
      } else if (question.type === "approach") {
        // Find the approach title
        const approach = question.approaches.find((appr) => appr.id === optionId);
        const title = approach?.title || optionId;
        onAnswer(title);
      } else if (question.type === "multi_choice") {
        // Multi selection - toggle
        setSelectedOptions((prev) =>
          prev.includes(optionId)
            ? prev.filter((id) => id !== optionId)
            : [...prev, optionId]
        );
      }
    },
    [question.type, question.options, question.approaches, onAnswer]
  );

  const handleSubmitMultiChoice = useCallback(() => {
    if (selectedOptions.length > 0) {
      // Convert option IDs to labels
      const labels = selectedOptions.map((optId) => {
        const option = question.options.find((opt) => opt.id === optId);
        return option?.label || optId;
      });
      onAnswer(labels);
    }
  }, [selectedOptions, question.options, onAnswer]);

  const handleSubmitTextInput = useCallback(() => {
    if (textInput.trim()) {
      onAnswer(textInput.trim());
    }
  }, [textInput, onAnswer]);

  const handleSubmitCustomInput = useCallback(() => {
    if (customInput.trim()) {
      onAnswer(customInput.trim());
    }
  }, [customInput, onAnswer]);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleSubmitTextInput();
      }
    },
    [handleSubmitTextInput]
  );

  const handleCustomKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleSubmitCustomInput();
      }
    },
    [handleSubmitCustomInput]
  );

  const renderOption = (option: QuestionOption) => (
    <button
      key={option.id}
      type="button"
      onClick={() => handleOptionClick(option.id)}
      disabled={isAnswering}
      className={`relative flex flex-col items-start p-4 rounded-lg border text-left transition-all hover:border-primary/50 hover:bg-primary/5 disabled:opacity-50 disabled:cursor-not-allowed ${
        selectedOptions.includes(option.id)
          ? "border-primary bg-primary/5 ring-1 ring-primary"
          : "border-border"
      }`}
    >
      {option.recommended && (
        <span className="absolute top-2 right-2 px-2 py-0.5 text-xs font-medium rounded-full bg-primary text-primary-foreground">
          Recommended
        </span>
      )}
      <div className="font-medium">{option.label}</div>
      {option.description && (
        <div className="text-sm text-muted-foreground mt-1">
          {option.description}
        </div>
      )}
    </button>
  );

  const renderApproach = (approach: ApproachOption) => (
    <button
      key={approach.id}
      type="button"
      onClick={() => handleOptionClick(approach.id)}
      disabled={isAnswering}
      className={`relative flex flex-col items-start p-4 rounded-lg border text-left transition-all hover:border-primary/50 hover:bg-primary/5 disabled:opacity-50 disabled:cursor-not-allowed ${
        selectedOptions.includes(approach.id)
          ? "border-primary bg-primary/5 ring-1 ring-primary"
          : "border-border"
      }`}
    >
      {approach.recommended && (
        <span className="absolute top-2 right-2 px-2 py-0.5 text-xs font-medium rounded-full bg-primary text-primary-foreground">
          Recommended
        </span>
      )}
      <div className="font-semibold text-base">{approach.title}</div>
      <div className="text-sm text-muted-foreground mt-1 mb-3">
        {approach.description}
      </div>
      <div className="w-full grid grid-cols-2 gap-3 text-xs">
        <div>
          <div className="font-medium text-green-600 dark:text-green-400 mb-1">
            Pros
          </div>
          <ul className="space-y-1">
            {approach.pros.map((pro, i) => (
              <li key={i} className="flex items-start gap-1 text-muted-foreground">
                <span className="text-green-600 dark:text-green-400">+</span>
                {pro}
              </li>
            ))}
          </ul>
        </div>
        <div>
          <div className="font-medium text-red-600 dark:text-red-400 mb-1">
            Cons
          </div>
          <ul className="space-y-1">
            {approach.cons.map((con, i) => (
              <li key={i} className="flex items-start gap-1 text-muted-foreground">
                <span className="text-red-600 dark:text-red-400">-</span>
                {con}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </button>
  );

  // Custom input section for single_choice and multi_choice
  const renderCustomInputSection = () => (
    <div className="mt-4 pt-4 border-t border-border">
      {!showCustomInput ? (
        <button
          type="button"
          onClick={() => setShowCustomInput(true)}
          className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-lg border border-dashed border-muted-foreground/30 text-muted-foreground hover:border-primary/50 hover:text-primary transition-colors"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
          </svg>
          <span className="text-sm font-medium">Or type your own answer</span>
        </button>
      ) : (
        <div className="space-y-3 animate-in fade-in slide-in-from-top-2 duration-200">
          <div className="flex items-center justify-between">
            <label className="text-sm font-medium">Your custom answer</label>
            <button
              type="button"
              onClick={() => {
                setShowCustomInput(false);
                setCustomInput("");
              }}
              className="text-xs text-muted-foreground hover:text-foreground"
            >
              Cancel
            </button>
          </div>
          <Textarea
            placeholder="Type your own answer..."
            value={customInput}
            onChange={(e) => setCustomInput(e.target.value)}
            onKeyDown={handleCustomKeyDown}
            disabled={isAnswering}
            rows={3}
            className="resize-none"
          />
          <Button
            onClick={handleSubmitCustomInput}
            disabled={!customInput.trim() || isAnswering}
            className="w-full"
          >
            {isAnswering ? "Processing..." : "Submit Custom Answer"}
          </Button>
        </div>
      )}
    </div>
  );

  return (
    <Card className="w-full max-w-none border-amber-100/80 dark:border-amber-900/40 shadow-[0_20px_45px_-25px_rgba(245,158,11,0.25)] animate-in fade-in slide-in-from-bottom-4 duration-300">
      <CardHeader className="pb-3">
        <CardTitle className="text-lg leading-relaxed">
          {question.question}
        </CardTitle>
        {question.context && (
          <p className="text-sm text-muted-foreground mt-1">{question.context}</p>
        )}
      </CardHeader>
      <CardContent className="space-y-3">
        {/* Single Choice Options */}
        {question.type === "single_choice" && (
          <>
            <div className="space-y-2">
              {question.options.map((option) => renderOption(option))}
            </div>
            {renderCustomInputSection()}
          </>
        )}

        {/* Multi Choice Options */}
        {question.type === "multi_choice" && (
          <>
            <div className="space-y-2">
              {question.options.map((option) => renderOption(option))}
            </div>
            {!showCustomInput && (
              <Button
                onClick={handleSubmitMultiChoice}
                disabled={selectedOptions.length === 0 || isAnswering}
                className="w-full mt-4"
              >
                {isAnswering ? "Processing..." : "Continue"}
              </Button>
            )}
            {renderCustomInputSection()}
          </>
        )}

        {/* Approach Options */}
        {question.type === "approach" && (
          <>
            <div className="space-y-3">
              {question.approaches.map((approach) => renderApproach(approach))}
            </div>
            {renderCustomInputSection()}
          </>
        )}

        {/* Text Input */}
        {question.type === "text_input" && (
          <div className="space-y-3">
            <Input
              placeholder="Type your answer..."
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isAnswering}
            />
            <Button
              onClick={handleSubmitTextInput}
              disabled={!textInput.trim() || isAnswering}
              className="w-full"
            >
              {isAnswering ? "Processing..." : "Continue"}
            </Button>
          </div>
        )}

        {/* Skip Button */}
        {question.allow_skip && onSkip && (
          <Button
            variant="ghost"
            size="sm"
            onClick={onSkip}
            disabled={isAnswering}
            className="w-full mt-2 text-muted-foreground"
          >
            Skip this question
          </Button>
        )}
      </CardContent>
    </Card>
  );
}
