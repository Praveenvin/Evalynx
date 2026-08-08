# Evalynx

AI-powered candidate assessment platform featuring intelligent resume screening and personalized mock interviews with adaptive evaluation.

## Overview

Evalynx is an AI-powered candidate assessment platform designed to streamline the initial stages of technical recruitment.

The platform combines resume screening with AI-powered mock interviews to evaluate candidates based on their resumes, target roles, technical skills, and interview responses.

The system provides two major assessment modules:

1. Resume Screening
2. AI Mock Interview

## Features

### Resume Screening

- Upload candidate resumes in PDF format
- Extract resume content automatically
- Compare candidate profiles against a job description
- AI-powered candidate evaluation
- Identify relevant skills and experience
- Generate screening results based on job requirements

### AI Mock Interview

- Interview based on resume or selected role and skills
- Standard interview mode with questions generated upfront
- Dynamic interview mode with questions generated based on previous answers
- Configurable interview duration
- Configurable number of questions
- Voice-first answering experience
- Optional text-based answering
- Voice transcription for candidate answers
- Text-to-speech for interviewer questions
- Replay interviewer questions
- Review voice transcripts before submitting
- Per-answer AI evaluation
- Final interview score and summary
- Automatic interview submission when the timer expires

### Interview Evaluation

Each answer is evaluated across multiple categories:

- Technical Knowledge
- Communication
- Problem Solving
- Relevance

The final score is calculated locally from the individual answer evaluations using configurable weights rather than relying on a single AI-generated overall score.

Current weighting:

```text
Technical Knowledge    30%
Communication          25%
Problem Solving        25%
Relevance              20%



## Getting Started

Follow the steps below to run Evalynx locally.

### Prerequisites

Make sure the following are installed:

- Python 3.10+
- Node.js 18+
- npm
- Git
- Groq API key

### 1. Clone the Repository

```bash
git clone https://github.com/Praveenvin/Evalynx.git
cd Evalynx

2. Set Up the Backend

Open a terminal and navigate to the backend directory:

cd backend

Create a Python virtual environment:

python -m venv venv

Activate the virtual environment:

.\venv\Scripts\Activate.ps1

Install the required Python packages:

pip install -r requirements.txt
3. Configure Environment Variables

The repository includes an .env.example file containing the required configuration.

Create your local .env file:

Copy-Item .env.example .env

Open the .env file:

notepad .env

Add your configuration:

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_STT_MODEL=whisper-large-v3-turbo
FRONTEND_ORIGIN=http://localhost:5173

Replace your_groq_api_key with your actual Groq API key.

Do not commit the .env file to GitHub.

4. Start the Backend

Keep the backend terminal open and run:

uvicorn app.main:app --reload

The backend will start at:

http://127.0.0.1:8000

You can verify that the backend is running by opening:

http://127.0.0.1:8000/health

Expected response:

{
  "status": "ok"
}
5. Set Up the Frontend

Open a new terminal window.

Navigate to the frontend directory:

cd frontend

Install the frontend dependencies:

npm install

Start the development server:

npm run dev

The frontend will be available at:

http://localhost:5173

Open the URL in your browser to use Evalynx.