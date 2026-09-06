"use client";

import { useEffect, useState } from "react";

import {
  Bot,
  Send,
  X,
  Sparkles,
  Loader2,
} from "lucide-react";

import { Opportunity } from "@/types/opportunity";

interface Props {
  opportunity: Opportunity | null;
  onClose: () => void;
}

interface Message {
  role: "user" | "assistant";
  content: string;
}

export function OpportunityAIChat({
  opportunity,
  onClose,
}: Props) {
  const [input, setInput] = useState("");

  const [messages, setMessages] =
    useState<Message[]>([]);

  const [sending, setSending] =
    useState(false);

  /*
   * Reset conversation whenever a NEW opportunity
   * is selected.
   */
  useEffect(() => {
    if (!opportunity) {
      setMessages([]);
      setInput("");
      return;
    }

    setMessages([
      {
        role: "assistant",
        content:
          `Hi! I'm your Revenue AI assistant. I can explain this ${opportunity.opportunity_type} opportunity, its financial impact, why it was detected, and what action is recommended.`,
      },
    ]);

    setInput("");
  }, [
    opportunity?.opportunity_id,
  ]);

  if (!opportunity) {
    return null;
  }

  const sendMessage = async () => {
    const question = input.trim();

    if (!question || sending) {
      return;
    }

    const userMessage: Message = {
      role: "user",
      content: question,
    };

    setMessages((prev) => [
      ...prev,
      userMessage,
    ]);

    setInput("");
    setSending(true);

    try {
      const response = await fetch(
        "http://localhost:8000/api/opportunity-chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question,
            opportunity,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data?.detail ||
            "Unable to get AI response"
        );
      }

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            data.answer ||
            "I couldn't generate an answer.",
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            error instanceof Error
              ? error.message
              : "Unable to connect to Revenue AI.",
        },
      ]);
    } finally {
      setSending(false);
    }
  };

  const useQuestion = (
    question: string
  ) => {
    setInput(question);
  };

  return (
    <div className="fixed inset-y-0 right-0 z-[60] flex w-full max-w-md flex-col border-l border-slate-200 bg-white shadow-2xl">

      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-200 px-5 py-4">

        <div className="flex items-center gap-3">

          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-[#146ef5]">
            <Bot className="h-5 w-5" />
          </div>

          <div>
            <h2 className="font-semibold text-slate-950">
              Revenue AI
            </h2>

            <p className="text-xs text-slate-400">
              Opportunity assistant
            </p>
          </div>

        </div>

        <button
          type="button"
          onClick={onClose}
          className="rounded-lg p-2 text-slate-400 transition hover:bg-slate-100 hover:text-slate-900"
          aria-label="Close Revenue AI"
        >
          <X className="h-5 w-5" />
        </button>

      </div>

      {/* Current opportunity */}
      <div className="border-b border-slate-100 bg-slate-50 px-5 py-4">

        <p className="text-xs uppercase tracking-wide text-slate-400">
          Current opportunity
        </p>

        <p className="mt-1 break-words font-semibold text-slate-900">
          {opportunity.opportunity_type}
        </p>

        <div className="mt-2 flex gap-2">

          <span className="rounded-full bg-blue-50 px-2.5 py-1 text-xs font-medium text-blue-600">
            {opportunity.category}
          </span>

          <span
            className={`rounded-full px-2.5 py-1 text-xs font-medium ${
              opportunity.priority === "HIGH"
                ? "bg-red-50 text-red-600"
                : opportunity.priority ===
                    "MEDIUM"
                  ? "bg-amber-50 text-amber-600"
                  : "bg-slate-100 text-slate-600"
            }`}
          >
            {opportunity.priority}
          </span>

        </div>

      </div>

      {/* Chat */}
      <div className="flex-1 space-y-4 overflow-y-auto p-5">

        {messages.map((message, index) => (
          <div
            key={`${message.role}-${index}`}
            className={`flex ${
              message.role === "user"
                ? "justify-end"
                : "justify-start"
            }`}
          >

            <div
              className={`max-w-[88%] rounded-2xl px-4 py-3 text-sm leading-6 ${
                message.role === "user"
                  ? "bg-[#146ef5] text-white"
                  : "bg-slate-100 text-slate-700"
              }`}
            >
              {message.content}
            </div>

          </div>
        ))}

        {sending && (
          <div className="flex justify-start">
            <div className="flex items-center gap-2 rounded-2xl bg-slate-100 px-4 py-3 text-sm text-slate-500">
              <Loader2 className="h-4 w-4 animate-spin" />
              Revenue AI is analyzing...
            </div>
          </div>
        )}

        {messages.length === 1 &&
          !sending && (
            <div className="space-y-2 pt-2">

              <p className="text-xs font-medium text-slate-400">
                Suggested questions
              </p>

              {[
                "Why is this opportunity high priority?",
                "How much revenue is at risk?",
                "Why was this detected?",
                "What should we do next?",
              ].map((question) => (
                <button
                  key={question}
                  type="button"
                  onClick={() =>
                    useQuestion(question)
                  }
                  className="flex w-full items-center gap-2 rounded-xl border border-slate-200 p-3 text-left text-xs text-slate-600 transition hover:border-blue-300 hover:bg-blue-50"
                >
                  <Sparkles className="h-4 w-4 shrink-0 text-[#146ef5]" />

                  {question}
                </button>
              ))}

            </div>
          )}

      </div>

      {/* Input */}
      <div className="border-t border-slate-200 p-4">

        <div className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white p-2">

          <input
            value={input}
            onChange={(event) =>
              setInput(event.target.value)
            }
            onKeyDown={(event) => {
              if (
                event.key === "Enter" &&
                !event.shiftKey
              ) {
                event.preventDefault();
                sendMessage();
              }
            }}
            placeholder="Ask about this opportunity..."
            disabled={sending}
            className="min-w-0 flex-1 bg-transparent px-2 text-sm outline-none placeholder:text-slate-400 disabled:opacity-50"
          />

          <button
            type="button"
            onClick={sendMessage}
            disabled={
              !input.trim() || sending
            }
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-[#146ef5] text-white transition hover:bg-blue-600 disabled:cursor-not-allowed disabled:opacity-40"
          >
            {sending ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </button>

        </div>

      </div>

    </div>
  );
}