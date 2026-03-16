# RepoLens AI

RepoLens AI is an AI-inspired GitHub repository intelligence tool that analyzes public repositories and generates insights about their technology stack, architecture, code quality, and potential improvements.

It is designed to help developers quickly understand unfamiliar repositories, detect engineering signals, and evaluate project quality without manually reading through the entire codebase.

## Features

- Analyze any public GitHub repository by URL
- Detect programming languages and likely technology stack
- Generate repository summaries
- Infer architecture patterns from structure and metadata
- Compute a quality score based on documentation, tests, CI/CD, and project signals
- Display GitHub metrics such as stars and forks
- Suggest improvements for maintainability and documentation
- Maintain recent analysis history in the UI

## Tech Stack

### Frontend
- Next.js
- TypeScript
- Tailwind CSS

### Backend
- FastAPI
- Python
- Requests

### Analysis Layer
- Rule-based repository inspection
- Heuristic architecture detection
- Metadata and file-structure analysis

## How It Works

1. The user enters a public GitHub repository URL.
2. The backend fetches repository metadata from the GitHub API.
3. RepoLens AI analyzes:
   - language breakdown
   - top-level repository structure
   - README contents
   - configuration files
   - development tooling signals
4. The system generates:
   - repository summary
   - detected stack
   - architecture insights
   - quality score
   - improvement suggestions

## Example Use Cases

- Quickly understand an open-source project before contributing
- Review repository health and engineering signals
- Evaluate stack and structure of unfamiliar codebases
- Generate developer-friendly insights for portfolio demos

## Project Structure

repolens-ai
│
├── backend
│   ├── app
│   │   ├── main.py
│   │   ├── analyzer.py
│   │   └── schemas.py
│   └── requirements.txt
│
├── frontend
│   ├── app
│   ├── components
│   └── lib
│
└── README.md

Running the Project Locally
Backend
cd backend
python -m venv .venv
source .venv/Scripts/activate   # Git Bash on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

Backend runs on:

http://localhost:8000

API docs are available at:

http://localhost:8000/docs
Frontend
cd frontend
npm install
npm run dev

Frontend runs on:

http://localhost:3000
Environment Variables

Create a file in:

frontend/.env.local

Add:

NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
API Endpoint
POST /api/analyze

Analyze a public GitHub repository.

Request body:

{
  "repo_url": "https://github.com/owner/repo"
}

Response includes:

repository name

full repository path

description

stars and forks

language breakdown

detected stack

architecture summary

repository summary

quality score

key signals

improvement suggestions

Why I Built This

I built RepoLens AI to explore how developer tooling can use repository metadata, project structure, and lightweight AI-style heuristics to generate practical engineering insights.

This project demonstrates:

GitHub API integration

backend analysis pipelines

frontend dashboard design

developer-focused product thinking

practical full-stack architecture

Future Improvements

LLM-powered repository summaries

deeper architecture inference using file trees

security and dependency risk analysis

repository comparison mode

support for private repositories with GitHub token authentication

Author

Basil Mirza

Full-Stack Software Engineer
React • Next.js • Python • Django • Node.js • AWS • DevOps
