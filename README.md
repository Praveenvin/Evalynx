# Evalynx
AI-powered candidate assessment platform featuring intelligent resume screening and personalized mock interviews with adaptive evaluation.


1. Clone & enter repo
powershell
git clone <repository-url>
cd Evalynx
2. Backend setup
powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
3. Configure environment variables
powershell
Copy-Item .env.example .env
notepad .env

Fill in:

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_STT_MODEL=whisper-large-v3-turbo
FRONTEND_ORIGIN=http://localhost:5173
4. Start backend (Terminal 1)
powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload

Verify at: http://127.0.0.1:8000/health → should return {"status": "ok"}

5. Start frontend (Terminal 2 — new window)
powershell
cd frontend
npm install
npm run dev

Open: http://localhost:5173


## About Evalynx

Evalynx is an AI-powered candidate assessment platform designed to streamline the initial stages of technical recruitment.

The platform combines resume screening with AI-powered mock interviews to evaluate candidates based on their resumes, target roles, technical skills, and interview responses.

The system provides two major assessment modules:

1. Resume Screening
2. AI Mock Interview

---

## Resume Screening

The Resume Screening module analyzes candidate resumes against a provided job description.

The candidate uploads a resume and provides the target job description. Evalynx extracts the resume content and uses AI to analyze how well the candidate matches the requirements of the role.

### Resume Screening Flow

```text
Candidate Resume
       |
       v
PDF Resume Extraction
       |
       v
Resume Content Analysis
       |
       v
Job Description Comparison
       |
       v
AI-Based Screening
       |
       v
Candidate Screening Result