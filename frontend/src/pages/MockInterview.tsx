import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowLeft, RotateCw, Volume2, VolumeX } from "lucide-react";
import InterviewSetup from "../components/InterviewSetup";
import ChatMessage from "../components/ChatMessage";
import AnswerPanel from "../components/AnswerPanel";
import ScoreBar from "../components/ScoreBar";
import Button from "../components/Button";
import {
  replayQuestion,
  startInterview,
  submitAnswer,
  submitVoiceAnswer,
} from "../services/interviewApi";
import { useSpeechSynthesis } from "../hooks/useSpeechSynthesis";
import { ApiError } from "../services/api";
import type {
  FinalEvaluation,
  InterviewConfig,
  InterviewState,
  ChatMessage as ChatMessageType,
} from "../types/interview";

type Stage = "setup" | "chat" | "result";

export default function MockInterview() {
  const [stage, setStage] = useState<Stage>("setup");
  const [setupError, setSetupError] = useState<string | null>(null);
  const [isStarting, setIsStarting] = useState(false);

  const [sessionId, setSessionId] = useState<string | null>(null);
  const [totalQuestions, setTotalQuestions] = useState(0);
  const [questionNumber, setQuestionNumber] = useState(0);
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState("");

  const [interviewState, setInterviewState] = useState<InterviewState>("idle");
  const [transcript, setTranscript] = useState("");
  const [chatError, setChatError] = useState<string | null>(null);
  const [isMuted, setIsMuted] = useState(false);
  const [allowTyping, setAllowTyping] = useState(true);

  const [result, setResult] = useState<FinalEvaluation | null>(null);

  const scrollRef = useRef<HTMLDivElement>(null);
  const { speak, cancel, isSpeaking } = useSpeechSynthesis();

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight });
  }, [messages]);

  useEffect(() => {
    return () => {
      cancel();
    };
  }, [cancel]);

  const playQuestionAudio = (text: string) => {
    if (isMuted) {
      return;
    }
    speak(text);
  };

  const handleStart = async (config: InterviewConfig) => {
    setIsStarting(true);
    setSetupError(null);
    try {
      const response = await startInterview(
        {
          source: config.source,
          role: config.role,
          skills: config.skills,
          mode: config.mode,
          duration: config.durationMinutes,
          question_count: config.questionCount,
        },
        config.resumeFile
      );

      setSessionId(response.session_id);
      setTotalQuestions(response.total_questions);
      setQuestionNumber(response.question_number);
      setCurrentQuestion(response.question);
      setAllowTyping(config.allowTyping);
      setMessages([
        { id: crypto.randomUUID(), role: "interviewer", content: response.question },
      ]);
      setStage("chat");
      playQuestionAudio(response.question);
    } catch (err) {
      setSetupError(
        err instanceof ApiError
          ? err.message
          : "Couldn't start the interview. Confirm the backend is running."
      );
    } finally {
      setIsStarting(false);
    }
  };

  const handleRecordingComplete = async (blob: Blob) => {
    if (!sessionId) return;
    setChatError(null);
    setInterviewState("transcribing");
    try {
      const { text } = await submitVoiceAnswer(sessionId, blob);
      setTranscript(text);
      setInterviewState("reviewing_transcript");
    } catch (err) {
      setChatError(
        err instanceof ApiError
          ? err.message
          : "Transcription failed. You can record again or type your answer."
      );
      setInterviewState("ready_to_record");
    }
  };

  const handleRecordAgain = () => {
    setTranscript("");
    setChatError(null);
    setInterviewState("ready_to_record");
  };

  const handleSubmitAnswer = async () => {
    if (!sessionId || !transcript.trim()) return;
    const answerText = transcript.trim();
    setChatError(null);
    setInterviewState("submitting");

    setMessages((prev) => [
      ...prev,
      { id: crypto.randomUUID(), role: "candidate", content: answerText },
    ]);

    try {
      setInterviewState("evaluating");
      const response = await submitAnswer(sessionId, answerText);
      setTranscript("");

      if (response.is_complete && response.final_evaluation) {
        setResult(response.final_evaluation);
        setStage("result");
        return;
      }

      const nextQuestion = response.next_question ?? "";
      setQuestionNumber(response.question_number);
      setCurrentQuestion(nextQuestion);
      setMessages((prev) => [
        ...prev,
        { id: crypto.randomUUID(), role: "interviewer", content: nextQuestion },
      ]);
      playQuestionAudio(nextQuestion);
    } catch (err) {
      setChatError(
        err instanceof ApiError
          ? err.message
          : "Couldn't submit your answer. Please try again."
      );
      setTranscript(answerText);
      setInterviewState("reviewing_transcript");
    }
  };

  const handleReplay = async () => {
    if (!sessionId) return;
    try {
      const { question } = await replayQuestion(sessionId);
      playQuestionAudio(question);
    } catch {
      setChatError("Couldn't replay the question right now.");
    }
  };

  const handleRestart = () => {
    cancel();
    setStage("setup");
    setSetupError(null);
    setSessionId(null);
    setMessages([]);
    setQuestionNumber(0);
    setTotalQuestions(0);
    setCurrentQuestion("");
    setTranscript("");
    setChatError(null);
    setInterviewState("idle");
    setResult(null);
  };

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 sm:py-10">
      {stage !== "chat" && (
        <>
          <Link
            to="/"
            className="inline-flex items-center gap-1.5 text-sm font-medium text-ink-soft transition-colors hover:text-ink"
          >
            <ArrowLeft size={15} />
            Back to Dashboard
          </Link>

          <h1 className="mt-4 font-display text-2xl font-semibold tracking-tight text-ink sm:text-3xl">
            Mock Interview
          </h1>
          <p className="mt-2 max-w-2xl text-sm leading-relaxed text-ink-soft">
            Practice with an AI interviewer and get feedback on your
            performance.
          </p>
        </>
      )}

      {stage === "setup" && (
        <div className="mt-8">
          {setupError && (
            <p className="mb-4 rounded-lg bg-weak-soft px-4 py-3 text-sm text-weak">
              {setupError}
            </p>
          )}
          <InterviewSetup onStart={handleStart} />
          {isStarting && (
            <p className="mt-3 text-sm text-ink-faint">Starting interview...</p>
          )}
        </div>
      )}

      {stage === "chat" && sessionId && (
        <div className="flex h-[calc(100vh-6rem)] flex-col rounded-2xl border border-border bg-surface">
          <div className="flex items-center justify-between border-b border-border px-5 py-4">
            <div>
              <p className="text-xs font-medium text-ink-faint">
                AI Mock Interview
              </p>
              <p className="mt-0.5 text-sm font-semibold text-ink">
                Question {Math.min(questionNumber, totalQuestions)} /{" "}
                {totalQuestions}
              </p>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={() => setIsMuted((m) => !m)}
                aria-label={isMuted ? "Unmute interviewer" : "Mute interviewer"}
                className="text-ink-faint transition-colors hover:text-ink"
              >
                {isMuted ? <VolumeX size={16} /> : <Volume2 size={16} />}
              </button>
              <button
                onClick={handleReplay}
                disabled={isSpeaking || !currentQuestion}
                aria-label="Replay question"
                className="text-ink-faint transition-colors hover:text-ink disabled:opacity-40"
              >
                <RotateCw size={15} />
              </button>
              <Link
                to="/"
                className="text-xs font-medium text-ink-faint hover:text-ink"
              >
                Exit
              </Link>
            </div>
          </div>

          <div
            ref={scrollRef}
            className="flex-1 space-y-5 overflow-y-auto px-5 py-6"
          >
            {messages.map((m, i) => (
              <ChatMessage
                key={m.id}
                message={m}
                speaking={isSpeaking && i === messages.length - 1}
              />
            ))}
          </div>

          <div className="border-t border-border p-4">
            {chatError && (
              <p className="mb-3 rounded-lg bg-weak-soft px-3 py-2 text-xs text-weak">
                {chatError}
              </p>
            )}
            <AnswerPanel
              state={interviewState}
              onRecordingComplete={handleRecordingComplete}
              transcript={transcript}
              onTranscriptChange={setTranscript}
              onSubmit={handleSubmitAnswer}
              onRecordAgain={handleRecordAgain}
              onStartRecording={cancel}
              allowTyping={allowTyping}
              disabled={false}
            />
          </div>
        </div>
      )}

      {stage === "result" && result && (
        <div className="mt-8">
          <div className="rounded-2xl border border-border bg-surface p-6 text-center sm:p-8">
            <p className="text-sm font-medium text-ink-faint">
              Interview Complete
            </p>
            <div className="mt-2 flex items-baseline justify-center gap-1.5">
              <span className="font-display text-5xl font-semibold text-ink">
                {result.overall_score}
              </span>
              <span className="text-lg text-ink-faint">/ 100</span>
            </div>
            {result.summary && (
              <p className="mx-auto mt-3 max-w-lg text-sm leading-relaxed text-ink-soft">
                {result.summary}
              </p>
            )}
          </div>

          <div className="mt-5 grid grid-cols-1 gap-4 rounded-2xl border border-border bg-surface p-6 sm:grid-cols-2 sm:p-7">
            <ScoreBar
              label="Technical Knowledge"
              score={result.technical_knowledge}
            />
            <ScoreBar label="Communication" score={result.communication} />
            <ScoreBar label="Problem Solving" score={result.problem_solving} />
            <ScoreBar
              label="Confidence / Clarity"
              score={result.confidence_clarity}
            />
          </div>

          <div className="mt-5 grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div className="rounded-2xl border border-border bg-surface p-5">
              <h3 className="text-sm font-semibold text-ink">Strengths</h3>
              <ul className="mt-2.5 flex flex-col gap-1.5">
                {result.strengths.map((s, i) => (
                  <li
                    key={i}
                    className="flex gap-2 text-sm leading-relaxed text-ink-soft"
                  >
                    <span className="mt-2 h-1 w-1 shrink-0 rounded-full bg-good" />
                    {s}
                  </li>
                ))}
              </ul>
            </div>
            <div className="rounded-2xl border border-border bg-surface p-5">
              <h3 className="text-sm font-semibold text-ink">
                Areas to Improve
              </h3>
              <ul className="mt-2.5 flex flex-col gap-1.5">
                {result.areas_to_improve.map((s, i) => (
                  <li
                    key={i}
                    className="flex gap-2 text-sm leading-relaxed text-ink-soft"
                  >
                    <span className="mt-2 h-1 w-1 shrink-0 rounded-full bg-warn" />
                    {s}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="mt-6 flex flex-col gap-3 sm:flex-row">
            <Button onClick={handleRestart}>Start Another Interview</Button>
            <Link to="/" className="sm:contents">
              <Button variant="secondary" className="w-full sm:w-auto">
                Back to Dashboard
              </Button>
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}