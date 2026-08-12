import { Link, useLocation } from "react-router-dom";
const links = [
  {
    to: "/resume-screening",
    label: "Resume Screening",
    mobileLabel: "Resume",
  },
  {
    to: "/mock-interview",
    label: "Mock Interview",
    mobileLabel: "Interview",
  },
  {
    to: "/course-recommendation",
    label: "Course Recommendation",
    mobileLabel: "Courses",
  },
];

export default function Navbar() {
  const location = useLocation();

  return (
    <header className="sticky top-0 z-30 border-b border-border bg-surface/80 backdrop-blur-md">
      <div className="mx-auto flex min-h-14 max-w-6xl items-center justify-between gap-4 px-4 py-2 sm:px-6">
        {/* Logo */}
        <Link
          to="/"
          className="flex shrink-0 items-center"
          aria-label="Evalynx Home"
        >
          <img
            src="/evalynx.png"
            alt="Evalynx"
            className="h-9 w-auto object-contain"
          />
        </Link>

        {/* Navigation */}
        <nav className="flex items-center gap-1 overflow-x-auto scrollbar-none">
          {links.map((link) => {
            const active = location.pathname === link.to;

            return (
              <Link
                key={link.to}
                to={link.to}
                className={`whitespace-nowrap rounded-lg px-2.5 py-1.5 text-xs font-medium transition-colors duration-150 sm:px-3 sm:text-sm ${
                  active
                    ? "bg-accent-soft text-accent-hover"
                    : "text-ink-soft hover:bg-canvas hover:text-ink"
                }`}
              >
                <span className="hidden sm:inline">{link.label}</span>
                <span className="sm:hidden">{link.mobileLabel}</span>
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}