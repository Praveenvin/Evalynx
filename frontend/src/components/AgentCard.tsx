import { Link } from "react-router-dom";
import { ArrowRight, type LucideIcon } from "lucide-react";
import Badge from "./Badge";

interface AgentCardProps {
  to: string;
  icon: LucideIcon;
  title: string;
  description: string;
  badges: string[];
}

export default function AgentCard({
  to,
  icon: Icon,
  title,
  description,
  badges,
}: AgentCardProps) {
  return (
    <Link
      to={to}
      className="group relative flex flex-col rounded-2xl border border-border bg-surface p-6 transition-all duration-200 hover:-translate-y-0.5 hover:border-border-strong hover:shadow-[0_8px_24px_-12px_rgba(23,20,31,0.15)] sm:p-7"
    >
      <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-accent-soft text-accent transition-colors duration-200 group-hover:bg-accent group-hover:text-white">
        <Icon size={22} strokeWidth={2} />
      </div>

      <h3 className="mt-5 font-display text-xl font-semibold text-ink">
        {title}
      </h3>
      <p className="mt-2 text-sm leading-relaxed text-ink-soft">
        {description}
      </p>

      <div className="mt-5 flex flex-wrap gap-2">
        {badges.map((badge) => (
          <Badge key={badge}>{badge}</Badge>
        ))}
      </div>

      <div className="mt-6 flex items-center gap-1.5 text-sm font-medium text-accent">
        Open Agent
        <ArrowRight
          size={16}
          className="transition-transform duration-200 group-hover:translate-x-1"
        />
      </div>
    </Link>
  );
}
