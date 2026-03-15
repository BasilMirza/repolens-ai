'use client'

import { useEffect, useState } from 'react'

import BadgeList from '@/components/BadgeList'
import HistoryList from '@/components/HistoryList'
import { RepoAnalysis } from '@/lib/types'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
const sampleUrl = 'https://github.com/vercel/next.js'

export default function RepoLensForm() {
  const [repoUrl, setRepoUrl] = useState('')
  const [result, setResult] = useState<RepoAnalysis | null>(null)
  const [history, setHistory] = useState<RepoAnalysis[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const fetchHistory = async () => {
    const res = await fetch(`${API_BASE}/api/history`, { cache: 'no-store' })
    if (res.ok) {
      const data = await res.json()
      setHistory(data)
    }
  }

  useEffect(() => {
    fetchHistory().catch(() => {})
  }, [])

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const res = await fetch(`${API_BASE}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repo_url: repoUrl }),
      })
      const data = await res.json()

      if (!res.ok) {
        throw new Error(data.detail || 'Analysis failed.')
      }

      setResult(data)
      await fetchHistory()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unexpected error occurred.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-7xl px-6 py-10 lg:px-8">
      <header className="mb-10">
        <div className="mb-4 inline-flex rounded-full border border-violet-500/30 bg-violet-500/10 px-3 py-1 text-sm text-violet-300">
          GitHub Repository Intelligence
        </div>
        <h1 className="max-w-3xl text-4xl font-bold tracking-tight text-white sm:text-5xl">
          RepoLens AI
        </h1>
        <p className="mt-4 max-w-3xl text-lg leading-8 text-slate-300">
          Analyze any public GitHub repository and get a summary, stack detection, architecture insights, quality signals, and improvement suggestions.
        </p>
      </header>

      <div className="grid gap-8 lg:grid-cols-[1.05fr_0.95fr]">
        <section className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6 shadow-2xl shadow-black/20">
          <h2 className="mb-5 text-xl font-semibold text-white">Analyze Repository</h2>

          <form onSubmit={onSubmit} className="space-y-5">
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-200">GitHub repository URL</label>
              <input
                value={repoUrl}
                onChange={(e) => setRepoUrl(e.target.value)}
                className="w-full rounded-2xl border border-slate-700 bg-slate-950/70 px-4 py-3 text-sm text-slate-100 outline-none placeholder:text-slate-500 focus:border-violet-500"
                placeholder="https://github.com/owner/repo"
              />
            </div>

            {error && (
              <div className="rounded-2xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-300">
                {error}
              </div>
            )}

            <div className="flex flex-wrap gap-3">
              <button
                type="submit"
                disabled={loading}
                className="rounded-full bg-violet-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-violet-500 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? 'Analyzing...' : 'Analyze Repository'}
              </button>

              <button
                type="button"
                onClick={() => {
                  setRepoUrl(sampleUrl)
                  setError('')
                }}
                className="rounded-full border border-slate-700 px-5 py-3 text-sm font-semibold text-slate-200 transition hover:border-slate-500"
              >
                Load Sample Repo
              </button>
            </div>
          </form>
        </section>

        <section className="space-y-6">
          <div className="grid gap-4 sm:grid-cols-3">
            <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-5">
              <p className="text-sm uppercase tracking-wide text-slate-400">Quality Score</p>
              <p className="mt-3 text-4xl font-bold text-white">{result?.quality_score ?? '--'}</p>
            </div>
            <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-5">
              <p className="text-sm uppercase tracking-wide text-slate-400">Stars</p>
              <p className="mt-3 text-4xl font-bold text-white">{result?.stars ?? '--'}</p>
            </div>
            <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-5">
              <p className="text-sm uppercase tracking-wide text-slate-400">Forks</p>
              <p className="mt-3 text-4xl font-bold text-white">{result?.forks ?? '--'}</p>
            </div>
          </div>

          <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6">
            <h2 className="mb-2 text-xl font-semibold text-white">Repository Analysis</h2>
            <p className="text-sm text-slate-400">{result?.full_name || 'Run an analysis to see insights.'}</p>

            {result && (
              <>
                <p className="mt-4 text-sm text-slate-300">
                  <span className="font-medium text-slate-100">Description:</span> {result.description}
                </p>
                <p className="mt-3 text-sm text-slate-300">
                  <span className="font-medium text-slate-100">Repository Summary:</span> {result.repo_summary}
                </p>
                <p className="mt-3 text-sm text-slate-300">
                  <span className="font-medium text-slate-100">Architecture Insight:</span> {result.architecture_summary}
                </p>

                <div className="mt-5 space-y-4">
                  <BadgeList title="Detected Stack" items={result.detected_stack} tone="blue" />
                  <BadgeList title="Key Signals" items={result.key_signals} tone="green" />
                  <BadgeList title="Improvement Suggestions" items={result.improvement_suggestions} tone="amber" />
                </div>

                <div className="mt-5 rounded-2xl border border-slate-800 bg-slate-950/60 p-5">
                  <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-300">Language Breakdown</h3>
                  <div className="space-y-2">
                    {Object.entries(result.language_breakdown).length ? (
                      Object.entries(result.language_breakdown).map(([language, value]) => (
                        <div key={language}>
                          <div className="mb-1 flex items-center justify-between text-sm text-slate-300">
                            <span>{language}</span>
                            <span>{value.toLocaleString()}</span>
                          </div>
                          <div className="h-2 rounded-full bg-slate-800">
                            <div
                              className="h-2 rounded-full bg-violet-500"
                              style={{
                                width: `${Math.min(
                                  100,
                                  (value / Math.max(...Object.values(result.language_breakdown))) * 100
                                )}%`,
                              }}
                            />
                          </div>
                        </div>
                      ))
                    ) : (
                      <p className="text-sm text-slate-400">No language metadata returned.</p>
                    )}
                  </div>
                </div>
              </>
            )}
          </div>
        </section>
      </div>

      <div className="mt-8">
        <HistoryList items={history} />
      </div>
    </div>
  )
}
