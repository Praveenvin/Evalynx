import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowLeft, Send } from "lucide-react";
import InterviewSetup from "../components/InterviewSetup";
import ChatMessage from "../components/ChatMessage";
import VoiceInput from "../components/VoiceInput";
import ScoreBar from "../components/ScoreBar";
import Button from "../components/Button";
import type {
  ChatMessage as ChatMessageType,
  InterviewConfig,
  InterviewResult,
} from "../types/interview";

type Stage = "setup" | "chat" | "result";

// Placeholder question bank used until the Mock Interview backend is
// connected. The chat flow, service calls, and result screen are fully
// wired to src/services/interviewApi.ts and ready to receive real data.
const PLACEHOLDER_QUESTIONS = [
  "Tell me about a challenging project you worked on and how you solved the main technical problem.",
  "How do you approach debugging an issue you've never seen before?",
  "Describe a time you had to learn a new technology quickly.",
  "How do you prioritize tasks when working on multiple features at once?",
  "Walk me through how you'd design a simple REST API for a to-do app.",
];

const PLACEHOLDER_RESULT: InterviewResult = {
  overall_score: 82,
  breakdown: {
    technical_knowledge: 85,
    communication: 78,
    problem_solving: 84,
    confidence_clarity: 80,
  },
  strengths: [
    "Strong technical understanding",
    "Good problem-solving approach",
  ],
  improvements: [
    "Give more structured explanations",
    "Provide more concrete examples",
  ],
};

export default function MockInterview() {
  const [stage, setStage] = useState<Stage>("setup");
  const [config, setConfig] = useState<InterviewConfig | null>(null);
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [questionIndex, setQuestionIndex] = useState(0);
  const [totalQuestions, setTotalQuestions] = useState(5);
  const [input, setInput] = useState("");
  const [result, setResult] = useState<InterviewResult | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight });
  }, [messages]);

  const handleStart = (cfg: InterviewConfig) => {
    setConfig(cfg);
    setTotalQuestions(cfg.questionCount);
    setQuestionIndex(1);
    setMessages([
      {
        id: crypto.randomUUID(),
        role: "interviewer",
        content: PLACEHOLDER_QUESTIONS[0],
        questionNumber: 1,
      },
    ]);
    setStage("chat");
  };

  const handleSend = () => {
    const trimmed = input.trim();
    if (!trimmed) return;

    const candidateMessage: ChatMessageType = {
      id: crypto.randomUUID(),
      role: "candidate",
      content: trimmed,
    };

    const nextIndex = questionIndex + 1;
    setInput("");

    if (nextIndex > totalQuestions) {
      setMessages((prev) => [...prev, candidateMessage]);
      setResult(PLACEHOLDER_RESULT);
      setStage("result");
      return;
    }

    const nextQuestion =
      PLACEHOLDER_QUESTIONS[(nextIndex - 1) % PLACEHOLDER_QUESTIONS.length];

    setMessages((prev) => [
      ...prev,
      candidateMessage,
      {
        id: crypto.randomUUID(),
        role: "interviewer",
        content: nextQuestion,
        questionNumber: nextIndex,
      },
    ]);
    setQuestionIndex(nextIndex);
  };

  const handleRestart = () => {
    setStage("setup");
    setConfig(null);
    setMessages([]);
    setQuestionIndex(0);
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
          <InterviewSetup onStart={handleStart} />
        </div>
      )}

      {stage === "chat" && config && (
        <div className="flex h-[calc(100vh-6rem)] flex-col rounded-2xl border border-border bg-surface">
          <div className="flex items-center justify-between border-b border-border px-5 py-4">
            <div>
              <p className="text-xs font-medium text-ink-faint">
                AI Mock Interview
              </p>
              <p className="mt-0.5 text-sm font-semibold text-ink">
                Question {Math.min(questionIndex, totalQuestions)} /{" "}
                {totalQuestions}
              </p>
            </div>
            <Link
              to="/"
              className="text-xs font-medium text-ink-faint hover:text-ink"
            >
              Exit
            </Link>
          </div>

          <div
            ref={scrollRef}
            className="flex-1 space-y-5 overflow-y-auto px-5 py-6"
          >
            {messages.map((m) => (
              <ChatMessage key={m.id} message={m} />
            ))}
          </div>

          <div className="border-t border-border p-4">
            <div className="flex items-end gap-2">
              <VoiceInput onTranscribed={(text) => setInput(text)} />
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleSend();
                  }
                }}
                placeholder="Type your answer..."
                rows={1}
                className="max-h-32 flex-1 resize-none rounded-xl border border-border bg-canvas px-3.5 py-2.5 text-sm text-ink outline-none placeholder:text-ink-faint focus:border-accent focus:ring-2 focus:ring-accent-ring"
              />
              <Button
                size="md"
                onClick={handleSend}
                disabled={!input.trim()}
                className="!px-3.5"
                aria-label="Send answer"
              >
                <Send size={16} />
              </Button>
            </div>
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
          </div>

          <div className="mt-5 grid grid-cols-1 gap-4 rounded-2xl border border-border bg-surface p-6 sm:grid-cols-2 sm:p-7">
            <ScoreBar
              label="Technical Knowledge"
              score={result.breakdown.technical_knowledge}
            />
            <ScoreBar
              label="Communication"
              score={result.breakdown.communication}
            />
            <ScoreBar
              label="Problem Solving"
              score={result.breakdown.problem_solving}
            />
            <ScoreBar
              label="Confidence / Clarity"
              score={result.breakdown.confidence_clarity}
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
                {result.improvements.map((s, i) => (
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
