import { useState, type KeyboardEvent } from "react";
import { Link } from "react-router-dom";
import { ArrowLeft, Clock, GraduationCap, Loader2, X } from "lucide-react";
import Button from "../components/Button";
import Badge from "../components/Badge";
import { recommendCourses } from "../services/courseRecommendationApi";
import { ApiError } from "../services/api";
import type { CourseRecommendationResponse } from "../types/courseRecommendation";
import type { ApiProvider } from "../types/interview";
import ErrorPopup, { type ApiErrorDetail } from "../components/ErrorPopup";

function TagInput({
  label,
  placeholder,
  values,
  onChange,
}: {
  label: string;
  placeholder: string;
  values: string[];
  onChange: (values: string[]) => void;
}) {
  const [draft, setDraft] = useState("");

  const addTag = () => {
    const trimmed = draft.trim();
    if (trimmed && !values.includes(trimmed)) {
      onChange([...values, trimmed]);
    }
    setDraft("");
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" || e.key === ",") {
      e.preventDefault();
      addTag();
    }
  };

  return (
    <div>
      <label className="text-xs font-medium text-ink-faint">{label}</label>
      <div className="mt-1.5 flex flex-wrap items-center gap-2 rounded-lg border border-border bg-canvas px-2.5 py-2 focus-within:border-accent focus-within:ring-2 focus-within:ring-accent-ring">
        {values.map((v) => (
          <span
            key={v}
            className="inline-flex items-center gap-1.5 rounded-full bg-accent-soft px-3 py-1 text-xs font-medium text-accent-hover"
          >
            {v}
            <button
              type="button"
              onClick={() => onChange(values.filter((x) => x !== v))}
              aria-label={`Remove ${v}`}
            >
              <X size={12} />
            </button>
          </span>
        ))}
        <input
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={handleKeyDown}
          onBlur={addTag}
          placeholder={values.length === 0 ? placeholder : "+ Add"}
          className="min-w-[100px] flex-1 bg-transparent py-0.5 text-sm text-ink outline-none placeholder:text-ink-faint"
        />
      </div>
    </div>
  );
}

