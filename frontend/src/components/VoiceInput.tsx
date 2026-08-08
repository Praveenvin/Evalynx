import { useRef, useState } from "react";
import { Mic, Square } from "lucide-react";
import { transcribeVoice } from "../services/interviewApi";

interface VoiceInputProps {
  onTranscribed: (text: string) => void;
}

export default function VoiceInput({ onTranscribed }: VoiceInputProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      chunksRef.current = [];

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };

      recorder.onstop = async () => {
        stream.getTracks().forEach((track) => track.stop());
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        setIsTranscribing(true);
        try {
          const { text } = await transcribeVoice(blob);
          onTranscribed(text);
        } catch {
          // Transcription backend isn't connected yet — the user can
          // still type their answer directly.
        } finally {
          setIsTranscribing(false);
        }
      };

      recorder.start();
      mediaRecorderRef.current = recorder;
      setIsRecording(true);
    } catch {
      // Microphone permission denied or unavailable.
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setIsRecording(false);
  };

  return (
    <button
      type="button"
      onClick={isRecording ? stopRecording : startRecording}
      disabled={isTranscribing}
      aria-label={isRecording ? "Stop recording" : "Record voice answer"}
      className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border transition-colors duration-150 ${
        isRecording
          ? "border-weak bg-weak-soft text-weak"
          : "border-border text-ink-soft hover:border-border-strong hover:bg-canvas"
      } disabled:opacity-50`}
    >
      {isRecording ? <Square size={16} /> : <Mic size={17} />}
    </button>
  );
}
