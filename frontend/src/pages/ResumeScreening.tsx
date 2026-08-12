import { useState } from "react";
import { Link } from "react-router-dom";
import { ArrowLeft, Loader2, History } from "lucide-react";
import FileUpload from "../components/FileUpload";
import FileList from "../components/FileList";
import Button from "../components/Button";
import CandidateTable from "../components/CandidateTable";
import CandidateDetails from "../components/CandidateDetails";
import ResumeScreeningHistory from "../components/ResumeScreeningHistory";
import { screenResumes } from "../services/resumeScreeningApi";
import type { CandidateResult, ScreeningResponse } from "../types/resumeScreening";
import type { ApiProvider } from "../types/interview";
import { ApiError } from "../services/api";
import ErrorPopup, { type ApiErrorDetail } from "../components/ErrorPopup";

export default function ResumeScreening() {
  const [jobDescription, setJobDescription] = useState("");
  const [resumes, setResumes] = useState<File[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | ApiErrorDetail | null>(null);
  const [results, setResults] = useState<ScreeningResponse | null>(null);
  const [selectedCandidate, setSelectedCandidate] = useState<CandidateResult | null>(null);
  const [apiProvider, setApiProvider] = useState<ApiProvider>("user");
  const [groqApiKey, setGroqApiKey] = useState("");
  const [showHistory, setShowHistory] = useState(false);
  const [fromHistory, setFromHistory] = useState(false);

  const hasNonAsciiKey = apiProvider === "user" && /[^\x00-\x7F]/.test(groqApiKey);
  const canScreen = jobDescription.trim().length > 0 && resumes.length > 0 && !hasNonAsciiKey;

  const handleAddFiles = (files: File[]) => {
    const existingNames = new Set(resumes.map((f) => f.name));
    const merged = [...resumes, ...files.filter((f) => !existingNames.has(f.name))];
    setResumes(merged);
  };

  const handleRemoveFile = (index: number) => {
    setResumes(resumes.filter((_, i) => i !== index));
  };

  const handleScreen = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await screenResumes(
        jobDescription,
        resumes,
        apiProvider,
        apiProvider === "user" ? groqApiKey : undefined
      );
      setResults(response);
    } catch (err: any) {
      setError(
        err instanceof ApiError
          ? err.message
          : "Couldn't reach the screening service. Confirm the backend is running."
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
    setFromHistory(false);
  };

  const handleHistoryDetail = (detail: ScreeningResponse) => {
    setResults(detail);
    setFromHistory(true);
    setShowHistory(false);
  };

  return (
    <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6 sm:py-10">
      <div className="flex items-center justify-between">
        <Link
          to="/"
          className="inline-flex items-center gap-1.5 text-sm font-medium text-ink-soft transition-colors hover:text-ink"
        >
          <ArrowLeft size={15} />
          Back to Dashboard
        </Link>
        {!showHistory && !fromHistory && (
          <Button variant="secondary" size="sm" onClick={() => setShowHistory(true)}>
            <History size={16} /> <span className="hidden sm:inline">History</span>
          </Button>
        )}
      </div>

      <h1 className="mt-4 font-display text-2xl font-semibold tracking-tight text-ink sm:text-3xl">
        Resume Screening
      </h1>
      <p className="mt-2 max-w-2xl text-sm leading-relaxed text-ink-soft">
        Compare multiple resumes against a job description using AI-powered
        semantic screening.
      </p>

      {showHistory ? (
        <ResumeScreeningHistory onClose={() => setShowHistory(false)} onSelectDetail={handleHistoryDetail} />
      ) : !results ? (
        <div className="mt-8 grid grid-cols-1 gap-5 lg:grid-cols-2">
          <section className="rounded-2xl border border-border bg-surface p-5 sm:p-6">
            <h2 className="text-sm font-semibold text-ink">Job Description</h2>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the job description here..."
              rows={14}
              className="mt-3 w-full resize-none rounded-xl border border-border bg-canvas p-4 text-sm leading-relaxed text-ink outline-none placeholder:text-ink-faint focus:border-accent focus:ring-2 focus:ring-accent-ring"
            />
          </section>

          <section className="rounded-2xl border border-border bg-surface p-5 sm:p-6">
            <h2 className="text-sm font-semibold text-ink">Resume Upload</h2>
            <div className="mt-3">
              <FileUpload onFilesSelected={handleAddFiles} />
              <FileList files={resumes} onRemove={handleRemoveFile} />
            </div>
          </section>

          {/* AI Provider */}
          <section className="rounded-2xl border border-border bg-surface p-5 sm:p-6 lg:col-span-2">
            <h2 className="text-sm font-semibold text-ink">AI Provider</h2>
            <div className="mt-3 grid grid-cols-1 gap-3">
              <button
                onClick={() => setApiProvider("user")}
                className={`flex items-center gap-3 rounded-xl border p-4 text-left transition-colors ${
                  apiProvider === "user"
                    ? "border-accent bg-accent-soft"
                    : "border-border hover:border-border-strong"
                }`}
              >
                <div
                  className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full border ${
                    apiProvider === "user"
                      ? "border-accent bg-accent"
                      : "border-ink-faint"
                  }`}
                >
                  {apiProvider === "user" && (
                    <div className="h-2 w-2 rounded-full bg-white" />
                  )}
                </div>
                <div className="flex-1">
                  <span className="flex items-center gap-2 text-sm font-medium text-ink">
                    Use my Groq API Key
                    <span className="rounded bg-accent/10 px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-accent">
                      Recommended
                    </span>
                  </span>
                  <span className="mt-0.5 block text-xs text-ink-soft">
                    Best and most reliable experience.
                  </span>
                </div>
              </button>

              {apiProvider === "user" && (
                <div className="ml-7 mt-1 max-w-sm">
                  <label className="mb-1 block text-xs font-semibold uppercase tracking-wider text-ink-faint">
                    Groq API Key
                  </label>
                  {/* Dummy hidden fields to defeat aggressive browser password managers */}
                  <input type="text" name="fakeusernameremembered" className="hidden" aria-hidden="true" style={{ display: 'none' }} />
                  <input type="password" name="fakepasswordremembered" className="hidden" aria-hidden="true" style={{ display: 'none' }} />
                  <input
                    type="password"
                    name={`groq-api-key-${Math.random().toString(36).substring(2)}`}
                    autoComplete="new-password"
                    data-lpignore="true"
                    data-1p-ignore="true"
                    placeholder="Enter your Groq API key"
                    value={groqApiKey}
                    onChange={(e) => setGroqApiKey(e.target.value)}
                    className={`w-full rounded-lg border bg-canvas px-3 py-2 text-sm text-ink outline-none transition-colors focus:border-accent ${
                      hasNonAsciiKey
                        ? "border-warn focus:border-warn"
                        : "border-border"
                    }`}
                  />
                  {hasNonAsciiKey ? (
                    <p className="mt-1.5 text-xs font-medium text-warn">
                      ⚠ Your key contains invalid characters (e.g. an em dash instead of
                      a hyphen). Please re-copy the key directly from{" "}
                      <a
                        href="https://console.groq.com/keys"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="underline"
                      >
                        console.groq.com
                      </a>
                      .
                    </p>
                  ) : (
                    <p className="mt-1.5 text-xs text-ink-faint">
                      Your key is used only for this screening and is not stored.
                    </p>
                  )}
                </div>
              )}

              <button
                onClick={() => setApiProvider("evalynx")}
                className={`flex items-center gap-3 rounded-xl border p-4 text-left transition-colors ${
                  apiProvider === "evalynx"
                    ? "border-accent bg-accent-soft"
                    : "border-border hover:border-border-strong"
                }`}
              >
                <div
                  className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full border ${
                    apiProvider === "evalynx"
                      ? "border-accent bg-accent"
                      : "border-ink-faint"
                  }`}
                >
                  {apiProvider === "evalynx" && (
                    <div className="h-2 w-2 rounded-full bg-white" />
                  )}
                </div>
                <div>
                  <span className="block text-sm font-medium text-ink">
                    Use Evalynx Built-in API
                  </span>
                  <span className="mt-0.5 block text-xs text-ink-soft">
                    No API key required. Availability may be limited during high usage.
                  </span>
                </div>
              </button>
            </div>
          </section>

          <div className="lg:col-span-2">
            {error && <ErrorPopup error={error} />}
            <Button
               onClick={handleScreen}
              disabled={!canScreen || isLoading}
              className="w-full sm:w-auto"
            >
              {isLoading ? (
                <>
                  <Loader2 size={16} className="animate-spin" />
                  Screening...
                </>
              ) : (
                "Screen Resumes"
              )}
            </Button>
          </div>
        </div>
      ) : (
        <div className="mt-8">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <h2 className="font-display text-xl font-semibold text-ink">
                {fromHistory ? "Historical Screening Results" : "Screening Results"}
              </h2>
              <p className="mt-1 text-sm text-ink-faint">
                {results.total_candidates} candidates screened
              </p>
            </div>
            <div className="flex items-center gap-3">
              {fromHistory && (
                <Button variant="secondary" size="sm" onClick={() => { setResults(null); setShowHistory(true); setFromHistory(false); }}>
                  <ArrowLeft size={16} className="mr-1" /> Back to History
                </Button>
              )}
              <Button variant={fromHistory ? "primary" : "secondary"} size="sm" onClick={handleReset}>
                New Screening
              </Button>
            </div>
          </div>

          <div className="mt-6">
            <CandidateTable
              candidates={results.results}
              onSelect={setSelectedCandidate}
            />
          </div>
        </div>
      )}

      {selectedCandidate && (
        <CandidateDetails
          candidate={selectedCandidate}
          onClose={() => setSelectedCandidate(null)}
        />
      )}
    </div>
  );
}
