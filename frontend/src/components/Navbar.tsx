import { Link, useLocation } from "react-router-dom";

const links = [
  { to: "/resume-screening", label: "Resume Screening" },
  { to: "/mock-interview", label: "Mock Interview" },
];

export default function Navbar() {
  const location = useLocation();

  return (
    <header className="sticky top-0 z-30 border-b border-border bg-surface/80 backdrop-blur-md">
      <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4 sm:px-6">
        <Link
          to="/"
          className="font-display text-lg font-semibold tracking-tight text-ink"
        >
          Evalynx
        </Link>

        <nav className="flex items-center gap-1">
          {links.map((link) => {
            const active = location.pathname === link.to;
            return (
              <Link
                key={link.to}
                to={link.to}
                className={`rounded-lg px-3 py-1.5 text-sm font-medium transition-colors duration-150 ${
                  active
                    ? "bg-accent-soft text-accent-hover"
                    : "text-ink-soft hover:bg-canvas hover:text-ink"
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
