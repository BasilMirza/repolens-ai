export type RepoAnalysis = {
  repo_name: string
  full_name: string
  description: string
  stars: number
  forks: number
  language_breakdown: Record<string, number>
  detected_stack: string[]
  architecture_summary: string
  repo_summary: string
  quality_score: number
  improvement_suggestions: string[]
  key_signals: string[]
}
