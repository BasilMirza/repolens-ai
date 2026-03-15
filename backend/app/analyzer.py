from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

import requests

GITHUB_API = "https://api.github.com"


def parse_repo_url(repo_url: str) -> tuple[str, str]:
    parsed = urlparse(repo_url)
    if "github.com" not in parsed.netloc:
        raise ValueError("Only GitHub repository URLs are supported.")

    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 2:
        raise ValueError("Repository URL must look like https://github.com/owner/repo")

    owner, repo = parts[0], parts[1].removesuffix(".git")
    return owner, repo


def _get_json(url: str) -> Any:
    response = requests.get(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "RepoLens-AI",
        },
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


def fetch_repo_data(owner: str, repo: str) -> dict[str, Any]:
    repo_meta = _get_json(f"{GITHUB_API}/repos/{owner}/{repo}")
    languages = _get_json(f"{GITHUB_API}/repos/{owner}/{repo}/languages")
    contents = _get_json(f"{GITHUB_API}/repos/{owner}/{repo}/contents")
    readme_text = ""

    try:
        readme = _get_json(f"{GITHUB_API}/repos/{owner}/{repo}/readme")
        if isinstance(readme, dict) and readme.get("download_url"):
            readme_res = requests.get(readme["download_url"], timeout=20)
            if readme_res.ok:
                readme_text = readme_res.text[:5000]
    except Exception:
        readme_text = ""

    return {
        "meta": repo_meta,
        "languages": languages if isinstance(languages, dict) else {},
        "contents": contents if isinstance(contents, list) else [],
        "readme_text": readme_text,
    }


def detect_stack(languages: dict[str, int], contents: list[dict[str, Any]], readme_text: str) -> list[str]:
    stack = set()
    names = {item.get("name", "").lower() for item in contents}
    readme = readme_text.lower()

    for lang in languages.keys():
        stack.add(lang)

    file_to_stack = {
        "package.json": "Node.js",
        "package-lock.json": "npm",
        "yarn.lock": "Yarn",
        "pnpm-lock.yaml": "pnpm",
        "requirements.txt": "Python",
        "pyproject.toml": "Python",
        "dockerfile": "Docker",
        "docker-compose.yml": "Docker Compose",
        "docker-compose.yaml": "Docker Compose",
        "go.mod": "Go",
        "pom.xml": "Java / Maven",
        "cargo.toml": "Rust",
        "composer.json": "PHP",
        "gemfile": "Ruby",
        "tsconfig.json": "TypeScript",
        "next.config.js": "Next.js",
        "next.config.mjs": "Next.js",
        "vite.config.ts": "Vite",
        "vite.config.js": "Vite",
        "tailwind.config.js": "Tailwind CSS",
        "tailwind.config.ts": "Tailwind CSS",
        "schema.prisma": "Prisma",
        ".github": "GitHub Actions",
    }

    for file_name, tech in file_to_stack.items():
        if file_name in names:
            stack.add(tech)

    keyword_map = {
        "react": "React",
        "next.js": "Next.js",
        "nextjs": "Next.js",
        "django": "Django",
        "fastapi": "FastAPI",
        "express": "Express",
        "nestjs": "NestJS",
        "postgres": "PostgreSQL",
        "mongodb": "MongoDB",
        "mysql": "MySQL",
        "redis": "Redis",
        "docker": "Docker",
        "kubernetes": "Kubernetes",
        "tailwind": "Tailwind CSS",
        "tensorflow": "TensorFlow",
        "pytorch": "PyTorch",
    }

    for keyword, tech in keyword_map.items():
        if keyword in readme:
            stack.add(tech)

    preferred_order = [
        "TypeScript",
        "JavaScript",
        "Python",
        "Go",
        "Java",
        "Rust",
        "PHP",
        "Ruby",
        "React",
        "Next.js",
        "Node.js",
        "Express",
        "Django",
        "FastAPI",
        "NestJS",
        "PostgreSQL",
        "MySQL",
        "MongoDB",
        "Redis",
        "Docker",
        "Docker Compose",
        "Kubernetes",
        "GitHub Actions",
        "Tailwind CSS",
        "Prisma",
        "TensorFlow",
        "PyTorch",
        "Vite",
    ]

    ordered = [item for item in preferred_order if item in stack]
    remaining = sorted([item for item in stack if item not in ordered])
    return ordered + remaining


def summarize_architecture(contents: list[dict[str, Any]], stack: list[str], readme_text: str) -> str:
    names = {item.get("name", "").lower() for item in contents}
    bullets = []

    if {"frontend", "backend"}.issubset(names) or {"client", "server"}.issubset(names):
        bullets.append(
            "The repository appears to separate frontend and backend concerns into distinct application layers."
        )
    elif "src" in names:
        bullets.append(
            "The repository appears to follow a source-centric structure with implementation code organized under a src directory."
        )
    else:
        bullets.append(
            "The repository appears to use a relatively flat top-level structure with core implementation files and configuration at the root."
        )

    if "Docker" in stack:
        bullets.append(
            "Containerization is present, suggesting support for reproducible local development or deployment workflows."
        )

    if "GitHub Actions" in stack or ".github" in names:
        bullets.append(
            "CI/CD automation signals are present through GitHub workflow configuration."
        )

    if any(db in stack for db in ["PostgreSQL", "MySQL", "MongoDB", "Redis"]):
        bullets.append(
            "The project appears to include persistent storage or caching infrastructure in its architecture."
        )

    if any(api in readme_text.lower() for api in ["api", "rest", "graphql"]):
        bullets.append(
            "The documentation suggests an API-driven architecture for data exchange or service integration."
        )

    return " ".join(bullets[:3])


