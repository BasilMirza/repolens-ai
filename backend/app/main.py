from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

from .analyzer import analyze_repository
from .schemas import RepoAnalysisRequest, RepoAnalysisResponse

app = FastAPI(title="RepoLens AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

history: list[dict] = []


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/analyze", response_model=RepoAnalysisResponse)
def analyze_repo(payload: RepoAnalysisRequest):
    try:
        result = analyze_repository(str(payload.repo_url))
        history.insert(0, result)
        if len(history) > 10:
            del history[10:]
        return result
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else 502
        if status == 404:
            raise HTTPException(status_code=404, detail="Repository not found or not publicly accessible.")
        if status == 403:
            raise HTTPException(status_code=403, detail="GitHub API rate limit reached. Try again later.")
        raise HTTPException(status_code=502, detail="Failed to fetch repository data from GitHub.")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected server error during repository analysis.")


@app.get("/api/history")
def get_history():
    return history[:10]
