#!/usr/bin/env python3
"""Mine substantive cross-version thesis content for restoration/rewrite planning."""
from __future__ import annotations

import argparse
import re
from difflib import SequenceMatcher
from pathlib import Path

from audit_thesis_docx_corpus import ROOT, audit_docx, normalize, words

CHAPTER_RE = re.compile(r"Κεφάλαιο\s+([1-7])", re.IGNORECASE)


def chapter_paragraphs(paragraphs: list[dict]) -> dict[str, list[str]]:
    current: str | None = None
    out: dict[str, list[str]] = {str(i): [] for i in range(1, 8)}
    for p in paragraphs:
        text = normalize(p.get("text", ""))
        if not text:
            continue
        if p.get("heading_level") == 1:
            m = CHAPTER_RE.search(text)
            current = m.group(1) if m else None
            continue
        if current and not p.get("heading_level") and len(words(text)) >= 24:
            out[current].append(text)
    return out


def max_similarity(text: str, targets: list[str]) -> float:
    a = text.casefold()
    best = 0.0
    for target in targets:
        # Fast length-ratio guard; wildly different paragraph sizes cannot be close matches.
        la, lb = len(a), len(target)
        if not la or not lb:
            continue
        ratio = min(la, lb) / max(la, lb)
        if ratio < 0.35:
            continue
        score = SequenceMatcher(None, a, target.casefold(), autojunk=False).ratio()
        if score > best:
            best = score
            if best >= 0.96:
                break
    return best


def load(path: str) -> tuple[dict, dict[str, list[str]]]:
    summary, paras = audit_docx(ROOT / path)
    return summary, chapter_paragraphs(paras)


def candidates(source: dict[str, list[str]], target: dict[str, list[str]]) -> dict[str, list[tuple[float, str]]]:
    result: dict[str, list[tuple[float, str]]] = {}
    for ch in map(str, range(1, 8)):
        rows: list[tuple[float, str]] = []
        for text in source[ch]:
            score = max_similarity(text, target[ch])
            if score < 0.72:
                rows.append((score, text))
        rows.sort(key=lambda item: (item[0], -len(words(item[1]))))
        result[ch] = rows
    return result


def write_pair(lines: list[str], label: str, src_name: str, dst_name: str,
               src: dict[str, list[str]], dst: dict[str, list[str]]) -> None:
    mined = candidates(src, dst)
    lines.extend([f"## {label}", "", f"Source: `{src_name}`", "", f"Comparison target: `{dst_name}`", ""])
    for ch in map(str, range(1, 8)):
        rows = mined[ch]
        strong = [r for r in rows if r[0] < 0.45]
        medium = [r for r in rows if 0.45 <= r[0] < 0.72]
        lines.append(f"### Chapter {ch}: {len(strong)} strongly distinct, {len(medium)} partially distinct paragraphs")
        lines.append("")
        for score, text in (strong + medium)[:8]:
            lines.append(f"- **similarity {score:.3f}; {len(words(text))} words** — {text}")
        if not rows:
            lines.append("- No materially distinct long paragraph detected by this mechanical test.")
        lines.append("")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="docs/thesis/audits/docx-corpus")
    args = parser.parse_args()
    out = ROOT / args.output
    out.mkdir(parents=True, exist_ok=True)

    stage6_path = "thesis/drafts/resilient-ai-agents-thesis-supervisor-ready-stage6.docx"
    stage8_path = "thesis/drafts/resilient-ai-agents-thesis-supervisor-ready-stage8.docx"
    stage9_path = "thesis/drafts/resilient-ai-agents-thesis-supervisor-ready-stage9.docx"
    t714_path = "thesis/archive/T714_run66_full_review_ready.docx"
    t715_path = "thesis/archive/T715_run98_audit_reconciled_reader_scoped.docx"

    s6, p6 = load(stage6_path)
    s8, p8 = load(stage8_path)
    s9, p9 = load(stage9_path)
    t714, p714 = load(t714_path)
    t715, p715 = load(t715_path)

    lines = [
        "# Cross-version thesis content mining",
        "",
        "Mechanical paragraph-level mining for rewrite planning. Similarity is character-level SequenceMatcher within the same chapter; low similarity means different wording/content, not automatically higher quality or truth. Every candidate must still be checked against current repository scientific and bibliography authority before reuse.",
        "",
        "## Version relation summary",
        "",
        f"- Stage 6: {s6['word_count']} words.",
        f"- Stage 8: {s8['word_count']} words.",
        f"- Stage 9: {s9['word_count']} words.",
        f"- T-714: {t714['word_count']} words.",
        f"- T-715 audit-reconciled: {t715['word_count']} words.",
        "- Stage 8/9 are near-neighbour editorial variants; Stage 9 is used as the representative old full draft below.",
        "",
    ]
    write_pair(lines, "Old Stage 9 material not closely represented in T-714", stage9_path, t714_path, p9, p714)
    write_pair(lines, "Old Stage 9 material not closely represented in compressed T-715", stage9_path, t715_path, p9, p715)
    write_pair(lines, "T-714 material not closely represented in old Stage 9", t714_path, stage9_path, p714, p9)

    # Small editorial-delta diagnostic for the near-identical Stage 6/8/9 family.
    lines.extend(["## Stage 6/8/9 editorial-family delta", ""])
    for label, src, dst in (("Stage 6 → Stage 9", p6, p9), ("Stage 8 → Stage 9", p8, p9)):
        mined = candidates(src, dst)
        total = sum(len(v) for v in mined.values())
        strong = sum(sum(1 for score, _ in v if score < 0.45) for v in mined.values())
        lines.append(f"- {label}: {total} long paragraphs below 0.72 similarity; {strong} below 0.45.")
    lines.append("")

    # Reference lists are kept verbatim for bibliography reconciliation.
    lines.extend(["## Reference lists captured from the retained DOCX files", ""])
    for summary in (s6, s8, s9, t714, t715):
        lines.append(f"### {summary['path']} — {summary['reference_entry_count']} detected entries")
        lines.append("")
        for ref in summary["reference_entries"]:
            lines.append(f"- {ref}")
        lines.append("")

    (out / "content-mining.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out / 'content-mining.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
