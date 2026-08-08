import { Bot, User } from "lucide-react";
import type { ChatMessage as ChatMessageType } from "../types/interview";

export default function ChatMessage({ message }: { message: ChatMessageType }) {
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
      </div>
    </div>
  );
}
