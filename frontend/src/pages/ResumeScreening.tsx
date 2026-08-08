import { useState } from "react";
import { Link } from "react-router-dom";
import { ArrowLeft, Loader2 } from "lucide-react";
import FileUpload from "../components/FileUpload";
import FileList from "../components/FileList";
import Button from "../components/Button";
import CandidateTable from "../components/CandidateTable";
import CandidateDetails from "../components/CandidateDetails";
import { screenResumes } from "../services/resumeScreeningApi";
import type { CandidateResult, ScreeningResponse } from "../types/resumeScreening";
import { ApiError } from "../services/api";

export default function ResumeScreening() {
  const [jobDescription, setJobDescription] = useState("");
  const [resumes, setResumes] = useState<File[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<ScreeningResponse | null>(null);
  const [selectedCandidate, setSelectedCandidate] =
    useState<CandidateResult | null>(null);

  const canScreen = jobDescription.trim().length > 0 && resumes.length > 0;

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
      const response = await screenResumes(jobDescription, resumes);
      setResults(response);
    } catch (err) {
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
  };

  return (
    <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6 sm:py-10">
      <Link
        to="/"
        className="inline-flex items-center gap-1.5 text-sm font-medium text-ink-soft transition-colors hover:text-ink"
      >
        <ArrowLeft size={15} />
        Back to Dashboard
      </Link>

      <h1 className="mt-4 font-display text-2xl font-semibold tracking-tight text-ink sm:text-3xl">
        Resume Screening
      </h1>
      <p className="mt-2 max-w-2xl text-sm leading-relaxed text-ink-soft">
        Compare multiple resumes against a job description using AI-powered
        semantic screening.
      </p>

      {!results ? (
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

          <div className="lg:col-span-2">
            {error && (
              <p className="mb-4 rounded-lg bg-weak-soft px-4 py-3 text-sm text-weak">
                {error}
              </p>
            )}
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
                Screening Results
              </h2>
              <p className="mt-1 text-sm text-ink-faint">
                {results.total_candidates} candidates screened
              </p>
            </div>
            <Button variant="secondary" size="sm" onClick={handleReset}>
              New Screening
            </Button>
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
