import type { ReactNode } from 'react'
import { CircleAlert, CircleCheck, History } from 'lucide-react'
import type { RunRecord } from './api'

export function PageHeading({
  eyebrow,
  title,
  description,
  action,
}: {
  eyebrow: string
  title: string
  description: string
  action?: ReactNode
}) {
  return (
    <div className="page-heading">
      <div>
        <span className="eyebrow">{eyebrow}</span>
        <h1>{title}</h1>
        <p>{description}</p>
      </div>
      {action ? <div className="page-heading-action">{action}</div> : null}
    </div>
  )
}

export function MetricCard({
  label,
  value,
  detail,
  icon,
  tone = 'default',
}: {
  label: string
  value: string
  detail: string
  icon: ReactNode
  tone?: 'default' | 'warning'
}) {
  return (
    <article className={`metric-card${tone === 'warning' ? ' metric-card-warning' : ''}`}>
      <div className="metric-card-top">
        <span>{label}</span>
        <span className="metric-icon">{icon}</span>
      </div>
      <strong>{value}</strong>
      <small>{detail}</small>
    </article>
  )
}

export function InlineState({
  tone,
  title,
  detail,
}: {
  tone: 'info' | 'error'
  title: string
  detail: string
}) {
  const Icon = tone === 'error' ? CircleAlert : CircleCheck
  return (
    <div className={`inline-state inline-state-${tone}`} role={tone === 'error' ? 'alert' : 'status'}>
      <Icon size={19} aria-hidden="true" />
      <div>
        <strong>{title}</strong>
        <span>{detail}</span>
      </div>
    </div>
  )
}

export function RoadmapCard({
  step,
  title,
  detail,
  icon,
}: {
  step: string
  title: string
  detail: string
  icon: ReactNode
}) {
  return (
    <article className="roadmap-card">
      <div className="roadmap-card-top">
        <span className="roadmap-step">{step}</span>
        <span className="roadmap-icon">{icon}</span>
      </div>
      <h2>{title}</h2>
      <p>{detail}</p>
    </article>
  )
}

export function EmptyState({
  title,
  detail,
}: {
  title: string
  detail: string
}) {
  return (
    <div className="empty-state">
      <div className="empty-state-icon">
        <History size={22} aria-hidden="true" />
      </div>
      <strong>{title}</strong>
      <span>{detail}</span>
    </div>
  )
}

export function LoadingRows() {
  return (
    <div className="loading-rows" aria-label="Loading data">
      <span />
      <span />
      <span />
    </div>
  )
}

export function RunTable({ runs }: { runs: RunRecord[] }) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Run</th>
            <th>Status</th>
            <th>Protocol</th>
            <th>Stage</th>
            <th>Finished</th>
          </tr>
        </thead>
        <tbody>
          {runs.map((run) => (
            <tr key={run.run_id}>
              <td className="run-id">{run.run_id}</td>
              <td><StatusLabel status={run.status} /></td>
              <td>{run.protocol_version}</td>
              <td>{humanize(run.stage)}</td>
              <td>{formatTimestamp(run.finished_at_utc)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export function Capability({ label, status }: { label: string; status: string }) {
  return (
    <div className="capability-row">
      <span>{label}</span>
      <small>{status}</small>
    </div>
  )
}

function StatusLabel({ status }: { status: string }) {
  const normalized = status.toLowerCase()
  const tone = normalized === 'completed'
    ? 'success'
    : normalized === 'failed' || normalized === 'invalid'
      ? 'error'
      : 'warning'
  return (
    <span className={`status-label status-label-${tone}`}>
      <span className="status-dot" aria-hidden="true" />
      {humanize(status)}
    </span>
  )
}

function humanize(value: string) {
  return value
    .replaceAll('_', ' ')
    .replaceAll('-', ' ')
    .replace(/\b\w/g, (match) => match.toUpperCase())
}

function formatTimestamp(value: string | null) {
  if (!value) return '—'
  const date = new Date(value)
  if (Number.isNaN(date.valueOf())) return value
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(date)
}
