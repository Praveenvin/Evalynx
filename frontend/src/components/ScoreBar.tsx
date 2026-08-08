interface ScoreBarProps {
  label: string;
  score: number;
  max?: number;
}

export default function ScoreBar({ label, score, max = 100 }: ScoreBarProps) {
  const pct = Math.max(0, Math.min(100, (score / max) * 100));

  return (
    <div>
      <div className="mb-1.5 flex items-center justify-between text-sm">
        <span className="text-ink-soft">{label}</span>
        <span className="font-medium text-ink">{score}</span>
      </div>
      <div className="h-1.5 w-full overflow-hidden rounded-full bg-canvas">
        <div
          className="h-full rounded-full bg-accent transition-all duration-500"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
