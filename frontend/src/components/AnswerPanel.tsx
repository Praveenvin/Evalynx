import { useState, useEffect } from "react";
import { Keyboard, Loader2, Mic, RotateCcw, Send, Square } from "lucide-react";
import { useVoiceRecorder } from "./VoiceInput";
import Button from "./Button";
import type { AnswerMethod, InterviewState } from "../types/interview";

interface AnswerPanelProps {
  state: InterviewState;
  onRecordingComplete: (blob: Blob) => void;
  transcript: string;
  onTranscriptChange: (value: string) => void;
  onSubmit: () => void;
  onRecordAgain: () => void;
  onStartRecording?: () => void;
  allowTyping: boolean;
  disabled: boolean;
}

export default function AnswerPanel({
  state,
  onRecordingComplete,
  transcript,
  onTranscriptChange,
  onSubmit,
  onRecordAgain,
  onStartRecording,
  allowTyping,
  disabled,
}: AnswerPanelProps) {
  const [method, setMethod] = useState<AnswerMethod>("voice");
  const { isRecording, error, audioBlob, startRecording, stopRecording, clearRecording } = useVoiceRecorder();

  useEffect(() => {
    if (audioBlob) {
      onRecordingComplete(audioBlob);
      clearRecording();
    }
  }, [audioBlob, onRecordingComplete, clearRecording]);

  const handleStart = () => {
    onStartRecording?.();
    startRecording();
  };

  const isReviewing = state === "reviewing_transcript";
  const isTranscribing = state === "transcribing";
  const isSubmitting = state === "submitting" || state === "evaluating";
  const canInteract = !disabled && !isSubmitting;

  if (isReviewing || (method === "text" && !isRecording && !isTranscribing)) {
    return (
      <div className="flex flex-col gap-3">
        <div className="flex items-center justify-between">
          <p className="text-xs font-semibold uppercase tracking-wide text-ink-faint">
            {isReviewing ? "Your answer" : "Your answer"}
          </p>
          {!isReviewing && (
            <button
              onClick={() => setMethod("voice")}
              disabled={!canInteract}
              className="inline-flex items-center gap-1 text-xs font-medium text-accent hover:text-accent-hover disabled:opacity-50"
            >
              <Mic size={12} /> Use voice instead
            </button>
          )}
        </div>

        <textarea
          value={transcript}
          onChange={(e) => onTranscriptChange(e.target.value)}
          placeholder="Type your answer..."
          rows={4}
          disabled={!canInteract}
          className="w-full resize-none rounded-xl border border-border bg-canvas p-3.5 text-sm leading-relaxed text-ink outline-none placeholder:text-ink-faint focus:border-accent focus:ring-2 focus:ring-accent-ring disabled:opacity-60"
        />

        <div className="flex gap-2">
          {isReviewing && (
            <Button
              variant="secondary"
              onClick={onRecordAgain}
              disabled={!canInteract}
            >
              <RotateCcw size={15} />
              Record Again
            </Button>
          )}
          <Button
            onClick={onSubmit}
            disabled={!canInteract || !transcript.trim()}
            className="flex-1 sm:flex-none"
          >
            {isSubmitting ? (
              <>
                <Loader2 size={15} className="animate-spin" />
                {state === "evaluating" ? "Evaluating..." : "Submitting..."}
              </>
            ) : (
              <>
                <Send size={15} />
                Submit Answer
              </>
            )}
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center gap-3 py-2">
      {isTranscribing ? (
        <div className="flex flex-col items-center gap-2 text-ink-soft">
          <Loader2 size={26} className="animate-spin text-accent" />
          <span className="text-sm font-medium">Transcribing...</span>
        </div>
      ) : (
        <>
          <button
            onClick={isRecording ? stopRecording : handleStart}
            disabled={!canInteract}
            aria-label={isRecording ? "Stop recording" : "Start speaking"}
            className={`flex h-16 w-16 items-center justify-center rounded-full border-2 transition-all duration-200 disabled:opacity-50 ${
              isRecording
                ? "border-weak bg-weak-soft text-weak animate-pulse"
                : "border-accent bg-accent-soft text-accent hover:bg-accent hover:text-white"
            }`}
          >
            {isRecording ? <Square size={22} /> : <Mic size={26} />}
          </button>
          <span className="text-sm font-medium text-ink-soft">
            {isRecording ? "Recording... tap to stop" : "Start Speaking"}
          </span>
        </>
      )}

      {error && <p className="text-xs text-weak">{error}</p>}

      {!isRecording && !isTranscribing && allowTyping && (
        <button
          onClick={() => setMethod("text")}
          disabled={!canInteract}
          className="mt-1 inline-flex items-center gap-1 text-xs font-medium text-ink-faint hover:text-ink disabled:opacity-50"
        >
          <Keyboard size={12} /> Type instead
        </button>
      )}
    </div>
  );
}