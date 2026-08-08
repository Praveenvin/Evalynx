import type { ReactNode } from "react";

export default function Badge({ children }: { children: ReactNode }) {
  return (
    <span className="inline-flex items-center rounded-full border border-border bg-canvas px-2.5 py-1 text-xs font-medium text-ink-soft">
      {children}
    </span>
  );
}
