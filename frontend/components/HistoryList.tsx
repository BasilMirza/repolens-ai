import { RepoAnalysis } from '@/lib/types'

export default function HistoryList({ items }: { items: RepoAnalysis[] }) {
  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6">
      <h2 className="mb-4 text-xl font-semibold text-white">Recent Analyses</h2>
      {items.length === 0 ? (
        <p className="text-sm text-slate-400">No analyses yet.</p>
      ) : (
        <div className="space-y-3">
          {items.map((item) => (
            <div key={`${item.full_name}-${item.quality_score}`} className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
              <p className="font-medium text-slate-100">{item.full_name}</p>
              <p className="mt-1 text-sm text-slate-400">Quality score: {item.quality_score}/100</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
