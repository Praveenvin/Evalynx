import { API_BASE_URL, parseJsonOrThrow } from "./api";
import type {
  InterviewResult,
  StartInterviewPayload,
  StartInterviewResponse,
  SubmitAnswerPayload,
  SubmitAnswerResponse,
} from "../types/interview";

// NOTE: The Mock Interview backend is not implemented yet. This service
// layer mirrors the shape the frontend expects so it can be wired up to
// the real FastAPI endpoints without further UI changes.

export async function startInterview(
  payload: StartInterviewPayload,
  resumeFile: File | null
): Promise<StartInterviewResponse> {
  const formData = new FormData();
  formData.append("source", payload.source);
  formData.append("mode", payload.mode);
  formData.append("duration_minutes", String(payload.duration_minutes));
  formData.append("question_count", String(payload.question_count));
  if (payload.role) formData.append("role", payload.role);
  if (payload.skills) formData.append("skills", JSON.stringify(payload.skills));
  if (resumeFile) formData.append("resume", resumeFile);

  const response = await fetch(`${API_BASE_URL}/api/mock-interview/start`, {
    method: "POST",
    body: formData,
  });

  return parseJsonOrThrow<StartInterviewResponse>(response);
}

export async function submitAnswer(
  payload: SubmitAnswerPayload
): Promise<SubmitAnswerResponse> {
  const response = await fetch(`${API_BASE_URL}/api/mock-interview/answer`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  return parseJsonOrThrow<SubmitAnswerResponse>(response);
}

export async function getInterviewResult(
  sessionId: string
): Promise<InterviewResult> {
  const response = await fetch(
    `${API_BASE_URL}/api/mock-interview/result/${sessionId}`
  );

  return parseJsonOrThrow<InterviewResult>(response);
}

export async function transcribeVoice(audioBlob: Blob): Promise<{ text: string }> {
  const formData = new FormData();
  formData.append("audio", audioBlob, "answer.webm");

  const response = await fetch(`${API_BASE_URL}/api/mock-interview/transcribe`, {
    method: "POST",
    body: formData,
  });

  return parseJsonOrThrow<{ text: string }>(response);
}
