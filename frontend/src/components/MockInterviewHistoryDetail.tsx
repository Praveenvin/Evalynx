import { ArrowLeft, CheckCircle2, List, ShieldCheck, ShieldAlert } from "lucide-react";
import Button from "./Button";
import type { FinalEvaluation } from "../types/interview";

export interface MockInterviewHistoryDetailData {
  id: string;
  created_at: string;
  role: string;
  skills: string[];
  mode: string;
  duration_minutes: number;
  total_questions: number;
  is_complete: boolean;
  security_mode?: string;
  proctoring_metadata?: { type: string; timestamp: number; id: string; }[];
  final_evaluation: FinalEvaluation | null;
  turns: {
    turn_index: number;
    question: string;
    answer: string;
    evaluation: {
      score: number;
      technical_score: number;
      communication_score: number;
      problem_solving_score: number;
      relevance_score: number;
      feedback: string;
      strengths: string[];
      improvements: string[];
    };
  }[];
}

interface Props {
  detail: MockInterviewHistoryDetailData;
  onBack: () => void;
}

export default function MockInterviewHistoryDetail({ detail, onBack }: Props) {
  let fallbackOverallScore: number | null = null;
  if (!detail.final_evaluation && detail.turns.length > 0) {
    const validTurns = detail.turns.filter((t) => t.evaluation && t.evaluation.score != null);
    if (validTurns.length > 0) {
      fallbackOverallScore = Math.floor(validTurns.reduce((acc, t) => acc + t.evaluation.score, 0) / validTurns.length);
    }
  }

  const overallScoreToDisplay = detail.final_evaluation?.overall_score ?? fallbackOverallScore;
  const questionsEvaluated = detail.turns.filter((t) => t.evaluation && t.evaluation.score != null).length;

  return (
    <div className="w-full">
      <div className="flex items-center gap-4 mb-6">
        <Button variant="secondary" size="sm" onClick={onBack}>
          <ArrowLeft size={16} className="mr-1" /> Back to Interview History
        </Button>
      </div>

      <div className="rounded-2xl border border-border bg-surface p-6 mb-6">
        <h2 className="font-display text-2xl font-semibold text-ink mb-2">Mock Interview</h2>
        <h3 className="text-lg font-medium text-ink-soft mb-6 capitalize">{detail.role || "Resume-based"}</h3>
        
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-sm text-ink-soft">
          <div>
            <div className="text-ink-faint text-xs font-medium uppercase tracking-wider mb-1">Mode</div>
            <div className="capitalize">{detail.mode}</div>
          </div>
          <div>
            <div className="text-ink-faint text-xs font-medium uppercase tracking-wider mb-1">Date</div>
            <div>{new Date(detail.created_at).toLocaleDateString()}</div>
          </div>
          <div>
            <div className="text-ink-faint text-xs font-medium uppercase tracking-wider mb-1">Duration</div>
            <div>{detail.duration_minutes} min</div>
          </div>
          <div>
            <div className="text-ink-faint text-xs font-medium uppercase tracking-wider mb-1">Questions</div>
            <div>{detail.total_questions}</div>
          </div>
          {detail.security_mode === "proctored" && (
            <div>
              <div className="text-ink-faint text-xs font-medium uppercase tracking-wider mb-1">Security</div>
              <div className="flex items-center gap-1 text-accent font-medium">
                <ShieldCheck size={14} /> Proctored
              </div>
            </div>
          )}
        </div>

        {detail.skills && detail.skills.length > 0 && (
          <div className="mt-4">
            <div className="text-ink-faint text-xs font-medium uppercase tracking-wider mb-2">Skills Assessed</div>
            <div className="flex flex-wrap gap-2">
              {detail.skills.map((skill, i) => (
                <span key={i} className="inline-flex items-center rounded-md bg-canvas px-2 py-1 text-xs font-medium text-ink-soft border border-border">
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="rounded-2xl border border-border bg-surface p-6 mb-6">
        <h3 className="font-display text-xl font-semibold text-ink mb-6">OVERALL RESULT</h3>
        
        <div className="flex flex-col gap-2">
          <div className="text-xs font-medium uppercase tracking-wider text-ink-faint">Overall Score</div>
          <div className="flex items-baseline gap-2">
            <span className="text-4xl font-display font-bold text-accent">
              {overallScoreToDisplay !== null ? overallScoreToDisplay : "-"}
            </span>
            <span className="text-lg font-medium text-ink-soft">/ 100</span>
          </div>
          {overallScoreToDisplay !== null && !detail.final_evaluation && (
            <div className="text-sm text-ink-soft mt-1">Based on {questionsEvaluated} question evaluation{questionsEvaluated !== 1 ? 's' : ''}</div>
          )}
        </div>
        
        {detail.final_evaluation && (
          <div className="mt-6 border-t border-border pt-6">
            <div className="mb-6">
              <h4 className="text-sm font-semibold text-ink mb-2">Overall Feedback</h4>
              <p className="text-sm text-ink-soft leading-relaxed">{detail.final_evaluation.summary}</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {detail.final_evaluation.strengths && detail.final_evaluation.strengths.length > 0 && (
                <div className="rounded-xl border border-border bg-canvas p-4">
                  <h4 className="text-sm font-semibold text-ink mb-3 flex items-center gap-2">
                    <span className="flex h-5 w-5 items-center justify-center rounded-full bg-success/10 text-success">
                      <CheckCircle2 size={12} />
                    </span>
                    Key Strengths
                  </h4>
                  <ul className="space-y-2">
                    {detail.final_evaluation.strengths.map((item, i) => (
                      <li key={i} className="text-sm text-ink-soft flex items-start gap-2">
                        <span className="text-success mt-0.5">•</span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {detail.final_evaluation.areas_to_improve && detail.final_evaluation.areas_to_improve.length > 0 && (
                <div className="rounded-xl border border-border bg-canvas p-4">
                  <h4 className="text-sm font-semibold text-ink mb-3 flex items-center gap-2">
                    <span className="flex h-5 w-5 items-center justify-center rounded-full bg-warn/10 text-warn">
                      <List size={12} />
                    </span>
                    Areas to Improve
                  </h4>
                  <ul className="space-y-2">
                    {detail.final_evaluation.areas_to_improve.map((item, i) => (
                      <li key={i} className="text-sm text-ink-soft flex items-start gap-2">
                        <span className="text-warn mt-0.5">•</span>
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {detail.security_mode === "proctored" && detail.proctoring_metadata && (
        <div className="rounded-2xl border border-border bg-surface p-6 mb-6">
          <h3 className="font-display text-xl font-semibold text-ink mb-6 flex items-center gap-2">
            <ShieldAlert size={20} className={detail.proctoring_metadata.length > 0 ? "text-warn-strong" : "text-success"} /> 
            PROCTORING LOG
          </h3>
          {detail.proctoring_metadata.length === 0 ? (
            <div className="text-sm text-ink-soft bg-canvas border border-border rounded-xl p-4 flex items-center justify-center">
              No violations recorded during this interview.
            </div>
          ) : (
            <div className="space-y-3">
              <div className="text-sm font-medium text-warn-strong mb-2">
                Total Violations: {detail.proctoring_metadata.length}
              </div>
              <div className="overflow-hidden rounded-xl border border-border bg-canvas">
                <table className="w-full text-left text-sm text-ink-soft">
                  <thead className="border-b border-border bg-surface/50 text-xs uppercase tracking-wider text-ink-faint">
                    <tr>
                      <th className="px-4 py-3 font-medium">Time</th>
                      <th className="px-4 py-3 font-medium">Violation Type</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border">
                    {detail.proctoring_metadata.map((v, i) => (
                      <tr key={v.id || i}>
                        <td className="px-4 py-3 font-medium text-ink">
                          {new Date(v.timestamp).toLocaleTimeString()}
                        </td>
                        <td className="px-4 py-3">
                          <span className="inline-flex items-center rounded-md bg-warn/10 px-2 py-1 text-xs font-medium text-warn-strong">
                            {v.type.replace(/_/g, " ")}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

      <h3 className="font-display text-xl font-semibold text-ink mb-6">Questions & Answers</h3>
      
      <div className="space-y-6">
        {[...detail.turns].sort((a, b) => a.turn_index - b.turn_index).map((turn) => (
          <div key={turn.turn_index} className="rounded-2xl border border-border bg-surface overflow-hidden">
            <div className="bg-canvas border-b border-border px-6 py-4 flex items-center justify-between">
              <h4 className="font-semibold text-ink">Question {turn.turn_index}</h4>
              {turn.evaluation && (
                <div className="text-sm font-medium text-accent">Score: {turn.evaluation.score}/100</div>
              )}
            </div>
            
            <div className="p-6 space-y-6">
              <div>
                <div className="text-xs font-semibold uppercase tracking-wider text-ink-faint mb-2">AI Question</div>
                <div className="text-sm text-ink leading-relaxed">{turn.question}</div>
              </div>
              
              <div>
                <div className="text-xs font-semibold uppercase tracking-wider text-ink-faint mb-2">Candidate Answer</div>
                {turn.answer ? (
                  <div className="text-sm text-ink-soft leading-relaxed italic bg-canvas p-4 rounded-xl border border-border">"{turn.answer}"</div>
                ) : (
                  <div className="text-sm text-ink-faint italic">No answer provided.</div>
                )}
              </div>

              {turn.evaluation && (
                <div className="border-t border-border pt-6">
                  <div className="mb-6">
                    <div className="text-xs font-semibold uppercase tracking-wider text-ink-faint mb-3">Evaluation</div>
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                      <div>
                        <div className="text-ink-faint text-[10px] font-semibold uppercase tracking-wider mb-1">Technical</div>
                        <div className="text-sm font-medium text-ink">{turn.evaluation.technical_score}/100</div>
                      </div>
                      <div>
                        <div className="text-ink-faint text-[10px] font-semibold uppercase tracking-wider mb-1">Communication</div>
                        <div className="text-sm font-medium text-ink">{turn.evaluation.communication_score}/100</div>
                      </div>
                      <div>
                        <div className="text-ink-faint text-[10px] font-semibold uppercase tracking-wider mb-1">Problem Solving</div>
                        <div className="text-sm font-medium text-ink">{turn.evaluation.problem_solving_score}/100</div>
                      </div>
                      <div>
                        <div className="text-ink-faint text-[10px] font-semibold uppercase tracking-wider mb-1">Relevance</div>
                        <div className="text-sm font-medium text-ink">{turn.evaluation.relevance_score}/100</div>
                      </div>
                    </div>
                  </div>

                  <div className="mb-4">
                    <div className="text-xs font-semibold uppercase tracking-wider text-ink-faint mb-2">Feedback</div>
                    <div className="text-sm text-ink-soft leading-relaxed">{turn.evaluation.feedback}</div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {turn.evaluation.strengths && turn.evaluation.strengths.length > 0 && (
                      <div>
                        <div className="text-xs font-semibold text-success mb-2">Strengths</div>
                        <ul className="space-y-1">
                          {turn.evaluation.strengths.map((s, i) => (
                            <li key={i} className="text-xs text-ink-soft flex items-start gap-1.5">
                              <span className="text-success">•</span> {s}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    
                    {turn.evaluation.improvements && turn.evaluation.improvements.length > 0 && (
                      <div>
                        <div className="text-xs font-semibold text-warn mb-2">Areas to Improve</div>
                        <ul className="space-y-1">
                          {turn.evaluation.improvements.map((s, i) => (
                            <li key={i} className="text-xs text-ink-soft flex items-start gap-1.5">
                              <span className="text-warn">•</span> {s}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
