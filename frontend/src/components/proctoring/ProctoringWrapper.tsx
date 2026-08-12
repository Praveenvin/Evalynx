import React, { useState, useEffect, useCallback } from "react";
import { useProctoring } from "../../hooks/proctoring/useProctoring";
import { useVisibilityMonitor } from "../../hooks/proctoring/useVisibilityMonitor";
import { useFullscreenMonitor } from "../../hooks/proctoring/useFullscreenMonitor";
import { useCopyPasteMonitor } from "../../hooks/proctoring/useCopyPasteMonitor";
import ViolationToastManager from "./ViolationToastManager";
import ProctoringCamera from "./ProctoringCamera";
import type { SecurityMode } from "../../types/interview";
import type { Violation } from "../../services/proctoring/violationManager";
import { violationManager } from "../../services/proctoring/violationManager";
import { Loader2, CheckCircle2, XCircle } from "lucide-react";

interface ProctoringWrapperProps {
  securityMode: SecurityMode;
  onAutoSubmit: (violations: Violation[]) => void;
  onReady?: () => void;
  onCancel?: () => void;
}

export default function ProctoringWrapper({ securityMode, onAutoSubmit, onReady, onCancel }: ProctoringWrapperProps) {
  useVisibilityMonitor(securityMode);
  const { isFullscreenWarningVisible, resumeFullscreen } = useFullscreenMonitor(securityMode);
  useCopyPasteMonitor(securityMode);

  const [isCameraActive, setIsCameraActive] = useState(false);
  const [hasFiredReady, setHasFiredReady] = useState(false);

  const {
    isReady,
    hasError,
    errorMessage,
    detectionState,
    toasts,
    violationCount,
    startProctoring
  } = useProctoring(securityMode, onAutoSubmit);

  useEffect(() => {
    if (isReady && isCameraActive && !hasFiredReady && !hasError) {
      setHasFiredReady(true);
      if (onReady) onReady();
    }
  }, [isReady, isCameraActive, hasFiredReady, hasError, onReady]);

  if (securityMode !== "proctored") {
    return null;
  }

  const handleVideoReady = useCallback((video: HTMLVideoElement) => {
    setIsCameraActive(true);
    startProctoring(video);
  }, [startProctoring]);

  return (
    <>
      <ViolationToastManager toasts={toasts} violationCount={violationCount} />
      
      {isReady && !hasError && (
        <ProctoringCamera 
          onVideoReady={handleVideoReady}
          detectionState={detectionState}
          violationCount={violationCount}
        />
      )}

      {/* Blocking overlay while camera / ML models are initializing */}
      {(!isReady || !isCameraActive) && !hasError && !hasFiredReady && (
        <div className="fixed inset-0 z-[9999] flex flex-col items-center justify-center bg-surface text-center p-6">
          <div className="max-w-md w-full bg-canvas border border-border rounded-2xl p-8 shadow-xl">
            <h2 className="text-xl font-bold text-ink mb-6">Preparing Secure Interview</h2>
            
            <div className="space-y-4 text-left">
              <div className="flex items-center gap-3 text-sm">
                {isCameraActive ? <CheckCircle2 className="text-success" size={20} /> : <Loader2 className="animate-spin text-accent" size={20} />}
                <span className={isCameraActive ? "text-ink" : "text-ink-soft"}>Camera {isCameraActive ? "— Ready" : "— Waiting for permission"}</span>
              </div>
              <div className="flex items-center gap-3 text-sm">
                {isReady ? <CheckCircle2 className="text-success" size={20} /> : <Loader2 className="animate-spin text-accent" size={20} />}
                <span className={isReady ? "text-ink" : "text-ink-soft"}>Face detection {isReady ? "— Ready" : "— Loading models"}</span>
              </div>
              <div className="flex items-center gap-3 text-sm">
                {isReady ? <CheckCircle2 className="text-success" size={20} /> : <Loader2 className="animate-spin text-accent" size={20} />}
                <span className={isReady ? "text-ink" : "text-ink-soft"}>Object detection {isReady ? "— Ready" : "— Loading models"}</span>
              </div>
              <div className="flex items-center gap-3 text-sm pt-2 border-t border-border">
                {(isReady && isCameraActive) ? <CheckCircle2 className="text-success" size={20} /> : <Loader2 className="animate-spin text-accent" size={20} />}
                <span className={(isReady && isCameraActive) ? "text-ink font-semibold" : "text-ink-soft font-semibold"}>Proctoring {(isReady && isCameraActive) ? "— Ready" : "— Initializing"}</span>
              </div>
            </div>
            
            <p className="text-xs text-ink-faint mt-8">
              Please allow camera access in your browser. The interview will begin automatically once your environment is secured.
            </p>
          </div>
        </div>
      )}

      {hasError && (
        <div className="fixed inset-0 z-[9999] flex flex-col items-center justify-center bg-black/80 backdrop-blur-sm text-center p-6">
          <div className="rounded-2xl bg-surface p-8 max-w-md shadow-2xl border border-red-500">
            <div className="flex justify-center mb-4"><XCircle className="text-red-500" size={48} /></div>
            <h2 className="text-xl font-bold text-ink mb-2">Initialization Failed</h2>
            <p className="text-sm text-ink-soft mb-6">{errorMessage}</p>
            <div className="flex gap-4 justify-center">
              {onCancel && (
                <button onClick={onCancel} className="px-6 py-3 bg-canvas text-ink font-medium rounded-lg hover:bg-border transition-colors">
                  Cancel Interview
                </button>
              )}
              <button onClick={() => window.location.reload()} className="px-6 py-3 bg-accent text-white font-medium rounded-lg hover:bg-accent-hover transition-colors">
                Retry
              </button>
            </div>
          </div>
        </div>
      )}

      {hasError && (
        <div className="fixed top-20 right-4 z-[9999] rounded-lg bg-red-100 p-4 border border-red-300 shadow-xl max-w-sm">
          <p className="text-sm font-semibold text-red-800">Proctoring Error</p>
          <p className="text-xs mt-1 text-red-600">{errorMessage}</p>
        </div>
      )}

      {isFullscreenWarningVisible && (
        <div className="fixed inset-0 z-[9999] flex flex-col items-center justify-center bg-black/80 backdrop-blur-sm text-center p-6">
          <div className="rounded-2xl bg-surface p-8 max-w-md shadow-2xl border border-warn">
            <h2 className="text-xl font-bold text-ink mb-2">Fullscreen Exited</h2>
            <p className="text-sm text-ink-soft mb-6">
              You must remain in fullscreen mode during a proctored interview. Return to fullscreen immediately to avoid a violation.
            </p>
            <div className="flex gap-4 justify-center">
              <button 
                onClick={resumeFullscreen}
                className="px-6 py-3 bg-accent text-white font-medium rounded-lg hover:bg-accent-hover transition-colors"
              >
                Return to Fullscreen
              </button>
              <button 
                onClick={() => onAutoSubmit(violationManager.getViolations())}
                className="px-6 py-3 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 transition-colors"
              >
                End Exam
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
