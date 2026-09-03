#!/usr/bin/env python3
"""One-shot branch reconciliation for the canonical thesis task ledger.

This temporary helper updates only known T-711/T-711A/T-538 status regions and fails
closed if the expected historical text is not present exactly once.
"""

from pathlib import Path

PATH = Path("docs/context/TASKS.md")
text = PATH.read_text(encoding="utf-8")
lines = text.splitlines()


def replace_single_prefix(prefix: str, replacement: str) -> None:
    matches = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one line starting {prefix!r}, found {len(matches)}")
    lines[matches[0]] = replacement


replace_single_prefix(
    "- **Project:**",
    "- **Project:** **8/8** master milestones objectively complete (#87). The accepted application and complete T-610→T-613 final v2.1 evidence chain have passed their objective gates. The user explicitly approved entry into WP7 on 2026-09-03; T-700, T-701, T-702 and T-710 are complete. T-711 review-ready Word composition is COMPLETE through PR #134 and the bounded synthesis enhancement PR #135; T-711A is the active pre-supervisor academic/compliance hardening task.",
)
replace_single_prefix(
    "- **Current task:**",
    "- **Current task:** `T-711A` is **IN_PROGRESS** on `thesis/t711a-final-hardening` / PR #136. It performs only bounded editorial/compliance hardening over the accepted T-711 document: source-grounded citation/wording corrections, targeted verified Related Work strengthening, Greek captions/headings and terminology normalization, RQ3 conditional-recovery clarification, accessibility/alt text, metadata cleanup, academic front/end-matter ordering, self-contained frozen configuration appendix, bibliography normalization, placeholder-aware final-mode QA and fresh complete Word visual QA. Frozen protocol-v2.1 science, T-611 evidence, T-612 estimands/results and registered T-613 scientific asset bytes remain immutable.",
)
replace_single_prefix(
    "- **Exact next action:**",
    "- **Exact next action:** continue `T-711A` only: finish the source-synchronized academic/compliance hardening, require green Repository/DOCX CI on the exact PR head, render the exact resulting Word artifact and visually inspect every final page. Then reconcile/merge T-711A. Do not start T-712 without actual supervisor/reviewer feedback and do not freeze T-713 while official student/declaration placeholders remain unresolved.",
)

# Replace the stale WP7 T-711 READY block, preserving the T-712 line and later history.
start_matches = [i for i, line in enumerate(lines) if line.startswith("- [ ] READY `T-711`")]
end_matches = [i for i, line in enumerate(lines) if line.startswith("- [ ] DEFERRED `T-712`")]
if len(start_matches) != 1 or len(end_matches) != 1 or end_matches[0] <= start_matches[0]:
    raise RuntimeError(
        f"Unexpected WP7 boundaries: T711={start_matches}, T712={end_matches}"
    )
start, end = start_matches[0], end_matches[0]
replacement_block = [
    "- [x] `T-711` — Produce and validate the review-ready editable Word thesis. COMPLETE.",
    "  - Depends on: `T-710` — satisfied.",
    "  - PR #134 composed the merged manuscript into a real editable `.docx`, converted validated citation-ready source IDs to IEEE numeric references, inserted all 24 planned registered scientific figures and three numbered Word tables, preserved Word headings/TOC/list/caption fields and passed structural plus full rendered-page QA; squash-merged as `8d67e578cd18253a46a8185bd00adfb2dc0f29e2`.",
    "  - PR #135 added one unnumbered composition-only ‘results at a glance’ synthesis graphic from already frozen RQ1/RQ2/RQ3 values, strengthened final-artifact provenance/hash QA and was squash-merged as `40ea5fdddd9d463916915d5655ea14c0bb869146`.",
    "  - Accepted T-711 review artifact before T-711A contained 24 registered scientific figures plus one synthesis graphic, 14 verified references and 3 Word tables with 83/83 pages covered by visual QA. No protocol, estimand, result, censoring decision or T-613 quantitative asset byte changed.",
    "- [ ] IN_PROGRESS `T-711A` — Final pre-supervisor academic/compliance hardening of the accepted T-711 thesis.",
    "  - Depends on: `T-711` — satisfied.",
    "  - Scope is editorial/composition only: correct the DQN foundation citation boundary; replace unsupported superiority/significance-style prose with neutral estimated-difference wording; strengthen Related Work only with synchronized verified citation-ready sources; normalize IEEE references from verified metadata; localize captions/headings and terminology; clarify conditional recovery for small recovered n; add figure alt text; scrub generic DOCX metadata; order glossary/references/appendices academically; make frozen method/configuration details self-contained; remove review-production appendix prose; enforce placeholder-aware final mode; and perform fresh full-document Word visual QA.",
    "  - Review builds may retain only the three explicitly known official-person/declaration placeholders. Final-mode/T-713 must fail on TODO/TBD/[να συμπληρωθεί]/[to be completed]/equivalent residue.",
    "  - Current implementation branch/PR: `thesis/t711a-final-hardening` / #136. Scientific boundary: no experiment rerun, no new estimand or p-value family, no changed numerical result, no changed right-censoring decision and no changed registered T-613 scientific media bytes.",
]
lines[start:end] = replacement_block

# Record bounded application polish without making it a thesis/science blocker.
if not any("`T-538`" in line for line in lines):
    t511_matches = [i for i, line in enumerate(lines) if line.startswith("- [x] `T-511`")]
    if len(t511_matches) != 1:
        raise RuntimeError(f"Expected one T-511 insertion anchor, found {len(t511_matches)}")
    i = t511_matches[0]
    t538 = [
        "- [ ] DEFERRED `T-538` — Bounded post-final application presentation polish.",
        "  - Non-scientific and not a T-711A/T-712/T-713 blocker.",
        "  - Reconcile the Experiment page with the completed/frozen final-study state; extend existing onboarding only where the end-to-end campaign→validation→evidence-finalization path is not already self-explanatory; add Run progress detail only when backed by stored runtime state and visually useful; optionally capture 2–4 authentic implementation screenshots for Chapter 4 if they improve explanation. Screenshots remain implementation illustrations, never scientific evidence.",
        "",
    ]
    lines[i:i] = t538

PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("Reconciled TASKS.md for T-711/T-711A/T-538")
