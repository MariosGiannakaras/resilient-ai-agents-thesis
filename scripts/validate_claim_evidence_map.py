#!/usr/bin/env python3
"""Validate the T-716 claim-centred evidence registry.

This validator protects five boundaries:
1. formal source IDs must exist in the synchronized citation-ready corpus;
2. context/informal IDs must exist in the synchronized canonical corpus;
3. literature claims should have >=2 formal sources unless an explicit exception exists;
4. protocol/project/result claims must include repository authorities;
5. the source-selection policy must explicitly preserve scientific quality over blind recency.

It validates provenance/coverage structure; it does not judge scientific truth or replace
human comparison of the cited analyses/evidence.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "docs/thesis/claim-evidence-map.json"
SOURCE_POLICY = ROOT / "docs/thesis/BIBLIOGRAPHY_SOURCE_SELECTION_POLICY.md"
BIB = ROOT / "research/bibliography"
READY = BIB / "citation-ready"
READY_CATALOG = READY / "catalog/sources.csv"
CANONICAL_CATALOG = BIB / "catalog/sources.csv"
SRC_RE = re.compile(r"^SRC-[0-9A-F]{10}$")
CLAIM_RE = re.compile(r"^(?:LIT|PROJ|RES|DISC|FUT)-[0-9]{3}$")


def ids_from_csv(path: Path) -> set[str]:
    if not path.is_file():
        raise SystemExit(f"missing required bibliography catalog: {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        return set()
    key = "Κωδικός" if "Κωδικός" in rows[0] else "source_id"
    return {r.get(key, "").strip() for r in rows if r.get(key, "").strip()}


def main() -> int:
    if not MAP.is_file():
        print(f"ERROR missing map: {MAP.relative_to(ROOT)}", file=sys.stderr)
        return 2
    if not SOURCE_POLICY.is_file():
        print(f"ERROR missing source-selection policy: {SOURCE_POLICY.relative_to(ROOT)}", file=sys.stderr)
        return 2

    policy_text = SOURCE_POLICY.read_text(encoding="utf-8")
    policy_required = (
        "Scientific fitness for the exact claim",
        "Scientific authority and evidence strength",
        "Primary/foundational value",
        "Methodological depth and reliability",
        "Recency among comparably strong sources",
        "newer` does **not** automatically mean `better",
        "Contradictory and limiting evidence remains visible",
    )

    data = json.loads(MAP.read_text(encoding="utf-8"))
    claims = data.get("claims")
    if not isinstance(claims, list) or not claims:
        print("ERROR claim list is empty", file=sys.stderr)
        return 2

    ready_ids = ids_from_csv(READY_CATALOG)
    canonical_ids = ids_from_csv(CANONICAL_CATALOG)
    errors: list[str] = []
    seen_claims: set[str] = set()
    used_formal: set[str] = set()
    used_context: set[str] = set()
    used_informal: set[str] = set()

    for marker in policy_required:
        if marker not in policy_text:
            errors.append(f"source-selection policy missing required rule: {marker}")

    for claim in claims:
        cid = str(claim.get("id", ""))
        ctype = str(claim.get("type", ""))
        statement = str(claim.get("claim", "")).strip()
        formal = claim.get("formal_sources", []) or []
        context = claim.get("context_sources", []) or []
        informal = claim.get("informal_sources", []) or []
        authorities = claim.get("project_authorities", []) or []
        exception = str(claim.get("single_source_exception_reason", "")).strip()

        if not CLAIM_RE.fullmatch(cid):
            errors.append(f"{cid or '<missing>'}: invalid claim ID")
        if cid in seen_claims:
            errors.append(f"{cid}: duplicate claim ID")
        seen_claims.add(cid)
        if ctype not in {"literature", "protocol", "project", "result"}:
            errors.append(f"{cid}: invalid type {ctype!r}")
        if len(statement) < 20:
            errors.append(f"{cid}: missing/substantively empty claim statement")
        if not str(claim.get("synthesis", "")).strip():
            errors.append(f"{cid}: missing synthesis")
        if not str(claim.get("limits", "")).strip():
            errors.append(f"{cid}: missing limits")

        for sid in formal:
            if not SRC_RE.fullmatch(sid):
                errors.append(f"{cid}: malformed formal source ID {sid!r}")
            elif sid not in ready_ids:
                errors.append(f"{cid}: formal source is not citation-ready: {sid}")
            used_formal.add(sid)

        for sid in context:
            if not SRC_RE.fullmatch(sid) or sid not in canonical_ids:
                errors.append(f"{cid}: unknown context source: {sid}")
            if sid in ready_ids:
                errors.append(f"{cid}: {sid} is citation-ready and should be classified formal, not context-only")
            used_context.add(sid)

        for sid in informal:
            if not SRC_RE.fullmatch(sid) or sid not in canonical_ids:
                errors.append(f"{cid}: unknown informal source: {sid}")
            used_informal.add(sid)

        if ctype == "literature" and len(set(formal)) < 2 and not exception:
            errors.append(f"{cid}: literature claim has fewer than 2 independent formal sources without exception")
        if ctype in {"protocol", "project", "result"} and not authorities:
            errors.append(f"{cid}: {ctype} claim has no repository authority")
        for rel in authorities:
            p = ROOT / rel
            if not p.exists():
                errors.append(f"{cid}: missing project authority path: {rel}")

    if not used_formal:
        errors.append("no formal source usage registered")

    if errors:
        print("Claim-evidence validation FAILED:", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1

    print(
        "Claim-evidence validation PASS: "
        f"claims={len(claims)}, formal_sources={len(used_formal)}, "
        f"context_sources={len(used_context)}, informal_sources={len(used_informal)}, "
        "source_selection_policy=quality-first-recency-aware"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
