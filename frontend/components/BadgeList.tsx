type Props = {
  title: string
  items: string[]
  tone?: 'blue' | 'green' | 'amber'
}

const toneMap = {
  blue: 'border-blue-500/30 bg-blue-500/10 text-blue-300',
  green: 'border-emerald-500/30 bg-emerald-500/10 text-emerald-300',
  amber: 'border-amber-500/30 bg-amber-500/10 text-amber-300',
}

export default function BadgeList({ title, items, tone = 'blue' }: Props) {
  return (
    <div>
      <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-300">{title}</h3>
      <div className="flex flex-wrap gap-2">
        {items.length ? (
          items.map((item) => (
            <span
              key={item}
              className={`rounded-full border px-3 py-1 text-xs font-medium ${toneMap[tone]}`}
            >
              {item}
            </span>
          ))
        ) : (
          <p className="text-sm text-slate-400">No items detected.</p>
        )}
      </div>
    </div>
  )
}
