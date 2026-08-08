export type Recommendation =
  | "Strong Match"
  | "Good Match"
  | "Potential Match"
  | "Weak Match";

export interface CandidateResult {
  rank: number;
  candidate_id: string;
  filename: string;
  overall_score: number;
  skills_score: number;
  experience_score: number;
  education_score: number;
  semantic_score: number;
  strengths: string[];
  gaps: string[];
  recommendation: Recommendation;
}

export interface ScreeningResponse {
  total_candidates: number;
  results: CandidateResult[];
}
