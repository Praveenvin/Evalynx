import { FileSearch, MessageSquareText, Globe } from "lucide-react";
import AgentCard from "../components/AgentCard";

function GithubMark() {
  return (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M12 .5C5.73.5.5 5.73.5 12c0 5.09 3.29 9.4 7.86 10.93.58.1.79-.25.79-.56 0-.28-.01-1.02-.02-2-3.2.7-3.88-1.54-3.88-1.54-.52-1.33-1.28-1.68-1.28-1.68-1.04-.72.08-.7.08-.7 1.15.08 1.76 1.19 1.76 1.19 1.03 1.75 2.69 1.25 3.34.96.1-.75.4-1.25.73-1.54-2.55-.29-5.24-1.28-5.24-5.68 0-1.25.45-2.28 1.19-3.08-.12-.29-.52-1.46.11-3.05 0 0 .96-.31 3.16 1.18a10.9 10.9 0 0 1 5.75 0c2.2-1.49 3.16-1.18 3.16-1.18.63 1.59.23 2.76.11 3.05.74.8 1.19 1.83 1.19 3.08 0 4.41-2.69 5.38-5.25 5.67.41.36.78 1.06.78 2.14 0 1.55-.01 2.79-.01 3.17 0 .31.21.67.8.56A10.52 10.52 0 0 0 23.5 12C23.5 5.73 18.27.5 12 .5Z" />
    </svg>
  );
}

function LinkedinMark() {
  return (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M20.45 20.45h-3.55v-5.57c0-1.33-.02-3.03-1.85-3.03-1.85 0-2.14 1.45-2.14 2.94v5.66H9.36V9h3.41v1.56h.05c.47-.9 1.63-1.85 3.36-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29ZM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12ZM7.12 20.45H3.56V9h3.56v11.45Z" />
    </svg>
  );
}

export default function Dashboard() {
  return (
    <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 sm:py-14">
      <div className="max-w-2xl">
        <h1 className="font-display text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
          Evalynx
        </h1>
        <p className="mt-3 text-base leading-relaxed text-ink-soft">
          AI tools for smarter hiring and interview preparation.
        </p>
        <p className="mt-1.5 text-sm text-ink-faint">
          Two focused AI agents. One simple workspace.
        </p>
      </div>

      <div className="mt-8 grid grid-cols-1 gap-5 sm:mt-10 sm:grid-cols-2">
        <AgentCard
          to="/resume-screening"
          icon={FileSearch}
          title="Resume Screening"
          description="Screen multiple resumes against a job description using semantic retrieval and AI-powered candidate evaluation."
          badges={["RAG", "FAISS", "Groq", "NLP"]}
        />
        <AgentCard
          to="/mock-interview"
          icon={MessageSquareText}
          title="Mock Interview"
          description="Practice realistic interviews with an AI interviewer using standard or dynamic questioning with voice or text answers."
          badges={["LLM", "Voice", "Dynamic Questions", "Evaluation"]}
        />
      </div>

      {/* About */}
      <div className="mt-14 max-w-2xl border-t border-border pt-8 sm:mt-16">
        <h2 className="text-xs font-semibold uppercase tracking-wide text-ink-faint">
          About Evalynx
        </h2>
        <p className="mt-3 text-sm leading-relaxed text-ink-soft">
          Evalynx combines two practical AI agents across the hiring journey.
          Resume Screening helps identify relevant candidates faster. Mock
          Interview helps candidates practice and evaluate their interview
          performance.
        </p>
      </div>

      {/* Developer footer */}
      <footer className="mt-10 flex flex-col gap-4 border-t border-border pt-6 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-sm font-medium text-ink">Built by Praveen V</p>
          <p className="mt-0.5 text-xs text-ink-faint">
            Computer Science &amp; Engineering · AI / Full-Stack Developer
          </p>
          <p className="mt-0.5 text-xs text-ink-faint">
            React · TypeScript · Python · FastAPI · AI/RAG
          </p>
        </div>
        <div className="flex items-center gap-2">
          <a
            href="https://praveen-v.vercel.app/"
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1.5 rounded-lg border border-border px-3 py-1.5 text-xs font-medium text-ink-soft transition-colors hover:border-border-strong hover:text-ink"
          >
            <Globe size={13} /> Portfolio
          </a>
          <a
            href="https://github.com/Praveenvin"
            target="_blank"
            className="inline-flex items-center gap-1.5 rounded-lg border border-border px-3 py-1.5 text-xs font-medium text-ink-soft transition-colors hover:border-border-strong hover:text-ink"
          >
            <GithubMark /> GitHub
          </a>
          <a
            href="https://www.linkedin.com/in/praveen-v-a75b5425a/"
            target="_blank"
            className="inline-flex items-center gap-1.5 rounded-lg border border-border px-3 py-1.5 text-xs font-medium text-ink-soft transition-colors hover:border-border-strong hover:text-ink"
          >
            <LinkedinMark /> LinkedIn
          </a>
        </div>
      </footer>
    </div>
  );
}