def summarize_repo(meta: dict[str, Any], stack: list[str], readme_text: str) -> str:
    full_name = meta.get("full_name", "This repository")
    description = (meta.get("description") or "").strip()
    stars = int(meta.get("stargazers_count", 0))
    forks = int(meta.get("forks_count", 0))

    stack_text = ", ".join(stack[:4]) if stack else "multiple technologies"
    readme_lower = readme_text.lower()

    summary_parts = []

    if description:
        summary_parts.append(f"{full_name} is a public GitHub repository. {description}")
    else:
        summary_parts.append(f"{full_name} is a public GitHub repository with no explicit GitHub description provided.")

    if stack:
        summary_parts.append(f"The detected stack suggests the project is built with {stack_text}.")

    if {"frontend", "backend"}.issubset({item.strip().lower() for item in readme_text.split()}):
        summary_parts.append("The repository likely follows a full-stack structure with separate frontend and backend concerns.")
    elif "next.js" in readme_lower or "react" in readme_lower:
        summary_parts.append("The repository appears to include a modern frontend application focused on component-based development.")
    elif "fastapi" in readme_lower or "django" in readme_lower or "express" in readme_lower:
        summary_parts.append("The repository appears to include backend or API-oriented application logic.")

    if stars > 0 or forks > 0:
        summary_parts.append(f"It has {stars} stars and {forks} forks, indicating some level of public visibility and reuse.")

    return " ".join(summary_parts[:4])


def compute_quality_score(
    meta: dict[str, Any],
    contents: list[dict[str, Any]],
    readme_text: str,
    stack: list[str],
) -> tuple[int, list[str], list[str]]:
    names = {item.get("name", "").lower() for item in contents}
    score = 45
    signals = []
    suggestions = []

    if readme_text.strip():
        score += 10
        signals.append("Repository includes a README, which improves discoverability and onboarding.")
    else:
        suggestions.append("Add or expand README documentation to explain setup, architecture, and usage.")

    if "license" in names or "license.md" in names:
        score += 5
        signals.append("License file detected, which helps clarify repository usage terms.")
    else:
        suggestions.append("Add a license file if the repository is intended for public use or collaboration.")

    if "tests" in names or "__tests__" in names or "pytest.ini" in names:
        score += 10
        signals.append("Test-related files or directories are present, suggesting some validation coverage.")
    else:
        suggestions.append("Add automated tests or surface testing instructions to improve confidence and maintainability.")

    if ".github" in names:
        score += 8
        signals.append("GitHub workflow configuration suggests CI/CD or automation support.")

    if "dockerfile" in names or "docker-compose.yml" in names or "docker-compose.yaml" in names:
        score += 7
        signals.append("Containerization files are present, which improves reproducibility across environments.")

    if meta.get("stargazers_count", 0) > 50:
        score += 5
        signals.append("The repository has meaningful community interest based on star count.")

    if not meta.get("description"):
        suggestions.append("Add a concise repository description to make the project easier to understand at a glance.")

    if not any(db in stack for db in ["PostgreSQL", "MySQL", "MongoDB", "Redis"]) and any(
        x in stack for x in ["Node.js", "FastAPI", "Django"]
    ):
        suggestions.append("Document persistence choices or database usage if the application includes backend services.")

    if len(stack) < 2:
        suggestions.append("Document the main runtime and tooling more clearly so the tech stack is easier to identify.")

    score = max(0, min(100, score))
    return score, signals[:5], suggestions[:5]


def analyze_repository(repo_url: str) -> dict[str, Any]:
    owner, repo = parse_repo_url(repo_url)
    data = fetch_repo_data(owner, repo)
    meta = data["meta"]
    languages = data["languages"]
    contents = data["contents"]
    readme_text = data["readme_text"]

    stack = detect_stack(languages, contents, readme_text)
    architecture_summary = summarize_architecture(contents, stack, readme_text)
    repo_summary = summarize_repo(meta, stack, readme_text)
    quality_score, key_signals, suggestions = compute_quality_score(meta, contents, readme_text, stack)

    description = meta.get("description") or "No repository description available."

    return {
        "repo_name": meta.get("name", repo),
        "full_name": meta.get("full_name", f"{owner}/{repo}"),
        "description": description,
        "stars": int(meta.get("stargazers_count", 0)),
        "forks": int(meta.get("forks_count", 0)),
        "language_breakdown": languages,
        "detected_stack": stack,
        "architecture_summary": architecture_summary,
        "repo_summary": repo_summary,
        "quality_score": quality_score,
        "improvement_suggestions": suggestions,
        "key_signals": key_signals,
    }