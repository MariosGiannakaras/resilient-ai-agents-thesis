import { BarChart3, Gauge, ShieldCheck } from 'lucide-react'
import { InlineState, PageHeading, RoadmapCard } from '../components'

export function ComparePage() {
  return (
    <>
      <PageHeading
        eyebrow="Analyze"
        title="Compare"
        description="Compare compatible agents and experiment groups with paired effects, uncertainty, counts, and condition/layout context."
      />
      <InlineState
        tone="info"
        title="The comparison contract is being upgraded with protocol v1.1"
        detail="Existing v1.0 evidence remains immutable. T-521/T-612 add the predeclared paired effects and 95% confidence intervals required for the F0/C0/D0 comparison; this page will render stored outputs rather than calculate ad-hoc claims in the browser."
      />
      <div className="content-grid content-grid-equal">
        <RoadmapCard step="A" title="Compatibility first" detail="Protocol, stage, metric version and aggregation compatibility are checked before a comparison is shown." icon={<ShieldCheck size={20} aria-hidden="true" />} />
        <RoadmapCard step="B" title="Component metrics" detail="Cumulative deficit, immediate degradation and terminal performance remain separate; no unlabeled composite resilience score." icon={<Gauge size={20} aria-hidden="true" />} />
        <RoadmapCard step="C" title="Paired uncertainty" detail="Effects, 95% confidence intervals and explicit n are presented with per-layout and condition breakdowns." icon={<BarChart3 size={20} aria-hidden="true" />} />
      </div>
    </>
  )
}
