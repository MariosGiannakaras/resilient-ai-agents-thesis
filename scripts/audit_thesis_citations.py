#!/usr/bin/env python3
"""Audit true bibliography-number usage in retained thesis DOCX files.

The DOCX corpus analyzer intentionally counts any bracketed number as a potential
citation. This script narrows the count by using the detected bibliography list
and only accepts bracketed numbers/ranges that resolve to an existing reference
number. It reports chapter-level density and uncited bibliography entries.
"""
from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

from audit_thesis_docx_corpus import ROOT, audit_docx, normalize, words

CIT_GROUP_RE = re.compile(r"\[(\d+(?:\s*(?:,|-|–)\s*\d+)*)\]")
REF_NUM_RE = re.compile(r"^\[(\d+)\]\s+")
CHAPTER_RE = re.compile(r"Κεφάλαιο\s+([1-7])", re.IGNORECASE)


def expand_group(expr: str) -> list[int]:
    nums = [int(v) for v in re.findall(r"\d+", expr)]
    if len(nums) == 2 and any(ch in expr for ch in "-–") and nums[1] >= nums[0]:
        return list(range(nums[0], nums[1] + 1))
    return nums


def audit(path: Path) -> dict:
    summary, paragraphs = audit_docx(path)
    references: dict[int, str] = {}
    for entry in summary["reference_entries"]:
        m = REF_NUM_RE.match(entry)
        if m:
            references[int(m.group(1))] = entry

    # Main body excludes the bibliography and everything after it.
    main: list[dict] = []
    for p in paragraphs:
        text = normalize(p["text"])
        if text.casefold() == "βιβλιογραφία":
            break
        main.append(p)

    current_chapter: str | None = None
    per_chapter: dict[str, Counter[int]] = {str(i): Counter() for i in range(1, 8)}
    per_chapter_words: Counter[str] = Counter()
    all_valid: Counter[int] = Counter()
    rejected_groups: list[str] = []

    for p in main:
        text = normalize(p["text"])
        if p.get("heading_level") == 1:
            m = CHAPTER_RE.search(text)
            current_chapter = m.group(1) if m else None
        if current_chapter:
            per_chapter_words[current_chapter] += len(words(text))
        for m in CIT_GROUP_RE.finditer(text):
            nums = expand_group(m.group(1))
            if nums and all(n in references for n in nums):
                for n in nums:
                    all_valid[n] += 1
                    if current_chapter:
                        per_chapter[current_chapter][n] += 1
            else:
                rejected_groups.append(m.group(0))

    return {
        "path": summary["path"],
        "reference_count": len(references),
        "references": references,
        "valid_in_text_citation_mentions": sum(all_valid.values()),
        "unique_cited_reference_count": len(all_valid),
        "uncited_reference_numbers": sorted(set(references) - set(all_valid)),
        "reference_usage": {str(k): all_valid.get(k, 0) for k in sorted(references)},
        "chapter_words": dict(per_chapter_words),
        "chapter_citations": {
            ch: {
                "citation_mentions": sum(counter.values()),
                "unique_references": sorted(counter),
                "unique_reference_count": len(counter),
                "mentions_per_1000_words": round(
                    1000 * sum(counter.values()) / per_chapter_words[ch], 2
                ) if per_chapter_words[ch] else 0.0,
            }
            for ch, counter in per_chapter.items()
        },
        "rejected_bracket_groups": rejected_groups,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="docs/thesis/audits/docx-corpus/citation-audit.md")
    args = parser.parse_args()
    targets = [
        ROOT / "thesis/archive/T714_run66_full_review_ready.docx",
        ROOT / "thesis/archive/T715_run98_audit_reconciled_reader_scoped.docx",
        ROOT / "thesis/drafts/resilient-ai-agents-thesis-supervisor-ready-stage9.docx",
    ]
    reports = [audit(p) for p in targets]
    lines = [
        "# Thesis citation coverage audit",
        "",
        "Counts below accept only bracketed numbers that resolve to an actual numbered bibliography entry in that same DOCX. This removes most false positives from experimental bracket notation.",
        "",
        "| Document | References | Valid citation mentions | Unique refs cited | Uncited refs |",
        "|---|---:|---:|---:|---|",
    ]
    for r in reports:
        uncited = ", ".join(map(str, r["uncited_reference_numbers"])) or "—"
        lines.append(
            f"| `{r['path']}` | {r['reference_count']} | {r['valid_in_text_citation_mentions']} | "
            f"{r['unique_cited_reference_count']} | {uncited} |"
        )
    lines.append("")
    for r in reports:
        lines.extend([f"## {r['path']}", "", "### Chapter-level density", "", "| Chapter | Words | Citation mentions | Unique refs | Mentions / 1k words |", "|---|---:|---:|---:|---:|"])
        for ch in map(str, range(1, 8)):
            c = r["chapter_citations"][ch]
            lines.append(
                f"| {ch} | {r['chapter_words'].get(ch, 0)} | {c['citation_mentions']} | "
                f"{c['unique_reference_count']} | {c['mentions_per_1000_words']:.2f} |"
            )
        lines.extend(["", "### Reference usage", ""])
        for n, entry in r["references"].items():
            lines.append(f"- **[{n}] — {r['reference_usage'][str(n)]} in-text mentions:** {entry}")
        lines.extend(["", "### Bracket groups rejected as non-citations", ""])
        if r["rejected_bracket_groups"]:
            unique = []
            for value in r["rejected_bracket_groups"]:
                if value not in unique:
                    unique.append(value)
            lines.append("- " + ", ".join(f"`{x}`" for x in unique[:80]))
        else:
            lines.append("- None")
        lines.append("")

    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
