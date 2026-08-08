import { X } from "lucide-react";
import type { CandidateResult } from "../types/resumeScreening";
import ScoreBar from "./ScoreBar";
import RecommendationBadge from "./RecommendationBadge";

interface CandidateDetailsProps {
  candidate: CandidateResult;
  onClose: () => void;
}

export default function CandidateDetails({
  candidate,
  onClose,
}: CandidateDetailsProps) {
  return (
    <div className="fixed inset-0 z-40 flex justify-end bg-ink/20 backdrop-blur-[2px]">
      <div
        className="absolute inset-0"
        onClick={onClose}
        aria-hidden="true"
      />
      <div className="relative flex h-full w-full max-w-md flex-col overflow-y-auto border-l border-border bg-surface p-6 shadow-2xl sm:p-7">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-xs font-medium text-ink-faint">Candidate</p>
            <h2 className="mt-1 font-display text-lg font-semibold text-ink">
              {candidate.filename}
            </h2>
          </div>
          <button
            onClick={onClose}
            aria-label="Close candidate details"
            className="rounded-lg p-1.5 text-ink-faint transition-colors hover:bg-canvas hover:text-ink"
          >
            <X size={18} />
          </button>
        </div>

        <div className="mt-6 rounded-xl bg-canvas p-4">
          <p className="text-xs font-medium text-ink-faint">Overall Score</p>
          <div className="mt-1 flex items-baseline gap-1.5">
            <span className="font-display text-3xl font-semibold text-ink">
              {candidate.overall_score.toFixed(1)}
            </span>
            <span className="text-sm text-ink-faint">/ 100</span>
          </div>
          <div className="mt-3">
            <RecommendationBadge recommendation={candidate.recommendation} />
          </div>
        </div>

        <div className="mt-6 flex flex-col gap-4">
          <ScoreBar label="Skills" score={candidate.skills_score} />
          <ScoreBar label="Experience" score={candidate.experience_score} />
          <ScoreBar label="Education" score={candidate.education_score} />
          <ScoreBar label="Semantic" score={candidate.semantic_score} />
        </div>

        {candidate.strengths.length > 0 && (
          <div className="mt-7">
            <h3 className="text-sm font-semibold text-ink">Strengths</h3>
            <ul className="mt-2.5 flex flex-col gap-1.5">
              {candidate.strengths.map((s, i) => (
                <li
                  key={i}
                  className="flex gap-2 text-sm leading-relaxed text-ink-soft"
                >
                  <span className="mt-2 h-1 w-1 shrink-0 rounded-full bg-good" />
                  {s}
                </li>
              ))}
            </ul>
          </div>
        )}

        {candidate.gaps.length > 0 && (
          <div className="mt-6">
            <h3 className="text-sm font-semibold text-ink">Gaps</h3>
            <ul className="mt-2.5 flex flex-col gap-1.5">
              {candidate.gaps.map((g, i) => (
                <li
                  key={i}
                  className="flex gap-2 text-sm leading-relaxed text-ink-soft"
                >
                  <span className="mt-2 h-1 w-1 shrink-0 rounded-full bg-weak" />
                  {g}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