export default function CourseRecommendation() {
  const [name, setName] = useState("");
  const [education, setEducation] = useState("");
  const [background, setBackground] = useState("");
  const [careerGoal, setCareerGoal] = useState("");
  const [currentSkills, setCurrentSkills] = useState<string[]>([]);
  const [interests, setInterests] = useState<string[]>([]);

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | ApiErrorDetail | null>(null);
  const [result, setResult] = useState<CourseRecommendationResponse | null>(null);

  const [apiProvider, setApiProvider] = useState<ApiProvider>("user");
  const [groqApiKey, setGroqApiKey] = useState("");

  const hasNonAsciiKey = apiProvider === "user" && /[^\x00-\x7F]/.test(groqApiKey);
  const canSubmit = name.trim().length > 0 && careerGoal.trim().length > 0 && !hasNonAsciiKey;

  const handleSubmit = async () => {
    if (!canSubmit) return;
    setIsLoading(true);
    setError(null);
    try {
      const response = await recommendCourses({
        name: name.trim(),
        education: education.trim(),
        background: background.trim(),
        career_goal: careerGoal.trim(),
        current_skills: currentSkills,
        interests,
        api_provider: apiProvider,
        groq_api_key: apiProvider === "user" ? groqApiKey : undefined,
      });
      setResult(response);
    } catch (err: any) {
      setError(
        err instanceof ApiError
          ? err.message
          : "Couldn't generate a recommendation. Confirm the backend is running."
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 sm:py-10">
      <Link
        to="/"
        className="inline-flex items-center gap-1.5 text-sm font-medium text-ink-soft transition-colors hover:text-ink"
      >
        <ArrowLeft size={15} />
        Back to Dashboard
      </Link>

      <h1 className="mt-4 font-display text-2xl font-semibold tracking-tight text-ink sm:text-3xl">
        Course Recommendation
      </h1>
      <p className="mt-2 max-w-2xl text-sm leading-relaxed text-ink-soft">
        Get a personalized, ordered learning path based on your background,
        goals, and current skills.
      </p>

      {!result ? (
        <div className="mt-8 rounded-2xl border border-border bg-surface p-5 sm:p-6">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label className="text-xs font-medium text-ink-faint">Name</label>
              <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. Alex"
                className="mt-1.5 w-full rounded-lg border border-border bg-canvas px-3 py-2 text-sm text-ink outline-none placeholder:text-ink-faint focus:border-accent focus:ring-2 focus:ring-accent-ring"
              />
            </div>
            <div>
              <label className="text-xs font-medium text-ink-faint">
                Career Goal
              </label>
              <input
                value={careerGoal}
                onChange={(e) => setCareerGoal(e.target.value)}
                placeholder="e.g. Full Stack Developer"
                className="mt-1.5 w-full rounded-lg border border-border bg-canvas px-3 py-2 text-sm text-ink outline-none placeholder:text-ink-faint focus:border-accent focus:ring-2 focus:ring-accent-ring"
              />
            </div>
            <div>
              <label className="text-xs font-medium text-ink-faint">
                Education
              </label>
              <input
                value={education}
                onChange={(e) => setEducation(e.target.value)}
                placeholder="e.g. B.E. Computer Science"
                className="mt-1.5 w-full rounded-lg border border-border bg-canvas px-3 py-2 text-sm text-ink outline-none placeholder:text-ink-faint focus:border-accent focus:ring-2 focus:ring-accent-ring"
              />
            </div>
            <div>
              <label className="text-xs font-medium text-ink-faint">
                Background
              </label>
              <input
                value={background}
                onChange={(e) => setBackground(e.target.value)}
                placeholder="e.g. Computer Science graduate"
                className="mt-1.5 w-full rounded-lg border border-border bg-canvas px-3 py-2 text-sm text-ink outline-none placeholder:text-ink-faint focus:border-accent focus:ring-2 focus:ring-accent-ring"
              />
            </div>
          </div>

          <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
            <TagInput
              label="Current Skills"
              placeholder="e.g. HTML, CSS, JavaScript"
              values={currentSkills}
              onChange={setCurrentSkills}
            />
            <TagInput
              label="Interests (optional)"
              placeholder="e.g. Web Development"
              values={interests}
              onChange={setInterests}
            />
          </div>

          {/* AI Provider */}
          <section className="mt-4 rounded-2xl border border-border bg-surface p-5 sm:p-6">
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
                      Your key is used only for this recommendation and is not stored.
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

          {error && <ErrorPopup error={error} />}

          <Button
            onClick={handleSubmit}
            disabled={!canSubmit || isLoading}
            className="mt-5 w-full sm:w-auto"
          >
            {isLoading ? (
              <>
                <Loader2 size={16} className="animate-spin" />
                Generating...
              </>
            ) : (
              "Generate Recommendation"
            )}
          </Button>
        </div>
      ) : (
        <div className="mt-8">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <h2 className="font-display text-xl font-semibold text-ink">
                Learning Path for {result.career_goal}
              </h2>
              <p className="mt-1 text-sm text-ink-faint">
                {result.learning_path.length} step
                {result.learning_path.length === 1 ? "" : "s"} · {" "}
                {result.skill_gaps.length} skill gap
                {result.skill_gaps.length === 1 ? "" : "s"} identified
              </p>
            </div>
            <Button variant="secondary" size="sm" onClick={handleReset}>
              New Recommendation
            </Button>
          </div>

          <div className="mt-5 rounded-2xl border border-border bg-surface p-5 sm:p-6">
            <p className="text-sm leading-relaxed text-ink-soft">
              {result.summary}
            </p>

            {result.current_skills.length > 0 && (
              <div className="mt-4 flex flex-wrap gap-2">
                {result.current_skills.map((s) => (
                  <Badge key={s}>{s}</Badge>
                ))}
              </div>
            )}
          </div>

          {result.learning_path.length === 0 ? (
            <div className="mt-5 rounded-2xl border border-border bg-surface p-6 text-center text-sm text-ink-soft">
              {result.goal_supported 
                ? "No additional courses needed right now — you already cover the core skills for this goal."
                : "We currently do not offer courses for this specific career goal."}
            </div>
          ) : (
            <div className="mt-5 flex flex-col gap-4">
              {result.learning_path.map((step) => (
                <div
                  key={step.step}
                  className="flex gap-4 rounded-2xl border border-border bg-surface p-5 sm:p-6"
                >
                  <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-accent-soft font-display text-sm font-semibold text-accent">
                    {step.step}
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <h3 className="font-display text-base font-semibold text-ink">
                        {step.course}
                      </h3>
                      <Badge>{step.difficulty}</Badge>
                    </div>
                    <p className="mt-1.5 text-sm leading-relaxed text-ink-soft">
                      {step.reason}
                    </p>

                    <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-1.5 text-xs text-ink-faint">
                      <span className="inline-flex items-center gap-1">
                        <Clock size={12} /> {step.duration}
                      </span>
                      {step.prerequisites.length > 0 && (
                        <span className="inline-flex items-center gap-1">
                          <GraduationCap size={12} /> Prerequisites:{" "}
                          {step.prerequisites.join(", ")}
                        </span>
                      )}
                    </div>

                    {step.skills_gained.length > 0 && (
                      <div className="mt-3 flex flex-wrap gap-1.5">
                        {step.skills_gained.map((s) => (
                          <Badge key={s}>{s}</Badge>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
