#!/usr/bin/env python3
from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one match, found {count}: {old[:120]!r}")
    p.write_text(text.replace(old, new), encoding="utf-8")

# TASKS.md canonical resume state.
replace_once(
    "docs/context/TASKS.md",
    "- **Project:** **8/8** master milestones objectively complete (#87). The accepted application and complete T-610→T-613 final v2.1 evidence chain have passed their objective gates. The user explicitly approved entry into WP7 on 2026-09-03; T-700, T-701, T-702 and T-710 are complete. T-711 review-ready Word composition is COMPLETE through PR #134 and the bounded synthesis enhancement PR #135; T-714 is the active pre-supervisor academic/compliance hardening task.",
    "- **Project:** **8/8** master milestones objectively complete (#87). The accepted application and complete T-610→T-613 final v2.1 evidence chain have passed their objective gates. The user explicitly approved entry into WP7 on 2026-09-03; T-700, T-701, T-702, T-710 and T-711 are complete. T-714 pre-supervisor academic/compliance hardening is also COMPLETE through PR #136, squash-merged as `42afba20fd5a7e9d3912418d0847b42e566aaca0`.",
)
replace_once(
    "docs/context/TASKS.md",
    "- **Current task:** `T-714` is **IN_PROGRESS** on `thesis/t711a-final-hardening` / PR #136. It performs only bounded editorial/compliance hardening over the accepted T-711 document: source-grounded citation/wording corrections, targeted verified Related Work strengthening, Greek captions/headings and terminology normalization, RQ3 conditional-recovery clarification, accessibility/alt text, metadata cleanup, academic front/end-matter ordering, self-contained frozen configuration appendix, bibliography normalization, placeholder-aware final-mode QA and fresh complete Word visual QA. Frozen protocol-v2.1 science, T-611 evidence, T-612 estimands/results and registered T-613 scientific asset bytes remain immutable.",
    "- **Current task:** `T-712` is **DEFERRED / WAITING FOR ACTUAL SUPERVISOR OR REVIEWER FEEDBACK**. T-714 is complete; no further internal rewrite cycle is authorized by default. The next input-bound action is to review/share the hardened Word thesis and supply real corrections when they exist. Frozen protocol-v2.1 science, T-611 evidence, T-612 estimands/results and registered T-613 scientific asset bytes remain immutable.",
)
replace_once(
    "docs/context/TASKS.md",
    "- **Exact next action:** continue `T-714` only: finish the source-synchronized academic/compliance hardening, require green Repository/DOCX CI on the exact PR head, render the exact resulting Word artifact and visually inspect every final page. Then reconcile/merge T-714. Do not start T-712 without actual supervisor/reviewer feedback and do not freeze T-713 while official student/declaration placeholders remain unresolved.",
    "- **Exact next action:** review the merged T-714 hardened Word thesis and provide actual supervisor/reviewer corrections when available. Keep T-712 deferred until such feedback exists. Do not freeze T-713 while official student/declaration placeholders remain unresolved; final Microsoft Word field updates and final-mode placeholder/person-metadata checks remain mandatory before final submission.",
)
replace_once(
    "docs/context/TASKS.md",
    "- [ ] IN_PROGRESS `T-714` — Final pre-supervisor academic/compliance hardening of the accepted T-711 thesis.\n  - Depends on: `T-711` — satisfied.\n  - Scope is editorial/composition only: correct the DQN foundation citation boundary; replace unsupported superiority/significance-style prose with neutral estimated-difference wording; strengthen Related Work only with synchronized verified citation-ready sources; normalize IEEE references from verified metadata; localize captions/headings and terminology; clarify conditional recovery for small recovered n; add figure alt text; scrub generic DOCX metadata; order glossary/references/appendices academically; make frozen method/configuration details self-contained; remove review-production appendix prose; enforce placeholder-aware final mode; and perform fresh full-document Word visual QA.\n  - Review builds may retain only the three explicitly known official-person/declaration placeholders. Final-mode/T-713 must fail on TODO/TBD/[να συμπληρωθεί]/[to be completed]/equivalent residue.\n  - Current implementation branch/PR: `thesis/t711a-final-hardening` / #136. Scientific boundary: no experiment rerun, no new estimand or p-value family, no changed numerical result, no changed right-censoring decision and no changed registered T-613 scientific media bytes.",
    "- [x] `T-714` — Final pre-supervisor academic/compliance hardening of the accepted T-711 thesis. COMPLETE.\n  - Depends on: `T-711` — satisfied.\n  - PR #136 completed the bounded editorial/composition hardening: corrected the DQN citation boundary and unsupported superiority wording; strengthened Related Work with three verified citation-ready sources; normalized 17 references; localized all 24 figure captions; added the RQ3 conditional-recovery warning and 25/25 alt texts; scrubbed generic DOCX metadata; corrected academic front/end-matter ordering; made Appendix A self-contained from the frozen protocol; removed review-production appendix prose; and enforced placeholder-aware final mode.\n  - Pagination hardening removed the front-matter blank page and Chapter 2 orphan page, kept glossary terms with their definitions, and kept the Chapter 4 architecture-flow summary together. Exact PR head `901b53e3fd7a8b84daee37dbbd485f1ff2173c55` passed Repository checks and T-711/T-714 DOCX QA v18. The final review-ready DOCX SHA-256 is `70c897dcda432c3bc3f5b66b3714d701fd895c9ed2e6ce8ff14b19bc46f9ba77`; 84/84 rendered pages are visually covered.\n  - Squash-merged through PR #136 as `42afba20fd5a7e9d3912418d0847b42e566aaca0`. Exactly three official-person/declaration placeholders remain intentionally review-only; final-mode/T-713 must reject them. No experiment, estimand, numerical result, right-censoring decision or registered T-613 scientific media byte changed.",
)

