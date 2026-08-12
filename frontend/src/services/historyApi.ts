import { API_BASE_URL, parseJsonOrThrow } from "./api";

// History Types
export interface PaginatedResponse<T> {
  items: T[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}

export interface ResumeScreeningHistoryItem {
  id: string;
  created_at: string;
  job_description: string;
  candidate_count: number;
  top_score: number | null;
  status: string;
}

export interface MockInterviewHistoryItem {
  id: string;
  created_at: string;
  role: string;
  mode: string;
  total_questions: number;
  overall_score: number | null;
  is_complete: boolean;
}

export interface CourseRecommendationHistoryItem {
  id: string;
  created_at: string;
  student_name: string;
  career_goal: string;
  course_count: number;
}

// History APIs
export async function getResumeScreeningHistory(page = 1, pageSize = 10) {
  const response = await fetch(`${API_BASE_URL}/api/resume-screening/history?page=${page}&page_size=${pageSize}`);
  return parseJsonOrThrow<PaginatedResponse<ResumeScreeningHistoryItem>>(response);
}

export async function getResumeScreeningHistoryDetail(id: string) {
  const response = await fetch(`${API_BASE_URL}/api/resume-screening/history/${id}`);
  return parseJsonOrThrow<any>(response);
}

export async function getMockInterviewHistory(page = 1, pageSize = 10) {
  const response = await fetch(`${API_BASE_URL}/api/mock-interview/history?page=${page}&page_size=${pageSize}`);
  return parseJsonOrThrow<PaginatedResponse<MockInterviewHistoryItem>>(response);
}

export async function getMockInterviewHistoryDetail(id: string) {
  const response = await fetch(`${API_BASE_URL}/api/mock-interview/history/${id}`);
  return parseJsonOrThrow<any>(response);
}

export async function getCourseRecommendationHistory(page = 1, pageSize = 10) {
  const response = await fetch(`${API_BASE_URL}/api/course-recommendation/history?page=${page}&page_size=${pageSize}`);
  return parseJsonOrThrow<PaginatedResponse<CourseRecommendationHistoryItem>>(response);
}

export async function getCourseRecommendationHistoryDetail(id: string) {
  const response = await fetch(`${API_BASE_URL}/api/course-recommendation/history/${id}`);
  return parseJsonOrThrow<any>(response);
}
