import { useEffect } from "react";
import { violationManager } from "../../services/proctoring/violationManager";
import type { SecurityMode } from "../../types/interview";

export function useCopyPasteMonitor(securityMode: SecurityMode) {
  useEffect(() => {
    if (securityMode !== "proctored") return;

    const handleCopy = (e: ClipboardEvent) => {
      e.preventDefault();
      violationManager.registerViolation("copy_paste", "Copying is not allowed");
    };

    const handlePaste = (e: ClipboardEvent) => {
      e.preventDefault();
      violationManager.registerViolation("copy_paste", "Pasting is not allowed");
    };

    const handleContextMenu = (e: MouseEvent) => {
      e.preventDefault();
    };

    document.addEventListener("copy", handleCopy);
    document.addEventListener("paste", handlePaste);
    document.addEventListener("contextmenu", handleContextMenu);

    return () => {
      document.removeEventListener("copy", handleCopy);
      document.removeEventListener("paste", handlePaste);
      document.removeEventListener("contextmenu", handleContextMenu);
    };
  }, [securityMode]);
}