# CURRENT_STATUS.md compact state.
replace_once("docs/context/CURRENT_STATUS.md", "**Date:** 2026-09-03", "**Date:** 2026-09-04")
replace_once(
    "docs/context/CURRENT_STATUS.md",
    "- `T-714` is **IN_PROGRESS** and is the exact current WP7 task: perform the bounded pre-supervisor academic/compliance hardening identified by the final document audits without changing frozen science. This includes citation/wording corrections, natural Greek academic style and terminology normalization, targeted verified related-work strengthening, consistent IEEE reference formatting, Greek captions, RQ3 conditional-recovery warning, accessibility/alt text, DOCX metadata cleanup, front/end-matter order, appendix cleanup/self-containment, placeholder-aware final-mode QA and a fresh full-document render/visual audit.",
    "- `T-714` is **COMPLETE**. PR #136 completed the bounded pre-supervisor academic/compliance hardening and was squash-merged as `42afba20fd5a7e9d3912418d0847b42e566aaca0`. The hardened review artifact contains 17 verified references, all 24 registered scientific figures plus one unnumbered synthesis graphic, 25/25 alt texts and four Word tables of which three are numbered. Exact head `901b53e3fd7a8b84daee37dbbd485f1ff2173c55` passed Repository and DOCX QA; the final DOCX SHA-256 is `70c897dcda432c3bc3f5b66b3714d701fd895c9ed2e6ce8ff14b19bc46f9ba77`, with 84/84 rendered pages covered by visual QA. Exactly three official-person/declaration placeholders remain intentionally unresolved for review mode. Frozen protocol-v2.1 science, T-611/T-612 values and registered T-613 scientific media bytes were unchanged.",
)
replace_once(
    "docs/context/CURRENT_STATUS.md",
    "T-714 may improve reader-facing wording, citations, bibliography formatting, accessibility, document ordering and presentation, but it must not recalculate, reinterpret or selectively replace accepted scientific evidence. New formal literature citations may come only from the synchronized verified citation-ready bibliography layer.",
    "T-714 completed reader-facing wording, citation, bibliography-formatting, accessibility, document-ordering and presentation hardening without recalculating, reinterpreting or selectively replacing accepted scientific evidence. Any later formal literature citation remains restricted to the synchronized verified citation-ready bibliography layer.",
)
replace_once(
    "docs/context/CURRENT_STATUS.md",
    "- `T-713` remains **DEFERRED** until T-714 and any real T-712 cycle are resolved and the final Microsoft Word field/update/placeholder/person-metadata gates pass.",
    "- `T-713` remains **DEFERRED** until any real T-712 feedback cycle is resolved and the final Microsoft Word field/update/placeholder/person-metadata gates pass.",
)
replace_once(
    "docs/context/CURRENT_STATUS.md",
    "Continue `T-714` only on branch `thesis/t711a-final-hardening`: implement the verified document-audit corrections as a bounded composition/editorial layer, update the canonical manuscript where reader-facing source text changes, preserve all frozen scientific identities, run repository/DOCX QA, render the complete resulting Word document and visually inspect every changed/final page before any merge. Do not start T-712 or T-713 and do not rerun or alter the final experiment.",
    "Review the merged T-714 hardened Word thesis and provide actual supervisor/reviewer corrections when available. T-712 remains deferred until real feedback exists; once supplied, incorporate only those corrections and revalidate the document. Do not start T-713 while official student/declaration placeholders remain unresolved, and do not rerun or alter the final experiment.",
)

# PROJECT_CONTEXT.md lifecycle reconciliation.
replace_once(
    "docs/context/PROJECT_CONTEXT.md",
    "6. T-710 evidence-grounded Greek manuscript drafting is complete and merged through PR #132.\n7. `T-711` review-ready Word composition is the next dependency-valid task.\n8. T-712 supervisor/reviewer corrections, T-713 final thesis freeze, defense work, final audits and standalone Windows packaging remain downstream.",
    "6. T-710 evidence-grounded Greek manuscript drafting is complete and merged through PR #132.\n7. T-711 review-ready Word composition and T-714 pre-supervisor academic/compliance hardening are complete; T-714 merged through PR #136 as `42afba20fd5a7e9d3912418d0847b42e566aaca0`.\n8. T-712 remains input-bound on actual supervisor/reviewer corrections; T-713 final thesis freeze, defense work, final audits and standalone Windows packaging remain downstream.",
)
replace_once(
    "docs/context/PROJECT_CONTEXT.md",
    "No green CI, UI screenshot, synthetic smoke, repository cleanup, writing convenience or Word-layout decision authorizes changing frozen scientific evidence or redefining accepted estimands/results. T-711 must compose from the accepted T-710 manuscript, T-611/T-612/T-613 artifacts and synchronized citation-ready bibliography without scientific reinterpretation.",
    "No green CI, UI screenshot, synthetic smoke, repository cleanup, writing convenience or Word-layout decision authorizes changing frozen scientific evidence or redefining accepted estimands/results. T-711/T-714 composition and hardening used the accepted T-710 manuscript, T-611/T-612/T-613 artifacts and synchronized citation-ready bibliography without scientific reinterpretation; any T-712 correction cycle must preserve the same boundary.",
)
