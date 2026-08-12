import { useEffect, useState } from "react";
import { violationManager } from "../../services/proctoring/violationManager";
import type { SecurityMode } from "../../types/interview";

export function useFullscreenMonitor(securityMode: SecurityMode) {
  const [isFullscreenWarningVisible, setIsFullscreenWarningVisible] = useState(false);
  const GRACE_PERIOD_MS = 5000;

  useEffect(() => {
    if (securityMode !== "proctored") return;

    let timeoutId: NodeJS.Timeout | null = null;

    const handleFullscreenChange = () => {
      if (!document.fullscreenElement) {
        // Exited fullscreen, trigger grace period warning
        setIsFullscreenWarningVisible(true);
        
        timeoutId = setTimeout(() => {
          // If still not in fullscreen after grace period, log violation
          if (!document.fullscreenElement) {
            violationManager.registerViolation("fullscreen_exit", "Exited Fullscreen");
            // Do not repeatedly log it if they just sit there, 
            // the state will remain warning but violation only logs once per exit.
          }
        }, GRACE_PERIOD_MS);
      } else {
        // Returned to fullscreen, clear warning
        setIsFullscreenWarningVisible(false);
        if (timeoutId) {
          clearTimeout(timeoutId);
          timeoutId = null;
        }
      }
    };

    document.addEventListener("fullscreenchange", handleFullscreenChange);
    
    // Automatically enter fullscreen when proctored session starts if not already
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch((e) => {
        console.warn("Could not auto-request fullscreen:", e);
      });
    }

    return () => {
      document.removeEventListener("fullscreenchange", handleFullscreenChange);
      if (timeoutId) clearTimeout(timeoutId);
    };
  }, [securityMode]);

  return {
    isFullscreenWarningVisible,
    resumeFullscreen: () => {
      document.documentElement.requestFullscreen().catch(console.error);
    }
  };
}
