# Bibliography source-selection policy

**Date:** 2026-09-05  
**Scope:** T-716 thesis writing and every later bibliography/citation audit.

## Principle

Source selection is claim-centred. A source is not preferred merely because it is already in the bibliography, is citation-ready, is newer, or was found first. All materially relevant sources for the claim are compared before final wording/citation selection.

## Ranking rule

When sources substantially overlap, use the following precedence:

1. **Scientific fitness for the exact claim.** Prefer the source whose scope, definitions, assumptions, population/environment and methods actually match the statement being written.
2. **Scientific authority and evidence strength.** Prefer primary research, rigorous peer-reviewed work, authoritative monographs/books, strong systematic reviews/meta-analyses and well-supported benchmark/methodology papers over weak secondary summaries, informal material or student work when they address the same claim.
3. **Primary/foundational value.** For the origin of an algorithm, exact equation, theorem, protocol or empirical finding, the primary/foundational source may outrank a newer secondary source even when older.
4. **Methodological depth and reliability.** Prefer transparent methods, adequate experimental/statistical support, reproducibility detail, explicit limitations and stronger evidence over superficial coverage.
5. **Recency among comparably strong sources.** If two or more sources are materially comparable in authority, methodological quality, relevance and depth, prefer the more recent source (for example 2024 over 2021), especially for state-of-the-art, survey, implementation-practice, benchmark and rapidly changing research-context claims.
6. **Current synthesis plus primary provenance where useful.** A recent high-quality survey/review may be preferred for current field framing, while older primary/foundational papers remain cited where the thesis discusses the original method, theorem or finding.
7. **Contradictory and limiting evidence remains visible.** A newer source does not erase credible older counter-evidence, and an older authoritative source is not discarded solely because of age.

## Explicit non-rules

- `newer` does **not** automatically mean `better`;
- citation-ready status means formally eligible, not scientifically superior;
- a student thesis, blog, talk, tutorial or auto-transcript does not outrank a rigorous primary paper or authoritative scholarly book merely because it is newer;
- journal/conference prestige alone does not substitute for relevance and methodological quality;
- one source never becomes a universal source of truth for a multi-source claim;
- project-specific protocol/result facts remain controlled by repository code/protocol/frozen evidence, not by external-source ranking.

## Required decision record for non-obvious choices

When an older source is intentionally preferred over a materially similar newer source, the claim synthesis should record the reason, such as:

- foundational/primary provenance;
- stronger methodological design or evidence;
- substantially greater depth;
- authoritative scholarly reference work;
- closer match to the exact claim;
- newer source is derivative, informal, narrower or scientifically weaker.

Likewise, when a recent review replaces an older review for general field framing, retain any older primary papers still needed for exact original claims.

## Operational use

`docs/thesis/CLAIM_EVIDENCE_TREE.md` is the human claim-level synthesis. `docs/thesis/claim-evidence-map.json` is the machine registry. `scripts/validate_claim_evidence_map.py` validates structural coverage and repository provenance; scientific source ranking remains an explicit evidence-synthesis judgment governed by this policy, because publication year alone cannot safely encode scientific quality.
