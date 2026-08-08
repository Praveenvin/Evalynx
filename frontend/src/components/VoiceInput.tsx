import { useCallback, useEffect, useRef, useState } from "react";

interface VoiceRecorderState {
  isRecording: boolean;
  audioBlob: Blob | null;
  error: string | null;
}

export function useVoiceRecorder() {
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const [state, setState] = useState<VoiceRecorderState>({
    isRecording: false,
    audioBlob: null,
    error: null,
  });

  const startRecording = useCallback(async () => {
    try {
      setState({
        isRecording: false,
        audioBlob: null,
        error: null,
      });

      if (!navigator.mediaDevices?.getUserMedia) {
        throw new Error(
          "Voice recording is not supported by this browser."
        );
      }

      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });

      streamRef.current = stream;
      chunksRef.current = [];

      const mimeType = MediaRecorder.isTypeSupported(
        "audio/webm;codecs=opus"
      )
        ? "audio/webm;codecs=opus"
        : "audio/webm";

      const recorder = new MediaRecorder(stream, {
        mimeType,
      });

      mediaRecorderRef.current = recorder;

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      recorder.onstop = () => {
        const blob = new Blob(chunksRef.current, {
          type: recorder.mimeType || "audio/webm",
        });

        setState({
          isRecording: false,
          audioBlob: blob,
          error: null,
        });

        stream.getTracks().forEach((track) => track.stop());
        streamRef.current = null;
      };

      recorder.onerror = () => {
        setState((previous) => ({
          ...previous,
          isRecording: false,
          error: "Recording failed.",
        }));

        stream.getTracks().forEach((track) => track.stop());
        streamRef.current = null;
      };

      recorder.start();

      setState({
        isRecording: true,
        audioBlob: null,
        error: null,
      });
    } catch (error) {
      const message =
        error instanceof Error
          ? error.message
          : "Could not access the microphone.";

      setState({
        isRecording: false,
        audioBlob: null,
        error: message,
      });
    }
  }, []);

  const stopRecording = useCallback(() => {
    const recorder = mediaRecorderRef.current;

    if (
      recorder &&
      recorder.state !== "inactive"
    ) {
      recorder.stop();
    }
  }, []);

  const cancelRecording = useCallback(() => {
    const recorder = mediaRecorderRef.current;

    if (
      recorder &&
      recorder.state !== "inactive"
    ) {
      recorder.ondataavailable = null;
      recorder.onstop = null;
      recorder.onerror = null;
      recorder.stop();
    }

    chunksRef.current = [];

    streamRef.current?.getTracks().forEach((track) => {
      track.stop();
    });

    streamRef.current = null;
    mediaRecorderRef.current = null;

    setState({
      isRecording: false,
      audioBlob: null,
      error: null,
    });
  }, []);

  const clearRecording = useCallback(() => {
    setState({
      isRecording: false,
      audioBlob: null,
      error: null,
    });
  }, []);

  useEffect(() => {
    return () => {
      streamRef.current?.getTracks().forEach((track) => {
        track.stop();
      });
    };
  }, []);

  return {
    isRecording: state.isRecording,
    audioBlob: state.audioBlob,
    error: state.error,
    startRecording,
    stopRecording,
    cancelRecording,
    clearRecording,
  };
}