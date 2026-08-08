# Evalynx

AI-powered hiring workspace with two focused agents: **Resume Screening** and **Mock Interview**.

## Tech Stack

- React + TypeScript + Vite
- Tailwind CSS v4
- React Router
- Lucide React icons

## Getting Started

```bash
npm install
npm run dev
```

The app runs at `http://localhost:5173`.

## Environment

Set the backend base URL in `.env`:

```
VITE_API_BASE_URL=http://localhost:8000
```

## Structure

```
src/
  components/     Reusable UI building blocks
  pages/          Dashboard, Resume Screening, Mock Interview
  services/       API layer (resumeScreeningApi.ts, interviewApi.ts)
  types/          Shared TypeScript types
```

## Backend Integration

- **Resume Screening** calls `POST {VITE_API_BASE_URL}/api/resume-screening/screen`
  with `job_description` and `resumes` as `multipart/form-data`. This is wired
  to your existing FastAPI endpoint.
- **Mock Interview** has a complete service layer in `src/services/interviewApi.ts`
  (`start`, `answer`, `result`, `transcribe`) ready to connect once the backend
  is implemented. Until then, the chat flow runs on a local placeholder
  question set so the UI is fully demoable.

## Build

```bash
npm run build
```
