export type InterviewSource = "resume" | "role";
export type InterviewMode = "standard" | "dynamic";
export type AnswerMethod = "voice" | "text";

export interface InterviewConfig {
  source: InterviewSource;
  resumeFile: File | null;
  role: string;
  skills: string[];
  mode: InterviewMode;
  durationMinutes: number;
  questionCount: number;
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
  role?: string;
  skills?: string[];
  mode: InterviewMode;
  duration_minutes: number;
  question_count: number;
}

export interface StartInterviewResponse {
  session_id: string;
  first_question: string;
  total_questions: number;
}

export interface SubmitAnswerPayload {
  session_id: string;
  answer: string;
}

export interface SubmitAnswerResponse {
  next_question: string | null;
  question_number: number;
  is_complete: boolean;
}
