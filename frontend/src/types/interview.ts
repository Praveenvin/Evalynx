export type InterviewSource = "resume" | "role";
export type InterviewMode = "standard" | "dynamic";
export type AnswerMethod = "voice" | "text";
export type ApiProvider = "custom" | "builtin";

export type InterviewState =
  | "idle"
  | "ai_speaking"
  | "ready_to_record"
  | "transcribing"
  | "reviewing_transcript"
  | "submitting"
  | "evaluating";

export interface FinalEvaluation {
  overall_score: number;
  technical_knowledge: number;
  communication: number;
  problem_solving: number;
  confidence_clarity: number;
  strengths: string[];
  areas_to_improve: string[];
  summary: string;
}

export interface InterviewConfig {
  source: InterviewSource;
  resumeFile: File | null;
  role: string;
  skills: string[];
  mode: InterviewMode;
  durationMinutes: number;
  questionCount: number;
  allowTyping: boolean;
  apiProvider: ApiProvider;
  groqApiKey?: string;
}

export interface ChatMessage {
  id: string;
  role: "interviewer" | "candidate";
  content: string;
  questionNumber?: number;
}

export interface InterviewScoreBreakdown {
  technical_knowledge: number;
  communication: number;
  problem_solving: number;
  confidence_clarity: number;
}

export interface InterviewResult {
  overall_score: number;
  breakdown: InterviewScoreBreakdown;
  strengths: string[];
  improvements: string[];
}

export interface StartInterviewPayload {
  source: InterviewSource;
  role: string;
  skills: string[];
  mode: InterviewMode;
  duration: number;
  question_count: number;
  api_provider: ApiProvider;
  groq_api_key?: string;
}

export interface StartInterviewResponse {
  session_id: string;
  question_number: number;
  total_questions: number;
  question: string;
  is_complete: boolean;
}

export interface SubmitAnswerPayload {
  session_id: string;
  answer: string;
}

export interface SubmitAnswerResponse {
  next_question: string | null;
  question_number: number;
  is_complete: boolean;
  final_evaluation?: FinalEvaluation;
}
