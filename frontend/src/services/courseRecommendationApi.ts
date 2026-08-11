import { API_BASE_URL, parseJsonOrThrow } from "./api";
import type {
  CourseRecommendationResponse,
  StudentProfile,
} from "../types/courseRecommendation";

export async function recommendCourses(
  profile: StudentProfile
): Promise<CourseRecommendationResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/course-recommendation/recommend`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(profile),
    }
  );

  return parseJsonOrThrow<CourseRecommendationResponse>(response);
}
