export interface StudentProfile {
  name: string;
  education: string;
  background: string;
  career_goal: string;
  current_skills: string[];
  interests: string[];
  groq_api_key?: string;
}

export interface LearningPathStep {
  step: number;
  course: string;
  reason: string;
  difficulty: string;
  prerequisites: string[];
  duration: string;
  skills_gained: string[];
}

export interface CourseRecommendationResponse {
  student: StudentProfile;
  career_goal: string;
  current_skills: string[];
  skill_gaps: string[];
  learning_path: LearningPathStep[];
  summary: string;
}
