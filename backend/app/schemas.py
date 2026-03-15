from pydantic import BaseModel, HttpUrl

class RepoAnalysisRequest(BaseModel):
    repo_url: HttpUrl

class RepoAnalysisResponse(BaseModel):
    repo_name: str
    full_name: str
    description: str
    stars: int
    forks: int
    language_breakdown: dict[str, int]
    detected_stack: list[str]
    architecture_summary: str
    repo_summary: str
    quality_score: int
    improvement_suggestions: list[str]
    key_signals: list[str]
