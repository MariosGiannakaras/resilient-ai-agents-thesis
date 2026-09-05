#!/usr/bin/env python3
"""Reconcile active documentation after the interrupted T-716 closure.

This script is intentionally idempotent.  It changes documentation/governance only; it
never edits the accepted thesis DOCX, frozen protocol, evidence, analysis, or assets.
"""
from __future__ import annotations

from pathlib import Path

SEMANTIC = "b01f853af794e596f0dfb491a3f5401365ca3f01fd7d410194e539f0b8a10cc1"
BIB = "27674a566ab55e4491b74243fe077a31ef81ae73"


def write(path: str, content: str) -> None:
    p = Path(path)
    content = content.rstrip() + "\n"
    if p.read_text(encoding="utf-8") != content:
        p.write_text(content, encoding="utf-8")


def replace(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if new in text:
        return
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one old or existing new variant; old matches={count}: {old[:120]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


write(
    "docs/context/CODEX_EXECUTION_PROMPT.md",
    f"""# Codex Execution Prompt

## User entrypoint

Give Codex only:

> `/goal Read docs/context/CODEX_EXECUTION_PROMPT.md and execute it completely. Recover actual Git/GitHub/repository state first, resume only dependency-valid unfinished work, preserve frozen evidence, and honor all external-input gates.`

## Startup / resume

1. Inspect Git status, current branch/worktree, recent commits, open PRs, CI and any unmerged branch before modifying anything. Preserve unique partial work.
2. Read exactly the session-start core: `AGENTS.md`, `docs/context/TASKS.md`, `docs/context/CURRENT_STATUS.md`.
3. Treat repository/Git/GitHub/evidence as recovery authority when chat/session memory is stale or truncated.
4. Read further files only for the selected task; use repository search before broad reading.
5. Never reopen completed scientific execution, evidence, analysis or thesis composition merely because an older active document or chat says it is next.

## Current durable state

- T-610 final protocol-v2.1 execution, T-611 evidence freeze, T-612 predeclared analysis and T-613 scientific thesis/defense assets are COMPLETE. Preserve the immutable failed 216-job predecessor and the accepted 603/603 DEC-062 replacement as separate histories.
- The accepted PySide6 **Experiment / Run / Results / Evidence** application is complete through T-537. T-538 is optional/deferred presentation polish and is not a thesis blocker.
- T-700, T-701, T-702, T-710, T-711, T-714, T-715 and **T-716 are COMPLETE**.
- T-716 review authority is `thesis/archive/T716_stage4_evidence_audited_review_ready.docx`, semantic OOXML SHA-256 `{SEMANTIC}`. `docs/thesis/T716_FINAL_ACCEPTANCE_AUDIT.md` records 11/11 PASS.
- The current bibliography consumer authority is immutable upstream SHA `{BIB}` (601 canonical / 129 citation-ready / 19 research-material records / 281 indexed originals).
- T-712 is DEFERRED until actual supervisor/reviewer feedback exists. Internal review is never relabelled as external feedback.
- T-713 is DEFERRED until T-712 is resolved where applicable and authoritative official person/declaration metadata plus final Microsoft Word/submission-format checks are available.
- T-720/T-721/T-722 and T-800/T-801/T-802 remain downstream of the final-thesis freeze. T-803 standalone Windows packaging remains post-thesis under issue #94.

## Execution discipline

Work on one bounded dependency-valid scope at a time. Use targeted checks during implementation and GitHub PR CI as the canonical full-suite pre-merge guard. Preserve unrelated user changes and avoid destructive Git operations.

Scientific and bibliographic boundaries remain fail-closed: do not change frozen protocol choices, roots/seeds, estimands, evidence, result interpretation or registered quantitative assets; do not hand-edit generated bibliography content; do not invent official metadata, feedback, deadlines or defense rules.

Routine branch/PR/CI/objective-review/correction/merge work is autonomous when the repository permits it. Completed work is not re-audited without new evidence except when a continuity/reproducibility defect is itself the active task.

## Stop conditions

If no real supervisor/reviewer feedback or other dependency-valid input exists after T-716, do not manufacture work to advance T-712/T-713. Record the externally gated state and stop. A new task starts only when `TASKS.md` dependencies and any explicit external/authorization gate are satisfied.
""",
)

write(
    "docs/context/IMPLEMENTATION_ROADMAP.md",
    f"""# Implementation Roadmap

`TASKS.md` is the canonical task/dependency/resume ledger and wins on exact status. This roadmap summarizes the accepted lifecycle after the completed T-716 review-ready thesis milestone.

## Completed scientific and application foundation

The project has completed and frozen:

1. bibliography ownership/provenance and immutable generated consumer architecture;
2. Python 3.12 + locked `uv`, project-owned Gymnasium GridWorld, deterministic RNG and evaluator/agent information firewall;
3. five-method protocol-v2.1 comparison: Q-Learning, SARSA, DQN, PPO and Dyna-Q+;
4. fair tuning/sizing, exact method-native continuation, matched FN/FD/AN/AD Phase B and frozen RQ1/RQ2/RQ3 estimands;
5. the failed 216-job T-610 attempt as immutable excluded history and the distinct DEC-062 replacement at 603/603 jobs;
6. T-611 evidence freeze, T-612 predeclared analysis and T-613 deterministic thesis/appendix/defense assets;
7. the accepted PySide6 experiment-first application through T-534/T-535/T-536 and T-537 active-tree cleanup.

The accepted application remains **Experiment / Run / Results / Evidence**. Scientific thresholds, reductions, RNG, checkpoint identity, finalization and result interpretation remain outside Qt presentation state. T-538 is optional/deferred bounded presentation polish, not a scientific or thesis prerequisite.

## Completed thesis path

The writing/review path is also complete through T-716:

- T-700 current official-guidance recheck;
- T-701 review of 22 supplied files / 21 unique example theses for structure/style context only;
- T-702 writing-gate bibliography freshness review;
- T-710 evidence-grounded Greek manuscript;
- T-711 editable Word composition;
- T-714 pre-supervisor academic/compliance hardening;
- T-715 bounded audit/scientific wording reconciliation;
- T-716 restoration/expansion plus final evidence-aware audit.

Accepted T-716 review authority: `thesis/archive/T716_stage4_evidence_audited_review_ready.docx`, semantic SHA-256 `{SEMANTIC}`, 25,327 words, 31/31 governed references, 25/25 scientific media and 92-page visual QA. All 11 final acceptance gates pass.

## Current dependency path

```text
T-716 review-ready thesis — COMPLETE
   └── actual supervisor/reviewer feedback -> T-712 corrections
          └── authoritative official metadata/declaration + final Word/submission checks -> T-713 final thesis freeze
                 ├── T-720 defense narrative/evidence map
                 │      └── T-721 final PowerPoint + speaker material
                 │             └── T-722 rehearsal/defense validation
                 ├── T-800 final bibliography/citation/official-guidance audit
                 ├── T-801 reproducibility/privacy/licensing/consistency audit
                 └── T-802 academic delivery readiness

T-803 standalone Windows package: post-thesis, tracked by issue #94.
```

There is no dependency-valid academic execution task between T-716 completion and receipt of actual T-712 feedback/official finalization inputs. Do not reopen T-716 or fabricate those inputs.

## Completion rule

The project is fully delivered only after the final thesis freeze, defense package, final audits/delivery readiness and post-thesis standalone package are completed under their own gates. Downstream artifacts must remain consistent with frozen T-611/T-612/T-613 science and the accepted T-716/T-713 thesis lineage.
""",
)

write(
    "docs/context/DEFINITION_OF_DONE.md",
    f"""# Definition of Done

Project-level completion conditions only. Concrete task IDs/status/dependencies/resume state live in `docs/context/TASKS.md`.

## Foundation, science, evidence and application

- [x] Official thesis identity, bibliography ownership/provenance, Python 3.12 + locked environment and reproducible repository workflow are established.
- [x] Project-owned GridWorld, deterministic separated RNG and evaluator/agent information boundary are validated.
- [x] Protocol-v2.1 five-method design, fair tuning/sizing, final roots/layouts/budgets and RQ1/RQ2/RQ3 estimands are frozen.
- [x] Exact Phase-A continuation and matched FN/FD/AN/AD Phase-B execution/evidence contracts are implemented.
- [x] The original 216-job T-610 attempt is preserved as excluded failed/incomplete history; the DEC-062 replacement completed 603/603 jobs.
- [x] T-611 final evidence is validated/frozen, T-612 predeclared analysis is finalized and T-613 quantitative thesis/defense assets are reproducible and provenance-registered.
- [x] The accepted PySide6 **Experiment / Run / Results / Evidence** application is complete through T-537 with stored-evidence-only scientific presentation and a preserved final-execution firewall.
- [x] Required UI workflow/render/CI acceptance for the completed application has passed. Optional T-538 presentation polish remains deferred and non-blocking.
- [ ] T-803 post-thesis standalone Windows package is produced and validated on the intended Windows environment.

## Thesis writing and review

- [x] Explicit pre-WP7 approval was received.
- [x] T-700 current official-guidance recheck and T-701 example-thesis structure/style review are complete.
- [x] T-702 writing-gate bibliography freshness review and immutable synchronization are complete; later governed T-716 source additions are synchronized in consumer snapshot `{BIB}`.
- [x] T-710 evidence-grounded Greek manuscript is complete.
- [x] T-711 editable Word composition and T-714 academic/compliance hardening are complete.
- [x] T-715 scientific wording/audit reconciliation is preserved as a bounded completed milestone.
- [x] T-716 full-content restoration/expansion and evidence-aware final review pass all 11 acceptance gates. Accepted review semantic SHA-256: `{SEMANTIC}`.
- [x] The accepted T-716 DOCX contains only the three deliberate official-data placeholders; no fabricated official metadata was introduced.
- [ ] T-712 actual supervisor/reviewer feedback is incorporated and affected evidence/citations are revalidated.
- [ ] T-713 final Word/submission candidate is frozen with authoritative metadata/declaration text, updated fields/cross-references/TOC/lists, final PDF where required and exact artifact identities.

## Defense and final academic delivery

- [ ] T-720 rechecks current defense rules and freezes the defense narrative/evidence map from the final thesis.
- [ ] T-721 produces the final PowerPoint and speaker material without new estimands or unsupported claims.
- [ ] T-722 validates rendering/media/demo fallback and rehearses to the verified official duration.
- [ ] T-800 final bibliography/citation/official-guidance audit passes.
- [ ] T-801 reproducibility/privacy/licensing/thesis/defense/application consistency audit passes.
- [ ] T-802 academic delivery readiness verifies the exact required file/form/deposit package and records submitted artifact identities.

No unchecked downstream item may be marked complete by inference. External feedback, official metadata, deadlines and defense rules are never invented.
""",
)

write(
    "docs/context/EXECUTION_WORKFLOW.md",
    f"""# Execution and Review Workflow

## Operating model

The user supplies goals, genuinely subjective academic choices, actual supervisor/Department feedback and private/official material when required. Repository automation owns routine Git/CI/task bookkeeping, reproducible technical evidence and objective validation. ChatGPT may perform Greek thesis/review/defense narrative work when the relevant task gate is open.

Normal flow:

> recover actual repository/GitHub state -> select one dependency-valid bounded scope -> implement -> targeted checks -> PR CI/objective review -> corrections -> durable reconciliation -> merge -> next allowed scope

## Session continuation

Every coding/repository session starts from `AGENTS.md`, `docs/context/TASKS.md` and `docs/context/CURRENT_STATUS.md`, after inspecting Git status/branch/recent commits/open PRs/CI. Repository evidence wins over stale chat memory. Never discard unique branch or uncommitted work without inspection.

## Validation discipline

Use the smallest deterministic checks that protect the changed boundary during implementation; GitHub PR CI is the canonical complete repository guard. Do not turn scientific matrices into CI tests or create arbitrary coverage/fuzzing projects. Required scientific/provenance/configuration state fails closed.

## Scientific authority and completed evidence chain

Protocol-v2.1 under DEC-058/DEC-060 remains frozen. Q-Learning, SARSA, DQN, PPO and Dyna-Q+ use the accepted common actual-interaction fairness contract, method-native continuation and matched FN/FD/AN/AD Phase B. RQ3 uses passive 32-interaction windows, tolerance 0.10, two-window stability and explicit right-censoring.

T-610 through T-613 are complete. Preserve the failed 216-job predecessor and accepted 603/603 DEC-062 replacement as distinct immutable histories; only T-611 frozen replacement evidence feeds T-612, and only registered T-612 outputs feed T-613. No downstream task may recompute or reinterpret frozen science outside its declared authority.

## Accepted application state

DEC-059/DEC-061 control the accepted PySide6 application. The clean experiment-first rebuild and subsequent hardening are complete through T-537. Primary surfaces are **Experiment / Run / Results / Evidence**. The UI presents validated stored evidence and cannot own scientific RNG, roots, checkpoint identity, reductions, recovery decisions, intervals, finalization or authorization.

T-538 is optional/deferred bounded presentation polish. T-803 standalone Windows packaging is post-thesis and is not a current academic blocker.

## Bibliography flow

All source discovery/originals/OCR/conversion/scientific analysis and promotion belong to `MariosGiannakaras/ThesisBibliography`. This repository consumes immutable generated snapshots read-only. The current T-716 consumer authority is `{BIB}`; formal citations resolve through `research/bibliography/citation-ready/`. Later freshness work is governed by T-800, not ad-hoc local edits.

## Thesis state and next gate

T-700/T-701/T-702/T-710/T-711/T-714/T-715/T-716 are complete. The accepted T-716 review authority is `thesis/archive/T716_stage4_evidence_audited_review_ready.docx`, semantic SHA-256 `{SEMANTIC}`, with 11/11 final acceptance gates passing.

The next academic task is **T-712 only when actual supervisor/reviewer feedback exists**. Until then, do not reopen T-716 or manufacture feedback. T-713 remains blocked by T-712 where applicable plus authoritative official metadata/declaration and final Microsoft Word/submission checks.

After T-713, follow the canonical sequence T-720 -> T-721 -> T-722 and T-800/T-801/T-802; T-803 remains post-thesis.

## Tool/ownership handoff

- Repository/Codex: reproducible evidence, technical validation, source/citation/result consistency, Git/CI and traceable assets.
- ChatGPT: Greek academic revision/narrative, defense storyline, slide copy and speaker material when their gates are open.
- Microsoft Word: final editable thesis inspection/field updates/freeze.
- PowerPoint: final defense presentation inspection/rehearsal.
- User: real supervisor/private/official inputs, selected manual app media where requested and final subjective academic sign-off.

Quantitative thesis/presentation assets derive from frozen repository evidence, never from manually retyped UI values.
""",
)

write(
    "docs/thesis/WP7_WP8_TOOL_WORKFLOW.md",
    f"""# WP7 / WP8 Thesis, Defense, and Delivery Tool Workflow

**Status:** T-716 review-ready composition COMPLETE. `docs/context/TASKS.md` is the only canonical task/dependency ledger.

**Current next academic task:** T-712 only when actual supervisor/reviewer feedback is received. T-713 remains blocked by T-712 where applicable plus authoritative official metadata/declaration and final Word/submission checks.

## Authority hierarchy

1. T-611/T-612/T-613 accepted evidence for experimental/result claims.
2. Synchronized citation-ready `ThesisBibliography` evidence for formal external claims; current consumer snapshot `{BIB}`.
3. Accepted repository decisions/configs/code for exact methodology/implementation claims.
4. Current verified Department/University guidance for structure/format/submission/defense rules.
5. Actual supervisor/reviewer instructions when supplied.
6. T-701 example-thesis-derived structure/style guidance as context only.
7. Accepted T-716 Word thesis for review/revision, subordinate to the authorities above.

Chat memory and example theses are never sufficient scientific authority.

## Completed WP7 path

- **T-700 COMPLETE:** dated official guidance recheck; no verified ICE-specific defense duration/slide-count/template/live-demo rule was found, so these remain future T-720/T-722 recheck items.
- **T-701 COMPLETE:** reviewed 22 supplied files representing 21 unique theses for structure/style context only; established the seven-chapter architecture and separate Results/Discussion.
- **T-702 COMPLETE:** completed the 2026-09-03 writing-gate freshness review. Its historical snapshot was `ada0d1aec7511098fd12610ae9e5abe7aea875cd` (599/123). Subsequent governed T-716 source work was synchronized normally; current consumer authority is `{BIB}` at 601 canonical / 129 citation-ready / 19 research-material records / 281 indexed originals.
- **T-710 COMPLETE:** evidence-grounded Greek manuscript and handoff package.
- **T-711 COMPLETE:** real editable Word composition with governed IEEE numeric citations, registered figures/tables and structural/render QA.
- **T-714 COMPLETE:** bounded academic/compliance hardening and front/end-matter/Word QA.
- **T-715 COMPLETE:** bounded reader/audit reconciliation; its compressed DOCX is historical, not the final composition baseline.
- **T-716 COMPLETE:** restored/expanded full-content thesis plus final evidence-aware audit. Accepted review authority is `thesis/archive/T716_stage4_evidence_audited_review_ready.docx`, semantic SHA-256 `{SEMANTIC}`, 25,327 words, 31/31 governed references, 25/25 preserved scientific media and 92-page visual QA. `docs/thesis/T716_FINAL_ACCEPTANCE_AUDIT.md` records 11/11 PASS.

The three remaining front-matter placeholders are deliberate because authoritative official data have not been supplied. They belong to T-713 and must not be invented.

## T-712 — actual supervisor/reviewer correction cycle

Start only from real feedback. For each request preserve a correction ledger containing the request, affected section, disposition/rationale, evidence/citation impact and resulting artifact identity. Revalidate affected claims, references, frozen values and rendered pages. Internal self-review is not T-712 feedback.

## T-713 — final thesis freeze

Inputs: accepted T-716/T-712 content, authoritative official person/institution/declaration text and final Microsoft Word/submission requirements. Update TOC/list/caption/cross-reference/page fields in Word, verify final references/captions/page numbering, produce the required PDF/deposit copy, run final-mode checks that reject placeholders and record exact Word/PDF identities under `thesis/final/`.

## T-720/T-721/T-722 — defense

Recheck current ICE/UNIWA defense rules first. Build the defense narrative strictly from the final thesis and frozen evidence; create a slide-level evidence map; then produce the final `.pptx`, embedded notes and separate Greek spoken script. Quantitative claims use frozen T-613/T-612-derived assets, not screenshots. Validate PowerPoint rendering, timing, media and static/demo fallback before freeze.

## T-800/T-801/T-802 — final audits and delivery

Recheck final bibliography/citations and official guidance; audit reproducibility/privacy/licensing and cross-artifact consistency; then assemble/verify the exact academic delivery package and record submitted artifact identities.

## T-803 — standalone Windows package

Only after the academic deliverable is stable, package the accepted PySide6 application for Windows and validate launch/close/restart/writable paths/privacy/licensing on the intended environment. This is tracked separately under issue #94.

## Manual application media rule

When a thesis/defense screenshot, GIF or video is actually needed, create an `ASSET-APP-*` instruction with exact application state, visible/hide requirements, purpose/placement, provenance and static fallback. Application media illustrate implementation/workflow; they never replace frozen quantitative evidence.
""",
)

write(
    "docs/thesis/PRESENTATION_WORKFLOW.md",
    f"""# Thesis Defense Presentation Workflow

**Status:** Deferred active specification. Do not build the final deck before T-713 final-thesis freeze and T-720's current defense-guidance/evidence-map gate. The pre-WP7 approval gate is already satisfied and T-716 is complete.

## Purpose

Produce an evidence-consistent PowerPoint defense package from the frozen final thesis, accepted protocol-v2.1 evidence/analysis/assets and validated application illustrations. The deck is not an independent scientific source.

## Inputs before final deck generation

- T-713 final Word/PDF thesis identity;
- current verified ICE/UNIWA defense duration/language/file/template/live-demo rules;
- T-611 frozen protocol-v2.1 evidence and T-612 final statistical interpretation;
- T-613 registered figures/tables/exports and any later verified final-thesis assets;
- slide-level claim/result/source evidence map from T-720;
- validated application screenshots/demo path only where useful, each with `ASSET-APP-*` provenance and static fallback.

## Narrative scope

The deck should defend the work rather than reproduce chapters. It normally covers:

- problem, motivation, research questions and bounded contribution;
- only the related-work concepts needed to understand the comparison;
- controlled GridWorld/uncertainty design and information/fairness boundaries;
- retained methods: Q-Learning, SARSA, DQN, PPO and Dyna-Q+;
- Phase-A nominal learning and matched Phase-B FN/FD/AN/AD Frozen-versus-Adaptive regimes;
- RQ1 nominal learning, RQ2 matched adaptation benefit/losses and RQ3 temporal recovery/right-censoring;
- principal frozen results with uncertainty and denominators;
- limitations/threats to validity and direct conclusions;
- architecture/application workflow only where it helps explain reproducibility or demonstration;
- concise future work where justified.

No slide may introduce a new estimand, post-hoc ranking, p-value superiority family or uncited factual claim.

## Tool split

- **Repository/Codex:** evidence map, frozen figures/tables, exact technical diagrams, app-media provenance and mechanical consistency checks.
- **ChatGPT:** defense narrative, concise Greek slide copy, transitions, embedded speaker notes, separate spoken Greek script and likely-question preparation.
- **Microsoft PowerPoint:** authoritative final `.pptx` inspection, Presenter View, media/animation/font/layout validation and rehearsal.
- **Canva:** optional bounded visual polish only; any exported PPTX must be revalidated in PowerPoint and Canva never becomes a data/citation source.

## Application screenshots / GIF / video

Animated/live media is supplemental. Every manual capture must state exact page/state/context, crop/hide requirements, slide purpose, caption/evidence identity and static fallback. No essential scientific conclusion may depend on live software or animation. Quantitative claims use repository-generated evidence assets.

## Speaker material

Produce both embedded PowerPoint speaker notes and a separate complete natural Greek spoken script synchronized to slide numbers/headings. Final length follows the verified official duration and rehearsal, not an invented slide-count rule.

## Validation gates

Before T-722 completion:

- every numerical/result claim matches frozen T-612/T-613 evidence and the final thesis;
- literature claims resolve through the final governed bibliography;
- method/condition/protocol terminology matches protocol-v2.1 and the final thesis;
- right-censored recovery remains explicit and horizon 256 is never presented as an observed recovery time;
- app media are authentic or explicitly labelled non-scientific illustrations;
- notes/script match final slide order;
- PPTX opens correctly in PowerPoint with readable layouts/fonts/tables/graphs and working media;
- no essential slide requires internet/cloud/live demo;
- tested static fallback exists for any live/animated element;
- rehearsal fits the verified official duration with safety margin.
""",
)

write(
    "docs/context/PROJECT_CONTEXT.md",
    f"""# Project Context

## Project identity

Official titles:

- Greek: **Σύγκριση και Αξιολόγηση Ανθεκτικών Πρακτόρων Τεχνητής Νοημοσύνης σε Περιβάλλοντα με Αβεβαιότητα**
- English: **Comparison and Evaluation of Resilient AI Agents in Uncertain Environments**

GridWorld is the controlled experimental testbed/visualization environment, not the thesis subject. The thesis main language is Greek; Microsoft Word remains the editable academic delivery format unless authoritative guidance changes it.

## Bibliography boundary and current authority

`MariosGiannakaras/ThesisBibliography` owns discovery, originals/OCR/conversion, scientific source analysis/evidence and promotion. This repository consumes immutable generated output read-only.

The current T-716 consumer authority is upstream SHA `{BIB}`, synchronized and validated at 601 canonical sources, 129 citation-ready sources, 19 research materials and 281 indexed originals. Earlier `ada0d1aec7511098fd12610ae9e5abe7aea875cd` (T-702 / 599/123) and older integration labels remain historical provenance only. Formal thesis citations resolve through `research/bibliography/citation-ready/`; generated bibliography content is never hand-edited locally.

## Frozen scientific authority

Historical protocol-v1.x and the first failed/incomplete T-610 attempt remain immutable history. DEC-058 is the historical protocol-v2.0 freeze; DEC-060 plus `configs/protocols/protocol-v2.1-final.json` define the accepted protocol-v2.1 amendment.

The final comparison uses Q-Learning, SARSA, DQN, PPO and Dyna-Q+ under common actual-environment-interaction fairness, method-native continuation and matched FN/FD/AN/AD Phase B. Twelve independent roots, two held-out layouts, four Phase-B conditions and a 256-interaction horizon are fixed. RQ2 adaptation benefit is `(FN-FD)-(AN-AD)`. RQ3 uses passive 32-interaction windows, primary directed tolerance 0.10, two consecutive qualifying windows and explicit right-censoring with `recovery_time=null`.

The DEC-062 replacement completed 603/603 jobs. T-611 froze only that replacement; T-612 finalized the predeclared analysis; T-613 generated the registered thesis/appendix/defense asset package. No downstream writing/presentation task may redefine those estimands or silently recompute final science.

## Accepted application

The current application is native PySide6 / Qt 6 Widgets under DEC-059/DEC-061 with primary surfaces **Experiment / Run / Results / Evidence**. The rebuild/hardening is complete through T-537. The UI is control/observation/presentation only; scientific RNG, checkpoint identity, root reduction, recovery decisions, intervals, evidence finalization and final authorization remain backend/evidence authority.

T-538 is optional deferred presentation polish. Final standalone Windows packaging remains post-thesis under T-803/issue #94.

## Thesis composition state

T-700, T-701, T-702, T-710, T-711, T-714, T-715 and **T-716 are COMPLETE**. The accepted T-716 review authority is `thesis/archive/T716_stage4_evidence_audited_review_ready.docx` with 25,327 whole-document words, 23,273 main-body words to bibliography, 766 paragraphs, 31/31 governed references used, 25/25 scientific media preserved and 92-page visual QA. Semantic OOXML package SHA-256: `{SEMANTIC}`. `docs/thesis/T716_FINAL_ACCEPTANCE_AUDIT.md` records 11/11 PASS.

Three front-matter placeholders remain deliberately because authoritative official student/declaration data have not been supplied. They are T-713 inputs, not unfinished T-716 drafting residue.

## Current lifecycle

1. Science/application/final evidence/analysis/assets — COMPLETE.
2. Review-ready full-content thesis through T-716 — COMPLETE.
3. T-712 — DEFERRED until actual supervisor/reviewer feedback arrives.
4. T-713 — DEFERRED until T-712 is resolved where applicable plus authoritative official metadata/declaration and final Word/submission checks.
5. T-720/T-721/T-722 — downstream defense work after final thesis freeze.
6. T-800/T-801/T-802 — downstream final audits/delivery readiness.
7. T-803 — post-thesis standalone Windows package.

`TASKS.md` and `CURRENT_STATUS.md` are the canonical concrete resume state. No stale chat, historical branch or older workflow document may reopen completed tasks without new evidence or an explicit dependency-valid instruction.
""",
)

write(
    "docs/context/OPEN_QUESTIONS.md",
    """# Open Questions

This file contains only genuinely unresolved items after current repository evidence and accepted decisions. Concrete status/dependencies are in `TASKS.md`; `CURRENT_STATUS.md` is the compact current state.

## Resolved and no longer open

Scientific method/protocol design, final execution/recovery, T-611 evidence freeze, T-612 analysis, T-613 assets, PySide6 application architecture/acceptance, pre-WP7 approval, T-700/T-701/T-702, T-710/T-711/T-714/T-715 and T-716 review-ready thesis composition are complete. Historical v1.x and failed-attempt evidence remain auditable history rather than open design questions.

## Current open questions

| ID | Open issue | Needed by | Blocks now? | Resolver / safe rule |
|---|---|---|---|---|
| OQ-ACA-001 | What actual supervisor/reviewer corrections, if any, will be requested? | T-712 | Yes for starting T-712; no work may be invented meanwhile. | Receive real feedback and record it explicitly. |
| OQ-ACA-002 | What is the verified submission/defense schedule? | Delivery/rehearsal | No current task. | User/Department; never invent dates. |
| OQ-ACA-003 | What exact current official Word template/submission package, person metadata and declaration wording apply? | T-713 | Yes when T-713 starts. | Recheck official sources and use authoritative supplied data only. |
| OQ-ACA-004 | What are the exact current defense duration/language/file/template/live-demo rules? | T-720/T-722 | No current task. | Recheck ICE/UNIWA guidance near defense; do not borrow another department's rules. |
| OQ-PKG-001 | What exact post-thesis standalone Windows packaging recipe is finally delivered? | T-803 / issue #94 | No. | Resolve after academic deliverable stability and validate on the intended Windows machine. |
| OQ-AI-001 | Is any optional AI feature useful inside the application? | Optional future UI only | No. | Do not integrate without a concrete measurable benefit. |
| OQ-PRIV-001 | Are additional privacy/licensing/copyright changes required before deliberate wider distribution? | T-801/T-803 | No current task. | Run final audit before release/distribution. |

## Current authority

T-716 is complete. The next academic action is T-712 only when actual supervisor/reviewer feedback exists; T-713 remains downstream of real feedback where applicable plus authoritative official metadata/declaration and final Word/submission checks. Until those inputs arrive, preserve the accepted T-716 milestone rather than manufacturing progress.
""",
)

# Targeted reconciliation for current decision/constraint/architecture records.
replace(
    "docs/context/USER_DECISIONS.md",
    "- Research/protocol/application/evidence remain the current priority. Thesis Results/Discussion writing remains blocked until the explicit later approval gate.",
    "- Research/protocol/application/final evidence and review-ready thesis composition through T-716 are complete. The next academic change is T-712 only from actual supervisor/reviewer feedback; T-713 remains the later official final-submission freeze."
)
replace(
    "docs/context/USER_DECISIONS.md",
    "## Clean UI restart — current explicit direction",
    "## Clean UI restart — completed historical direction"
)
replace(
    "docs/context/USER_DECISIONS.md",
    "- The previously paused UI implementation is considered incomplete/non-authoritative for continuation.",
    "- This direction was executed by the accepted T-534/T-535/T-536 rebuild and T-537 cleanup; the previously paused UI implementation remains non-authoritative history."
)
replace(
    "docs/context/USER_DECISIONS.md",
    "- The compressed T-715 reader-scoped DOCX is not the final thesis. Restore the fuller T-714-level academic coverage and integrate the validated T-715 scientific corrections; do not trade scientific/academic completeness for simplification and do not add filler merely to raise word count.",
    f"- The compressed T-715 reader-scoped DOCX is historical, not the final review authority. T-716 restored/expanded full content, retained validated T-715 corrections and is accepted at semantic SHA-256 `{SEMANTIC}`; do not regress to the compressed version without new evidence/feedback."
)
replace(
    "docs/context/USER_DECISIONS.md",
    "- Supervisor-specific corrections will be recorded only when actually received.",
    "- T-716 review-ready composition is complete; supervisor-specific T-712 corrections will be recorded only when actually received."
)

replace(
    "docs/context/CONSTRAINTS.md",
    "- DEC-060 and `configs/protocols/protocol-v2.1-final.json` are the current pre-execution scientific authority.",
    "- DEC-060 and `configs/protocols/protocol-v2.1-final.json` are the accepted protocol-v2.1 scientific authority; final execution/evidence/analysis are already frozen through T-610/T-611/T-612."
)
replace(
    "docs/context/CONSTRAINTS.md",
    "- The current UI restart must begin from fresh `main` and may replace the presentation layer from scratch. Existing pre-restart widgets/layouts/styles/screenshots are reference/history only, not design authority.",
    "- The clean PySide6 UI restart is complete through T-537. Pre-restart widgets/layouts/styles/screenshots remain reference/history only; current presentation authority is the accepted Experiment / Run / Results / Evidence implementation."
)
replace(
    "docs/context/CONSTRAINTS.md",
    "- Thesis/presentation writing remains blocked until the evidence and explicit pre-WP7 approval gates are satisfied.",
    "- The evidence and pre-WP7 approval gates are satisfied and T-716 review-ready composition is complete. Further thesis revision is gated on real T-712 feedback; T-713/T-720+ retain their official-input/finalization gates."
)

replace(
    "docs/context/BIBLIOGRAPHY_INTEGRATION.md",
    "The current major-writing-gate synchronized baseline is full upstream SHA `ada0d1aec7511098fd12610ae9e5abe7aea875cd`, accepted through T-702 and thesis PR #130. Older immutable refs remain historical snapshots and are never moved.",
    f"The current T-716 synchronized consumer baseline is full upstream SHA `{BIB}`, accepted after governed source promotion/re-sync. The T-702 SHA `ada0d1aec7511098fd12610ae9e5abe7aea875cd` and older immutable refs remain historical snapshots and are never moved."
)
replace(
    "docs/context/BIBLIOGRAPHY_INTEGRATION.md",
    "Current T-702 acceptance facts are 599 canonical sources, 123 citation-ready sources, 19 research materials, 281 indexed original PDFs, 1,634 integrity-covered corpus files, and upstream schema version 1. The accepted checkout is `ada0d1aec7511098fd12610ae9e5abe7aea875cd`; the complete-corpus source commit is `c999dbe272baa081d3666254655aeeec17549c1f`; the citation-ready source commit is `84d62ec3eb18e1d3565625bc02c289131282ea27`. Trust-aware consumer validation reports 40 thesis references: 38 citation-ready and 2 research-material. These values describe this immutable baseline only; synchronization logic reads and validates metadata dynamically for every later immutable ref. Earlier v2/v3 acceptance facts remain historical and are preserved in their decision/history records rather than treated as current state.",
    f"Current T-716 consumer facts are 601 canonical sources, 129 citation-ready sources, 19 research materials and 281 indexed originals at immutable checkout `{BIB}`. The T-702 checkout `ada0d1aec7511098fd12610ae9e5abe7aea875cd` (599 canonical / 123 citation-ready) remains historical writing-gate provenance. Synchronization logic reads and validates package metadata dynamically for every immutable ref; earlier acceptance counts/commits remain historical records rather than current state."
)

replace(
    "docs/thesis/CLAIM_EVIDENCE_TREE.md",
    "**Status:** living pre-writing authority  ",
    "**Status:** accepted T-716 claim/evidence authority; reopen only for governed later revision  "
)
replace(
    "docs/thesis/THESIS_STRUCTURE_DRAFT.md",
    "**Status:** Structure-only preparation. Chapter/section headings are aligned with DEC-060 RQ1/RQ2/RQ3, but WP7 writing remains BLOCKED until final evidence is accepted and the explicit pre-WP7 gate is approved. No result, discussion or conclusion content may be inferred from this outline. The structure must still be checked against current University/Department rules and any later supervisor/template guidance before final writing.",
    "**Status:** HISTORICAL/SUPERSEDED structure-only preparation. WP7/T-716 composition is complete; current thesis structure authority is `THESIS_STRUCTURE_AND_STYLE_GUIDE.md` plus the accepted T-716 DOCX. This outline remains only as pre-writing history and must not be used to reopen completed chapter architecture."
)
replace(
    "docs/context/CONTRADICTIONS.md",
    "| CON-028 | The paused/pre-v2.1 UI implementation should simply be continued. | Restart the UI from current `main`; re-read v2.1 contracts and rebuild presentation from today's state. Existing presentation code/screenshots are replaceable reference, not authority. | Latest explicit user direction. | No. |",
    "| CON-028 | The paused/pre-v2.1 UI implementation should simply be continued. | The clean restart was executed and accepted through T-534/T-535/T-536/T-537; the current PySide6 Experiment / Run / Results / Evidence application is authority. | Superseded and completed. | No. |"
)

# Add one durable changelog entry, once.
changelog = Path("docs/context/CHANGELOG_CONTEXT.md")
text = changelog.read_text(encoding="utf-8")
marker = "## 2026-09-05 — T-716 final acceptance and continuity reconciliation"
if marker not in text:
    anchor = "# Context Changelog\n\nRecord only material changes to the project source of truth. Detailed commit-by-commit history remains in Git; accepted decisions remain indexed in `docs/decisions/DECISION_LOG.md`.\n\n"
    if not text.startswith(anchor):
        raise RuntimeError("CHANGELOG_CONTEXT.md header changed unexpectedly")
    entry = f"""{marker}\n\n- Completed T-716 full-content restoration/expansion and evidence-aware review; `docs/thesis/T716_FINAL_ACCEPTANCE_AUDIT.md` records 11/11 PASS for the archived stage-4 review DOCX, semantic SHA-256 `{SEMANTIC}`.\n- Preserved frozen T-611/T-612/T-613 science/media and governed 31/31 formal references; no experiment, estimand, result or registered quantitative asset was changed.\n- Recovered the interrupted-session state: the final-acceptance branch had completed CI but had not yet been integrated. Reconciled stale active bootstrap/roadmap/workflow documents so future sessions cannot restart T-613, the UI rebuild, T-711 or the pre-WP7 gate.\n- Current academic gate is T-712 only on actual supervisor/reviewer feedback; T-713 remains downstream of real feedback where applicable plus authoritative official metadata/declaration and final Word/submission checks.\n\n"""
    changelog.write_text(anchor + entry + text[len(anchor):], encoding="utf-8")

print("T-716 continuity reconciliation complete")
