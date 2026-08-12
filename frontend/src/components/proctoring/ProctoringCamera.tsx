import { useEffect, useRef } from "react";
import { useDraggable } from "../../hooks/proctoring/useDraggable";
import type { DetectionState } from "../../services/proctoring/visualDetector";
import { GripHorizontal, ShieldAlert, ShieldCheck } from "lucide-react";

interface ProctoringCameraProps {
  onVideoReady: (video: HTMLVideoElement) => void;
  detectionState: DetectionState;
  violationCount: number;
}

export default function ProctoringCamera({ onVideoReady, detectionState, violationCount }: ProctoringCameraProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const { position, onMouseDown, onTouchStart } = useDraggable();

  useEffect(() => {
    let currentStream: MediaStream | null = null;
    let isMounted = true;

    async function setupCamera() {
      if (!videoRef.current) return;
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
          video: { facingMode: "user", width: 320, height: 240 },
          audio: false
        });
        
        if (!isMounted) {
          stream.getTracks().forEach(t => t.stop());
          return;
        }

        currentStream = stream;
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          // Important: Wait for video to be ready before firing callback
          videoRef.current.onloadedmetadata = () => {
            if (isMounted && videoRef.current) {
              videoRef.current.play().catch(e => console.error("Play error:", e));
              onVideoReady(videoRef.current);
            }
          };
        }
      } catch (err) {
        console.error("Camera access denied or unavailable", err);
      }
    }

    setupCamera();

    return () => {
      isMounted = false;
      if (currentStream) {
        currentStream.getTracks().forEach(t => t.stop());
      } else if (videoRef.current?.srcObject) {
        const stream = videoRef.current.srcObject as MediaStream;
        stream.getTracks().forEach(t => t.stop());
      }
    };
  }, [onVideoReady]);

  // Determine current status message
  let statusMsg = "Monitoring Active";
  let isAlert = false;
  
  if (detectionState.phoneDetected) {
    statusMsg = "Phone Detected!";
    isAlert = true;
  } else if (detectionState.faceCount === 0) {
    statusMsg = "Face not detected";
    isAlert = true;
  } else if (detectionState.faceCount > 1) {
    statusMsg = "Multiple faces";
    isAlert = true;
  }

  return (
    <div 
      ref={containerRef}
      className="fixed z-50 overflow-hidden rounded-xl bg-black shadow-2xl border-2 transition-colors duration-300"
      style={{
        width: 240,
        height: 180,
        right: 24,
        bottom: 24,
        transform: `translate(${position.x}px, ${position.y}px)`,
        borderColor: isAlert ? "rgb(239 68 68)" : "rgb(34 197 94)", // warn-strong vs success
      }}
    >
      {/* Drag Handle & Status Bar */}
      <div 
        className="absolute top-0 left-0 right-0 z-10 flex items-center justify-between bg-black/60 px-2 py-1 backdrop-blur-sm cursor-grab active:cursor-grabbing"
        onMouseDown={onMouseDown}
        onTouchStart={onTouchStart}
      >
        <div className="flex items-center gap-1.5 text-white">
          {isAlert ? <ShieldAlert size={12} className="text-red-400" /> : <ShieldCheck size={12} className="text-green-400" />}
          <span className="text-[10px] font-medium tracking-wide">
            {statusMsg}
          </span>
        </div>
        <GripHorizontal size={14} className="text-white/50" />
      </div>

      {/* Video Feed */}
      <video
        ref={videoRef}
        autoPlay
        playsInline
        muted
        className="h-full w-full object-cover scale-x-[-1]" // Mirror effect
      />

      {/* Bounding Boxes */}
      <div className="absolute inset-0 pointer-events-none scale-x-[-1]">
        {detectionState.faces.map((face, i) => {
          // Note: Coordinates from BlazeFace might need scaling depending on native video resolution vs CSS resolution.
          // For simplicity here, assuming they roughly align or we'd need aspect ratio math.
          // BlazeFace returns coords relative to video element dimensions.
          const scaleX = 240 / (videoRef.current?.videoWidth || 320);
          const scaleY = 180 / (videoRef.current?.videoHeight || 240);
          
          return (
            <div
              key={i}
              className="absolute border-2 border-green-500 rounded-sm"
              style={{
                left: face.x * scaleX,
                top: face.y * scaleY,
                width: face.width * scaleX,
                height: face.height * scaleY,
              }}
            />
          );
        })}
      </div>

      {/* Violation Counter */}
      <div className="absolute bottom-2 left-2 z-10 rounded bg-black/70 px-2 py-1 backdrop-blur-sm">
        <span className="text-[10px] font-bold text-white">
          Violations: {violationCount} / 10
        </span>
      </div>
    </div>
  );
}
