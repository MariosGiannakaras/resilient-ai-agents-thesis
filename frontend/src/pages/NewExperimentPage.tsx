import { Play, Settings2, ShieldCheck } from 'lucide-react'
import { InlineState, PageHeading, RoadmapCard } from '../components'

export function NewExperimentPage() {
  return (
    <>
      <PageHeading
        eyebrow="Configure"
        title="New Experiment"
        description="Build a validated experiment from protocol-owned choices and review the exact resolved configuration before launch."
      />
      <InlineState
        tone="info"
        title="Configuration launch is intentionally not enabled yet"
        detail="T-521 must define the candidate protocol-v1.1 configuration surface and T-530 must expose a truthful runtime launch contract. This screen will not invent selectable values before those contracts exist."
      />
      <div className="content-grid content-grid-equal">
        <RoadmapCard step="01" title="Select scientific configuration" detail="Agent set, layout, uncertainty condition, seed/repetition plan, and only protocol-approved parameters." icon={<Settings2 size={20} aria-hidden="true" />} />
        <RoadmapCard step="02" title="Review resolved execution" detail="Exact protocol identity, run count, parameter values, resources, and blocking validation issues before launch." icon={<ShieldCheck size={20} aria-hidden="true" />} />
        <RoadmapCard step="03" title="Launch through runtime service" detail="A real backend run enters the active workspace; there is no browser-only simulation or placeholder execution." icon={<Play size={20} aria-hidden="true" />} />
      </div>
    </>
  )
}
