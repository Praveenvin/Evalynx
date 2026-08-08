import { Bot, User } from "lucide-react";
import type { ChatMessage as ChatMessageType } from "../types/interview";

export default function ChatMessage({ message, speaking }: { message: ChatMessageType, speaking?: boolean }) {
  const isInterviewer = message.role === "interviewer";

  return (
    <div
      className={`flex items-start gap-3 ${
        isInterviewer ? "" : "flex-row-reverse"
      }`}
    >
      <div
        className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full ${
          isInterviewer
            ? "bg-accent-soft text-accent"
            : "bg-ink text-white"
        }`}
      >
        {isInterviewer ? <Bot size={16} /> : <User size={16} />}
      </div>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed sm:max-w-[70%] ${
          isInterviewer
            ? "rounded-tl-sm bg-canvas text-ink"
            : "rounded-tr-sm bg-accent text-white"
        }`}
      >
        {message.content}
        {speaking && (
          <span className="ml-2 inline-flex items-center gap-1 opacity-70">
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-current" style={{ animationDelay: "0ms" }} />
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-current" style={{ animationDelay: "150ms" }} />
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-current" style={{ animationDelay: "300ms" }} />
          </span>
        )}
      </div>
    </div>
  );
}
