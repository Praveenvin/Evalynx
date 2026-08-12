import { useEffect, useRef } from "react";
import { violationManager } from "../../services/proctoring/violationManager";
import type { SecurityMode } from "../../types/interview";

export function useVisibilityMonitor(securityMode: SecurityMode) {
  useEffect(() => {
    if (securityMode !== "proctored") return;

    const handleVisibilityChange = () => {
      if (document.hidden) {
        violationManager.registerViolation("tab_switch", "Tab Switch Detected");
      }
    };

    const handleBlur = () => {
      // Browsers often fire blur when clicking outside the window or switching apps
      violationManager.registerViolation("tab_switch", "Window Lost Focus");
    };

    document.addEventListener("visibilitychange", handleVisibilityChange);
    window.addEventListener("blur", handleBlur);

    return () => {
      document.removeEventListener("visibilitychange", handleVisibilityChange);
      window.removeEventListener("blur", handleBlur);
    };
  }, [securityMode]);
}
