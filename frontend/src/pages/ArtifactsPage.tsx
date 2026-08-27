import { Archive, Boxes, Waypoints } from 'lucide-react'
import { InlineState, PageHeading, RoadmapCard } from '../components'

export function ArtifactsPage() {
  return (
    <>
      <PageHeading
        eyebrow="Trace & export"
        title="Artifacts"
        description="Inspect real figures, tables, data exports, manifests, and provenance without cluttering the primary analysis views."
      />
      <InlineState
        tone="info"
        title="Artifact browser migration is not complete"
        detail="The React view will enumerate existing version-controlled CSV/JSON/HTML evidence through a bounded FastAPI artifact contract. Files will never be relabeled or regenerated merely to fit the UI."
      />
      <div className="content-grid content-grid-equal">
        <RoadmapCard step="01" title="Figures & tables" detail="Preview real generated analysis outputs and export the exact stored files." icon={<Boxes size={20} aria-hidden="true" />} />
        <RoadmapCard step="02" title="Evidence provenance" detail="Trace source runs, protocol/config identity, analysis version and checksums through expandable detail." icon={<Waypoints size={20} aria-hidden="true" />} />
        <RoadmapCard step="03" title="Historical integrity" detail="v1.0 evidence remains archived and immutable when v1.1 becomes the accepted replacement path." icon={<Archive size={20} aria-hidden="true" />} />
      </div>
    </>
  )
}
