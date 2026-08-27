import { useEffect, useMemo, useState } from 'react'
import { Activity, ChevronRight, CircleCheck, Cpu, History, RefreshCw } from 'lucide-react'
import { NavLink } from 'react-router-dom'
import { api, type HealthPayload, type SystemPayload } from '../api'
import { EmptyState, InlineState, LoadingRows, MetricCard, PageHeading, RunTable } from '../components'
import { useRuns } from '../hooks'

export function DashboardPage() {
  const { runs, loading: runsLoading, error: runsError, reload: reloadRuns } = useRuns()
  const [health, setHealth] = useState<HealthPayload | null>(null)
  const [system, setSystem] = useState<SystemPayload | null>(null)
  const [sideLoading, setSideLoading] = useState(true)
  const [sideError, setSideError] = useState<string | null>(null)
  const [reloadKey, setReloadKey] = useState(0)

  useEffect(() => {
    const controller = new AbortController()
    setSideLoading(true)
    setSideError(null)
    Promise.all([api.health(controller.signal), api.system(controller.signal)])
      .then(([healthPayload, systemPayload]) => {
        setHealth(healthPayload)
        setSystem(systemPayload)
      })
      .catch((reason: unknown) => {
        if (!controller.signal.aborted) {
          setSideError(reason instanceof Error ? reason.message : 'Unknown API error')
        }
      })
      .finally(() => {
        if (!controller.signal.aborted) setSideLoading(false)
      })
    return () => controller.abort()
  }, [reloadKey])

  const loading = runsLoading || sideLoading
  const error = runsError ?? sideError
  const recentRuns = useMemo(() => runs.slice(-6).reverse(), [runs])
  const completed = runs.filter((run) => run.status === 'completed').length
  const nonCompleted = runs.length - completed

  const reload = () => {
    reloadRuns()
    setReloadKey((key) => key + 1)
  }

  return (
    <>
      <PageHeading
        eyebrow="Research control room"
        title="Dashboard"
        description="A truthful overview of stored experiment evidence, application readiness, and current machine resources."
        action={
          <button type="button" className="button button-secondary" onClick={reload} disabled={loading}>
            <RefreshCw size={16} aria-hidden="true" /> Refresh
          </button>
        }
      />

      {error ? <InlineState tone="error" title="Dashboard data could not be loaded" detail={error} /> : null}

      <section className="metric-grid" aria-label="Dashboard summary">
        <MetricCard
          label="Finalized runs"
          value={runsLoading ? '—' : String(runs.length)}
          detail="Integrity-indexed run bundles"
          icon={<History size={18} aria-hidden="true" />}
        />
        <MetricCard
          label="Completed"
          value={runsLoading ? '—' : String(completed)}
          detail={nonCompleted ? `${nonCompleted} retained non-completed` : 'No retained non-completed indexed runs'}
          icon={<CircleCheck size={18} aria-hidden="true" />}
        />
        <MetricCard
          label="Runtime stream"
          value={health?.active_runtime_service === 'not-yet-implemented' ? 'Pending' : 'Available'}
          detail="T-530 adds active-run WebSocket state"
          icon={<Activity size={18} aria-hidden="true" />}
          tone="warning"
        />
        <MetricCard
          label="System snapshot"
          value={sideLoading ? '—' : system?.status === 'unavailable' ? 'Unavailable' : 'Available'}
          detail="Canonical local inventory collector"
          icon={<Cpu size={18} aria-hidden="true" />}
        />
      </section>

      <div className="content-grid content-grid-main">
        <section className="panel panel-large">
          <div className="panel-heading">
            <div>
              <span className="section-kicker">Recent evidence</span>
              <h2>Finalized run history</h2>
            </div>
            <NavLink className="text-link" to="/runs">
              Open runs <ChevronRight size={15} aria-hidden="true" />
            </NavLink>
          </div>
          {runsLoading ? (
            <LoadingRows />
          ) : recentRuns.length ? (
            <RunTable runs={recentRuns} />
          ) : (
            <EmptyState
              title="No finalized runs are indexed"
              detail="Persisted experiment evidence will appear here after the canonical registry contains finalized run bundles."
            />
          )}
        </section>

        <aside className="panel protocol-panel">
          <span className="section-kicker">Current gate</span>
          <h2>Pre-WP7 refinement</h2>
          <GateRow tone="info" title="Protocol v1.1" detail="Candidate — not frozen" />
          <GateRow tone="warning" title="Human application validation" detail="T-511 still required" />
          <GateRow tone="muted" title="Thesis writing" detail="Blocked until explicit approval" />
        </aside>
      </div>
    </>
  )
}

function GateRow({ tone, title, detail }: { tone: 'info' | 'warning' | 'muted'; title: string; detail: string }) {
  return (
    <div className="gate-row">
      <span className={`status-dot status-dot-${tone}`} aria-hidden="true" />
      <div>
        <strong>{title}</strong>
        <span>{detail}</span>
      </div>
    </div>
  )
}
