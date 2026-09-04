# Deliverable Retention Policy

**Effective:** 2026-09-05  
**Authority:** explicit user decision

## Rule

Every file surfaced to the user as a meaningful thesis/project deliverable must have a persistent repository copy. A local `/mnt/data` path or an expiring GitHub Actions artifact may be used as a working/cache location, but must never be the only retained copy of a delivered document.

## Storage convention

- `thesis/archive/` — immutable historical review/delivery milestones, including superseded or later-rejected versions that were meaningfully surfaced to the user.
- `thesis/final/` — only genuinely accepted final/submission candidates and their release metadata.
- QA reports/manifests that establish the identity or validation state of a delivered DOCX/PDF are retained next to the corresponding archived/final milestone.
- Stable filenames and SHA-256 hashes are recorded so later sessions can identify the exact document independently of chat history or temporary storage.

## Delivery gate

Before a new DOCX/PDF/release package is described as retained, review-ready, final, or otherwise handed off as a project deliverable:

1. run the applicable content/scientific/structural/visual QA;
2. commit the exact delivered bytes to the repository under the appropriate archive/final path;
3. record the version identity/hash and purpose in the relevant manifest/status documentation;
4. verify the repository copy exists on the integrated branch.

Temporary working files, render intermediates, helper-test documents, scratch ZIPs and duplicate byte-for-byte local copies do not need separate permanent retention unless they themselves were surfaced as meaningful deliverables or contain unique non-reproducible content.

## Thesis-specific clarification

The audit-reconciled T-715 reader-scoped DOCX is retained for provenance but is not the final thesis: on 2026-09-05 the user explicitly rejected its excessive reduction in length relative to the earlier full manuscript. The next full thesis must recover the fuller academic coverage while preserving the validated T-715 scientific corrections.
