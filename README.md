# RepoLens AI

RepoLens AI is a full-stack web application that analyzes a public GitHub repository and generates a high-level engineering summary.

It helps developers quickly understand:
- what a repository does
- which technologies it uses
- what architecture patterns it appears to follow
- what quality signals are present
- what improvements could be made

## Features

- Analyze any **public GitHub repository URL**
- Repository summary
- Tech stack detection
- Architecture insights
- Quality score
- Improvement suggestions
- Recent analysis history

## Tech Stack

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS

### Backend
- FastAPI
- Python
- Requests

## Local Development

### Backend
```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate   # Git Bash on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Create `frontend/.env.local`:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8001
```

Then open:
- Frontend: http://localhost:3000
- Backend docs: http://localhost:8001/docs

## Notes

- This MVP supports **public repositories only**
- It uses heuristic analysis and GitHub API metadata to generate insights
- You can later extend it with GitHub tokens, embeddings, or an LLM
