import { API_BASE_URL, parseJsonOrThrow } from "./api";
import type { ScreeningResponse } from "../types/resumeScreening";

export async function screenResumes(
  jobDescription: string,
  resumes: File[]
): Promise<ScreeningResponse> {
  const formData = new FormData();
  formData.append("job_description", jobDescription);
  resumes.forEach((file) => {
    formData.append("resumes", file);
  });

  const response = await fetch(`${API_BASE_URL}/api/resume-screening/screen`, {
    method: "POST",
    body: formData,
  });

  return parseJsonOrThrow<ScreeningResponse>(response);
}
