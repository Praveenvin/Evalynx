import { ChevronRight } from "lucide-react";
import type { CandidateResult } from "../types/resumeScreening";
import RecommendationBadge from "./RecommendationBadge";

interface CandidateTableProps {
  candidates: CandidateResult[];
  onSelect: (candidate: CandidateResult) => void;
}

export default function CandidateTable({
  candidates,
  onSelect,
}: CandidateTableProps) {
  return (
    <div className="overflow-hidden rounded-2xl border border-border bg-surface">
      {/* Desktop / tablet table */}
      <table className="hidden w-full text-left text-sm sm:table">
        <thead>
          <tr className="border-b border-border text-xs font-medium text-ink-faint">
            <th className="px-5 py-3 font-medium">Rank</th>
            <th className="px-5 py-3 font-medium">Candidate</th>
            <th className="px-5 py-3 font-medium">Overall</th>
            <th className="px-5 py-3 font-medium">Skills</th>
            <th className="px-5 py-3 font-medium">Experience</th>
            <th className="px-5 py-3 font-medium">Education</th>
            <th className="px-5 py-3 font-medium">Recommendation</th>
            <th className="px-5 py-3" />
          </tr>
        </thead>
        <tbody>
          {candidates.map((c) => (
            <tr
              key={c.candidate_id}
              onClick={() => onSelect(c)}
              className="cursor-pointer border-b border-border last:border-0 transition-colors hover:bg-canvas"
            >
              <td className="px-5 py-4 font-display font-semibold text-ink-faint">
                #{c.rank}
              </td>
              <td className="px-5 py-4 font-medium text-ink">{c.filename}</td>
              <td className="px-5 py-4 font-semibold text-ink">
                {c.overall_score.toFixed(1)}
              </td>
              <td className="px-5 py-4 text-ink-soft">{c.skills_score}</td>
              <td className="px-5 py-4 text-ink-soft">{c.experience_score}</td>
              <td className="px-5 py-4 text-ink-soft">{c.education_score}</td>
              <td className="px-5 py-4">
                <RecommendationBadge recommendation={c.recommendation} />
              </td>
              <td className="px-5 py-4 text-ink-faint">
                <ChevronRight size={16} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Mobile stacked cards */}
      <div className="flex flex-col divide-y divide-border sm:hidden">
        {candidates.map((c) => (
          <button
            key={c.candidate_id}
            onClick={() => onSelect(c)}
            className="flex flex-col gap-2 px-4 py-4 text-left transition-colors active:bg-canvas"
          >
            <div className="flex items-center justify-between">
              <span className="font-display text-sm font-semibold text-ink-faint">
                #{c.rank}
              </span>
              <RecommendationBadge recommendation={c.recommendation} />
            </div>
            <div className="flex items-center justify-between">
              <span className="truncate font-medium text-ink">
                {c.filename}
              </span>
              <span className="shrink-0 font-semibold text-ink">
                {c.overall_score.toFixed(1)}
              </span>
            </div>
            <div className="flex gap-4 text-xs text-ink-faint">
              <span>Skills {c.skills_score}</span>
              <span>Exp {c.experience_score}</span>
              <span>Edu {c.education_score}</span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
