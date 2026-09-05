# Thesis deliverable archive

This directory is the permanent Git-tracked archive of thesis document versions that were surfaced as meaningful review/delivery milestones. GitHub Actions artifacts and local `/mnt/data` files are transient working copies and are not the source of truth.

## Archived milestones

| File | Origin | DOCX SHA-256 | Approx. whole-document words | Role |
|---|---|---|---:|---|
| `T711_run22_review_ready.docx` | T-711 DOCX QA run #22 (`33746548415`) | `32c755d64600d3af9c19a66b9e8d85bfe6a9b61de3c74bba77f581ce1dd007b5` | 19,659 | Initial review-ready T-711 milestone. |
| `T711_run27_results_synthesis.docx` | T-711 DOCX QA run #27 (`33757702212`) | `ee8bcc13191046391654063fba870ed8799bd7c91da77882ed17154b6eaa68b7` | 19,659 | Results-synthesis T-711 milestone. |
| `T714_run66_full_review_ready.docx` | T-714 DOCX QA run #66 (`33853513834`) | `70c897dcda432c3bc3f5b66b3714d701fd895c9ed2e6ce8ff14b19bc46f9ba77` | 20,925 | **Full-content baseline.** Use this as the prose/coverage baseline for the next expanded thesis, while integrating the scientifically corrected T-715 audit material. |
| `T715_run90_pre_audit_reader_scoped.docx` | T-715 DOCX QA run #90 (`33871667506`) | `53bbdc7750e7e1f3bbc545fc6e442e540c4ae63204842fd54db280401b7b8a4d` | ≈11,600 | Reader-scoped pre-audit milestone; preserved because it was surfaced during review. Superseded for scientific wording by run #98. |
| `T715_run98_audit_reconciled_reader_scoped.docx` | T-715 DOCX QA run #98 (`33928822577`) | `e06a466e667359486a86f30c561c42b74b4e209ea28bb8d94c2652c9d36616d1` | ≈12,900 | Audit-reconciled reader-scoped milestone. Scientifically corrected and QA-passing, but **not the final thesis** because the user rejected the excessive compression on 2026-09-05. |
| `T716_stage3_full_content_review_ready.docx` | T-716 stage-3 reconstruction workflow run #1 (`33968319566`) | `364b22543cef75dabcc03a003ad538f8873604e85a234a2d71bdbba1c1f7fe8c` | 25,265 | Full-content reconstruction milestone. Reconstructed from T-714, integrates T-715 corrections and the 601/129 bibliography layer; semantic package SHA-256 `b7e3cfb98dfc7a9d5b8fb6309b7a9be90c7c89eccd77ae14be20bbc7d8e31e8e`; 92/92-page visual QA passed. |
| `T716_stage4_evidence_audited_review_ready.docx` | T-716 stage-4 evidence-audit workflow run #1 (`33969325159`) | `08992272e90b0cae6b457a3f4ce66511cc7c337aeea0b6d3645d632f8d66a7f7` | 25,327 | **Current evidence-audited review milestone.** 31/31 references used; strengthens Watkins/SARSA attribution, Sutton-1990 Dyna precedence, Khetarpal continual-RL authority and bounded safe-continual framing. Semantic package SHA-256 `b01f853af794e596f0dfb491a3f5401365ca3f01fd7d410194e539f0b8a10cc1`; 92-page visual QA passed with 79 pixel-identical pages and manual inspection of all 13 changed pages. |

Each archived DOCX has its corresponding `*_qa-report.json` beside it. The exact hashes were verified before the archive copy was committed.

## Current composition authority

The archived T-716 stage-4 evidence-audited milestone is the accepted T-716 full-content review authority. It inherits the stage-3 restoration/expansion of T-714, preserves all validated T-715 corrections and frozen T-611/T-612/T-613 evidence, and completes the source-attribution/precedence pass without changing experiments, estimands, results or registered media. `docs/thesis/T716_FINAL_ACCEPTANCE_AUDIT.md` records PASS on all 11 completion gates. T-716 is therefore COMPLETE; T-713 final-submission freezing remains downstream.

The T-715 audit corrections remain authoritative for the corrected protocol/scientific wording. In particular, later composition must preserve the two-window RQ3 recovery rule, exact disturbance semantics, 180-unit tuning design and selected configurations, 12-root sizing basis, declared RQ1/RQ2 metric definitions, and the no-post-hoc-analysis boundary recorded in `docs/thesis/T715_AUDIT_RECONCILIATION.md`.

## Retention rule

Do not delete or replace historical milestone files merely because a newer thesis version exists. New review/delivery versions receive a new stable filename and hash. A truly accepted submission candidate belongs under `thesis/final/`; historical or rejected/superseded milestones remain here for provenance and recovery.
