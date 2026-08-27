import { History, RefreshCw, Route } from 'lucide-react'
import { Capability, EmptyState, InlineState, LoadingRows, PageHeading, RunTable } from '../components'
import { useRuns } from '../hooks'

export function RunsPage() {
  const { runs, loading, error, reload } = useRuns()
  return (
    <>
      <PageHeading
        eyebrow="Monitor & inspect"
        title="Runs"
        description="The central workspace for active execution, live GridWorld observation, event timelines, retained history, and run-level evidence."
        action={
          <button type="button" className="button button-secondary" onClick={reload} disabled={loading}>
            <RefreshCw size={16} aria-hidden="true" /> Refresh history
          </button>
        }
      />
      <div className="content-grid content-grid-main">
        <section className="panel panel-large">
          <div className="panel-heading">
            <div><span className="section-kicker">Live workspace</span><h2>Active run observer</h2></div>
            <span className="badge badge-warning">Runtime service pending</span>
          </div>
          <div className="gridworld-unavailable">
            <div className="gridworld-mark" aria-hidden="true"><Route size={32} strokeWidth={1.5} /></div>
            <div>
              <h3>No live trajectory is being fabricated</h3>
              <p>T-530 will stream real observer state through WebSocket. Until then this surface remains explicitly unavailable rather than drawing a synthetic GridWorld path.</p>
            </div>
          </div>
        </section>
        <aside className="panel">
          <span className="section-kicker">Capabilities</span>
          <h2>Lifecycle controls</h2>
          <Capability label="Stop / cancel" status="Awaiting runtime contract" />
          <Capability label="Restart" status="Awaiting safe-state contract" />
          <Capability label="Pause / resume" status="Unsupported unless proven safe" />
        </aside>
      </div>

      <section className="panel panel-spaced">
        <div className="panel-heading">
          <div><span className="section-kicker">Stored evidence</span><h2>Finalized history</h2></div>
          <span className="badge">{loading ? 'Loading' : `${runs.length} indexed`}</span>
        </div>
        {error ? <InlineState tone="error" title="Run history unavailable" detail={error} /> : null}
        {!error && (loading
          ? <LoadingRows />
          : runs.length
            ? <RunTable runs={[...runs].reverse()} />
            : <EmptyState title="No finalized runs" detail="Finalized evidence will appear here when indexed." />)}
        {!loading && runs.length > 0 ? (
          <p className="panel-footnote"><History size={14} aria-hidden="true" /> Historical run replay is available only when the retained bundle contains step trace data.</p>
        ) : null}
      </section>
    </>
  )
}
