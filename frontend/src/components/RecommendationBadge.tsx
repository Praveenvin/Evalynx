import type { Recommendation } from "../types/resumeScreening";

const styles: Record<Recommendation, string> = {
  "Strong Match": "bg-good-soft text-good",
  "Good Match": "bg-accent-soft text-accent-hover",
  "Potential Match": "bg-warn-soft text-warn",
  "Weak Match": "bg-weak-soft text-weak",
};

export default function RecommendationBadge({
  recommendation,
}: {
  recommendation: Recommendation;
}) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium whitespace-nowrap ${styles[recommendation]}`}
    >
      {recommendation}
    </span>
  );
}
