import { API_BASE_URL, parseJsonOrThrow } from "./api";

import type {
  StartInterviewPayload,
  StartInterviewResponse,
  SubmitAnswerResponse,
} from "../types/interview";

export async function startInterview(
  payload: StartInterviewPayload,
  resumeFile: File | null,
): Promise<StartInterviewResponse> {
  const formData = new FormData();

  formData.append("source", payload.source);
  formData.append("role", payload.role || "");
  formData.append("skills", JSON.stringify(payload.skills ?? []));
  formData.append("mode", payload.mode);
  formData.append("duration", String(payload.duration));
  formData.append("question_count", String(payload.question_count));

  if (resumeFile) {
    formData.append("resume", resumeFile);
  }

  const response = await fetch(
    `${API_BASE_URL}/api/mock-interview/start`,
    {
      method: "POST",
      body: formData,
    },
  );

  return parseJsonOrThrow<StartInterviewResponse>(
    response,
  );
}


/**
 * Submit a typed/text answer.
 *
 * Backend:
 * POST /api/mock-interview/{session_id}/answer
 */
export async function submitAnswer(
  sessionId: string,
  answer: string,
): Promise<SubmitAnswerResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/mock-interview/${sessionId}/answer`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        answer,
      }),
    },
  );

  return parseJsonOrThrow<SubmitAnswerResponse>(
    response,
  );
}


/**
 * Submit recorded voice to Groq Whisper through the backend.
 *
 * Backend:
 * POST /api/mock-interview/{session_id}/voice-answer
 *
 * This only transcribes the answer.
 * The returned text must then be reviewed by the candidate
 * before calling submitAnswer().
 */
export async function submitVoiceAnswer(
  sessionId: string,
  audioBlob: Blob,
): Promise<{ text: string }> {
  const formData = new FormData();

  formData.append(
    "audio",
    audioBlob,
    "answer.webm",
  );

  const response = await fetch(
    `${API_BASE_URL}/api/mock-interview/${sessionId}/voice-answer`,
    {
      method: "POST",
      body: formData,
    },
  );

  return parseJsonOrThrow<{ text: string }>(
    response,
  );
}


/**
 * Replay the current interviewer question.
 *
 * Backend:
 * POST /api/mock-interview/{session_id}/replay-question
 */
export async function replayQuestion(
  sessionId: string,
): Promise<{ question: string }> {
  const response = await fetch(
    `${API_BASE_URL}/api/mock-interview/${sessionId}/replay-question`,
    {
      method: "POST",
    },
  );

  return parseJsonOrThrow<{ question: string }>(
    response,
  );
}


/**
 * Generate spoken audio for the interviewer question.
 *
 * Backend:
 * POST /api/mock-interview/{session_id}/speak
 */
export async function fetchQuestionAudio(
  sessionId: string,
  text: string,
): Promise<Blob> {
  const response = await fetch(
    `${API_BASE_URL}/api/mock-interview/${sessionId}/speak`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text,
      }),
    },
  );

  if (!response.ok) {
    const message = await response.text();

    throw new Error(
      message || "Failed to generate question audio.",
    );
  }

  return response.blob();
}


/**
 * Manually complete an interview.
 *
 * Backend:
 * POST /api/mock-interview/{session_id}/complete
 */
export async function completeInterview(
  sessionId: string,
) {
  const response = await fetch(
    `${API_BASE_URL}/api/mock-interview/${sessionId}/complete`,
    {
      method: "POST",
    },
  );

  return parseJsonOrThrow(response);
}