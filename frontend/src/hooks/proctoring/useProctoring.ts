import { useState, useEffect, useRef, useCallback } from "react";
import { visualDetector, type DetectionState } from "../../services/proctoring/visualDetector";
import { violationManager, type Violation } from "../../services/proctoring/violationManager";
import type { SecurityMode } from "../../types/interview";

export function useProctoring(securityMode: SecurityMode, onAutoSubmit: (violations: Violation[]) => void) {
  const [isReady, setIsReady] = useState(securityMode === "standard");
  const [hasError, setHasError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  
  const [detectionState, setDetectionState] = useState<DetectionState>({
    faceCount: 0,
    faces: [],
    phoneDetected: false
  });

  const [toasts, setToasts] = useState<{ id: string, message: string }[]>([]);
  const [violationCount, setViolationCount] = useState(0);

  // Helper to trigger violations based on visual detector states, applying Grace Periods
  const [noFaceSince, setNoFaceSince] = useState<number | null>(null);
  const [multipleFaceSince, setMultipleFaceSince] = useState<number | null>(null);
  const [phoneSince, setPhoneSince] = useState<number | null>(null);

  const GRACE_MS_NO_FACE = 5000;
  const GRACE_MS_MULTIPLE = 4000;
  const GRACE_MS_PHONE = 1500;

  useEffect(() => {
    if (securityMode !== "proctored") return;

    visualDetector.initialize()
      .then(() => setIsReady(true))
      .catch(err => {
        setHasError(true);
        setErrorMessage("Failed to load proctoring models. Please ensure you have a stable connection and try again.");
      });

    return () => {
      visualDetector.stop();
      violationManager.reset();
    };
  }, [securityMode]);

  useEffect(() => {
    if (securityMode !== "proctored") return;

    violationManager.setCallbacks(
      onAutoSubmit,
      (msg, count) => {
        setViolationCount(count);
        const id = Math.random().toString(36).substr(2, 9);
        setToasts(prev => [...prev, { id, message: msg }]);
        
        setTimeout(() => {
          setToasts(prev => prev.filter(t => t.id !== id));
        }, 4000); // 4 second toast duration
      }
    );
  }, [securityMode, onAutoSubmit]);

  // Evaluate detection state and trigger violations with grace period logic
  useEffect(() => {
    if (securityMode !== "proctored" || !isReady) return;

    const now = Date.now();

    // No Face Logic
    if (detectionState.faceCount === 0) {
      if (!noFaceSince) setNoFaceSince(now);
      else if (now - noFaceSince > GRACE_MS_NO_FACE) {
        violationManager.registerViolation("no_face", "Face not detected");
      }
    } else {
      setNoFaceSince(null);
    }

    // Multiple Face Logic
    if (detectionState.faceCount > 1) {
      if (!multipleFaceSince) setMultipleFaceSince(now);
      else if (now - multipleFaceSince > GRACE_MS_MULTIPLE) {
        violationManager.registerViolation("multiple_faces", "Multiple faces detected");
      }
    } else {
      setMultipleFaceSince(null);
    }

    // Phone Detection Logic
    if (detectionState.phoneDetected) {
      if (!phoneSince) setPhoneSince(now);
      else if (now - phoneSince > GRACE_MS_PHONE) {
        violationManager.registerViolation("phone_detected", "Mobile phone detected");
      }
    } else {
      setPhoneSince(null);
    }

  }, [detectionState, securityMode, isReady, noFaceSince, multipleFaceSince, phoneSince]);

  const stopProctoring = useCallback(() => {
    visualDetector.stop();
    const video = document.getElementById("proctoring-video") as HTMLVideoElement;
    if (video && video.srcObject) {
      const stream = video.srcObject as MediaStream;
      stream.getTracks().forEach(track => track.stop());
      video.srcObject = null;
    }
  }, []);

  useEffect(() => {
    return () => {
      stopProctoring();
    };
  }, [stopProctoring]);

  const stabilizationRef = useRef({
    consecutiveFrames: 0,
    lastStableFaceCount: 0,
    lastStableFaces: [] as any[],
  });

  const startProctoring = useCallback((videoElement: HTMLVideoElement) => {
    if (securityMode === "proctored" && isReady) {
      visualDetector.start(videoElement, (rawState) => {
        const ref = stabilizationRef.current;
        const smoothedState = { ...rawState };

        if (rawState.faceCount === ref.lastStableFaceCount) {
          ref.consecutiveFrames = 0;
          ref.lastStableFaces = rawState.faces;
        } else {
          ref.consecutiveFrames++;
          if (ref.consecutiveFrames > 5) {
            ref.lastStableFaceCount = rawState.faceCount;
            ref.lastStableFaces = rawState.faces;
            ref.consecutiveFrames = 0;
          } else {
            smoothedState.faceCount = ref.lastStableFaceCount;
            if (smoothedState.faces.length === 0 && ref.lastStableFaceCount > 0) {
              smoothedState.faces = ref.lastStableFaces;
            }
          }
        }
        
        setDetectionState(smoothedState);
      });
    }
  }, [securityMode, isReady]);

  return {
    isReady,
    hasError,
    errorMessage,
    detectionState,
    toasts,
    violationCount,
    startProctoring,
    stopProctoring
  };
}
