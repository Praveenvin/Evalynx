import { useState } from "react";
import { FileText, Sparkles, Target, X } from "lucide-react";
import type {
  InterviewConfig,
  InterviewMode,
  InterviewSource,
  ApiProvider,
} from "../types/interview";
import FileUpload from "./FileUpload";
import FileList from "./FileList";
import Button from "./Button";

interface InterviewSetupProps {
  onStart: (config: InterviewConfig) => void;
}

const durations = [15, 30, 40, 60];
const questionCounts = [5, 10, 15, 20];

export default function InterviewSetup({ onStart }: InterviewSetupProps) {
  const [source, setSource] = useState<InterviewSource>("role");
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [role, setRole] = useState("");
  const [skills, setSkills] = useState<string[]>([]);
  const [skillInput, setSkillInput] = useState("");
  const [mode, setMode] = useState<InterviewMode>("standard");
  const [duration, setDuration] = useState(30);
  const [questionCount, setQuestionCount] = useState(10);
  const [allowTyping, setAllowTyping] = useState(true);
  const [apiProvider, setApiProvider] = useState<ApiProvider>("user");
  const [groqApiKey, setGroqApiKey] = useState("");

  const addSkill = () => {
    const trimmed = skillInput.trim();
    if (trimmed && !skills.includes(trimmed)) {
      setSkills([...skills, trimmed]);
    }
    setSkillInput("");
  };

  const hasNonAsciiKey = apiProvider === "user" && /[^\x00-\x7F]/.test(groqApiKey);
  const canStart = (source === "role" ? role.trim().length > 0 : !!resumeFile) && !hasNonAsciiKey;

  return (
    <div className="flex flex-col gap-6">
      {/* Interview source */}
      <section className="rounded-2xl border border-border bg-surface p-5 sm:p-6">
        <h3 className="text-sm font-semibold text-ink">Interview Source</h3>
        <div className="mt-3 grid grid-cols-1 gap-3 sm:grid-cols-2">
          <button
            onClick={() => setSource("resume")}
            className={`flex items-center gap-3 rounded-xl border p-4 text-left transition-colors ${source === "resume"
                ? "border-accent bg-accent-soft"
                : "border-border hover:border-border-strong"
              }`}
          >
            <FileText size={18} className="text-accent" />
            <span className="text-sm font-medium text-ink">
              Based on Resume
            </span>
          </button>
          <button
            onClick={() => setSource("role")}
            className={`flex items-center gap-3 rounded-xl border p-4 text-left transition-colors ${source === "role"
                ? "border-accent bg-accent-soft"
                : "border-border hover:border-border-strong"
              }`}
          >
            <Target size={18} className="text-accent" />
            <span className="text-sm font-medium text-ink">
              Based on Role &amp; Skills
            </span>
          </button>
        </div>

        {source === "resume" ? (
          <div className="mt-4">
            <FileUpload
              multiple={false}
              label="resume"
              onFilesSelected={(files) => setResumeFile(files[0] ?? null)}
            />
            {resumeFile && (
              <FileList
                files={[resumeFile]}
                onRemove={() => setResumeFile(null)}
              />
            )}
          </div>
        ) : (
          <div className="mt-4 flex flex-col gap-4">
            <div>
              <label className="text-xs font-medium text-ink-faint">
                Role
              </label>
              <input
                value={role}
                onChange={(e) => setRole(e.target.value)}
                placeholder="e.g. Software Developer"
                className="mt-1.5 w-full rounded-lg border border-border bg-canvas px-3 py-2 text-sm text-ink outline-none focus:border-accent focus:ring-2 focus:ring-accent-ring"
              />
            </div>
            <div>
              <label className="text-xs font-medium text-ink-faint">
                Skills
              </label>
              <div className="mt-1.5 flex flex-wrap gap-2">
                {skills.map((skill) => (
                  <span
                    key={skill}
                    className="inline-flex items-center gap-1.5 rounded-full bg-accent-soft px-3 py-1 text-xs font-medium text-accent-hover"
                  >
                    {skill}
                    <button
                      onClick={() =>
                        setSkills(skills.filter((s) => s !== skill))
                      }
                      aria-label={`Remove ${skill}`}
                    >
                      <X size={12} />
                    </button>
                  </span>
                ))}
                <input
                  value={skillInput}
                  onChange={(e) => setSkillInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" || e.key === ",") {
                      e.preventDefault();
                      addSkill();
                    }
                  }}
                  onBlur={addSkill}
                  placeholder="+ Add"
                  className="w-24 rounded-full border border-dashed border-border-strong bg-transparent px-3 py-1 text-xs text-ink outline-none focus:border-accent"
                />
              </div>
            </div>
          </div>
        )}
      </section>

      {/* Interview mode */}
      <section className="rounded-2xl border border-border bg-surface p-5 sm:p-6">
        <h3 className="text-sm font-semibold text-ink">Interview Mode</h3>
        <div className="mt-3 grid grid-cols-1 gap-3 sm:grid-cols-2">
          <button
            onClick={() => setMode("standard")}
            className={`rounded-xl border p-4 text-left transition-colors ${mode === "standard"
                ? "border-accent bg-accent-soft"
                : "border-border hover:border-border-strong"
              }`}
          >
            <span className="text-sm font-medium text-ink">Standard</span>
            <p className="mt-1 text-xs leading-relaxed text-ink-soft">
              Generate the interview questions upfront.
            </p>
          </button>
          <button
            onClick={() => setMode("dynamic")}
            className={`relative rounded-xl border p-4 text-left transition-colors ${mode === "dynamic"
                ? "border-accent bg-accent-soft"
                : "border-border hover:border-border-strong"
              }`}
          >
            <span className="inline-flex items-center gap-1 text-sm font-medium text-ink">
              Dynamic
              <Sparkles size={13} className="text-accent" />
            </span>
            <p className="mt-1 text-xs leading-relaxed text-ink-soft">
              Generate the next question based on the previous answer.
            </p>
          </button>
        </div>
      </section>

      {/* Duration + question count */}
      <section className="grid grid-cols-1 gap-6 rounded-2xl border border-border bg-surface p-5 sm:grid-cols-2 sm:p-6">
        <div>
          <h3 className="text-sm font-semibold text-ink">Duration</h3>
          <div className="mt-3 flex flex-wrap gap-2">
            {durations.map((d) => (
              <button
                key={d}
                onClick={() => setDuration(d)}
                className={`rounded-lg border px-3 py-1.5 text-sm font-medium transition-colors ${duration === d
                    ? "border-accent bg-accent-soft text-accent-hover"
                    : "border-border text-ink-soft hover:border-border-strong"
                  }`}
              >
                {d} min
              </button>
            ))}
          </div>
        </div>
        <div>
          <h3 className="text-sm font-semibold text-ink">
            Number of Questions
          </h3>
          <div className="mt-3 flex flex-wrap gap-2">
            {questionCounts.map((q) => (
              <button
                key={q}
                onClick={() => setQuestionCount(q)}
                className={`rounded-lg border px-3 py-1.5 text-sm font-medium transition-colors ${questionCount === q
                    ? "border-accent bg-accent-soft text-accent-hover"
                    : "border-border text-ink-soft hover:border-border-strong"
                  }`}
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Answer method */}
      <section className="rounded-2xl border border-border bg-surface p-5 sm:p-6">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-ink">Answer Method</h3>
          <label className="flex cursor-pointer items-center gap-2">
            <input
              type="checkbox"
              checked={allowTyping}
              onChange={(e) => setAllowTyping(e.target.checked)}
              className="h-4 w-4 accent-accent"
            />
            <span className="text-sm text-ink-soft">Allow typing</span>
          </label>
        </div>
        <div className="mt-3 inline-flex items-center gap-2 rounded-lg bg-accent-soft px-3 py-2 text-sm font-medium text-accent-hover">
          {allowTyping ? "Voice + Text" : "Voice Only"}
        </div>
        <p className="mt-2 text-xs text-ink-faint">
          {allowTyping
            ? "Speak your answer or type it — both are available during the interview."
            : "Speak your answer using your microphone. Typing is disabled."}
        </p>
      </section>

      {/* API Provider */}
      <section className="rounded-2xl border border-border bg-surface p-5 sm:p-6">
        <h3 className="text-sm font-semibold text-ink">AI Provider</h3>
        <div className="mt-3 grid grid-cols-1 gap-3">
          <button
            onClick={() => setApiProvider("user")}
            className={`flex items-center gap-3 rounded-xl border p-4 text-left transition-colors ${apiProvider === "user"
                ? "border-accent bg-accent-soft"
                : "border-border hover:border-border-strong"
              }`}
          >
            <div
              className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full border ${apiProvider === "user"
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
                className={`w-full rounded-lg border bg-canvas px-3 py-2 text-sm text-ink outline-none transition-colors focus:border-accent ${hasNonAsciiKey
                    ? "border-warn focus:border-warn"
                    : "border-border"
                  }`}
              />
              {hasNonAsciiKey ? (
                <p className="mt-1.5 text-xs font-medium text-warn">
                  ⚠ Your key contains invalid characters (e.g. an em dash instead of a
                  hyphen). This happens when autocorrect is active. Please re-copy the
                  key directly from{" "}
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
                  Your key is used only for this interview and is not stored.
                </p>
              )}
            </div>
          )}

          <button
            onClick={() => setApiProvider("evalynx")}
            className={`flex items-center gap-3 rounded-xl border p-4 text-left transition-colors ${apiProvider === "evalynx"
                ? "border-accent bg-accent-soft"
                : "border-border hover:border-border-strong"
              }`}
          >
            <div
              className={`flex h-4 w-4 shrink-0 items-center justify-center rounded-full border ${apiProvider === "evalynx"
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

      <Button
        size="md"
        disabled={!canStart}
        onClick={() =>
          onStart({
            source,
            resumeFile,
            role,
            skills,
            mode,
            durationMinutes: duration,
            questionCount,
            allowTyping,
            apiProvider,
            groqApiKey: apiProvider === "user" ? groqApiKey : undefined,
          })
        }
        className="w-full sm:w-auto sm:self-end"
      >
        Start Interview
      </Button>
    </div>
  );
}
