import { AlertTriangle, X } from "lucide-react";
import { useEffect, useState } from "react";

interface Toast {
  id: string;
  message: string;
}

interface ViolationToastManagerProps {
  toasts: Toast[];
  violationCount: number;
}

export default function ViolationToastManager({ toasts, violationCount }: ViolationToastManagerProps) {
  if (toasts.length === 0) return null;

  return (
    <div className="fixed top-4 right-4 z-[9999] flex flex-col gap-2">
      {toasts.map((toast) => (
        <div 
          key={toast.id} 
          className="flex min-w-[300px] items-center gap-3 rounded-lg border border-warn/30 bg-warn/10 p-4 shadow-lg backdrop-blur-md animate-in slide-in-from-top-4 fade-in"
        >
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-warn/20 text-warn-strong">
            <AlertTriangle size={16} />
          </div>
          <div className="flex flex-col">
            <span className="text-sm font-semibold text-warn-strong">
              {toast.message}
            </span>
            <span className="text-xs font-medium text-warn-strong/80">
              Violation {violationCount} / 10
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}
