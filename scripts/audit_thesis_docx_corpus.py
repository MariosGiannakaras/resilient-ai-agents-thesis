#!/usr/bin/env python3
"""Audit retained thesis DOCX milestones without changing them.

The report is content-oriented: document word counts, heading/section structure,
reference-list size, in-text numeric citation usage, captions/placeholders and
coarse cross-version text overlap. It reads OOXML directly with the standard
library so it can run in repository CI without Word/LibreOffice.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
WORD_RE = re.compile(r"[^\W_]+(?:[-’'][^\W_]+)*", re.UNICODE)
CIT_RE = re.compile(r"\[(\d+(?:\s*(?:-|–|,)\s*\d+)*)\]")
PLACEHOLDER_RE = re.compile(
    r"(?:\[\[[^\]]+\]\]|\b(?:TODO|TBD|PLACEHOLDER)\b|"
    r"\b(?:ΟΝΟΜΑ\s+ΦΟΙΤΗΤΗ|ΑΡΙΘΜΟΣ\s+ΜΗΤΡΩΟΥ|ΟΝΟΜΑ\s+ΕΠΙΒΛΕΠΟΝΤΑ)\b)",
    re.IGNORECASE,
)
REFERENCE_HEADINGS = {"βιβλιογραφία", "references", "βιβλιογραφικες αναφορες", "βιβλιογραφικές αναφορές"}


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def normalize(text: str) -> str:
    return " ".join(text.split())


def style_map(zf: zipfile.ZipFile) -> dict[str, str]:
    try:
        root = ET.fromstring(zf.read("word/styles.xml"))
    except KeyError:
        return {}
    out: dict[str, str] = {}
    for style in root.findall(f".//{W}style"):
        sid = style.get(f"{W}styleId", "")
        name = style.find(f"{W}name")
        out[sid] = name.get(f"{W}val", sid) if name is not None else sid
    return out


def paragraph_text(p: ET.Element) -> str:
    parts: list[str] = []
    for node in p.iter():
        if node.tag == f"{W}t" and node.text:
            parts.append(node.text)
        elif node.tag == f"{W}tab":
            parts.append("\t")
        elif node.tag == f"{W}br":
            parts.append("\n")
    return normalize("".join(parts))


def paragraph_style(p: ET.Element, styles: dict[str, str]) -> tuple[str, str]:
    ppr = p.find(f"{W}pPr")
    if ppr is None:
        return "", ""
    node = ppr.find(f"{W}pStyle")
    if node is None:
        return "", ""
    sid = node.get(f"{W}val", "")
    return sid, styles.get(sid, sid)


def heading_level(style_id: str, style_name: str) -> int | None:
    for value in (style_name, style_id):
        compact = value.replace(" ", "")
        m = re.search(r"heading([1-9])$", compact, re.IGNORECASE)
        if m:
            return int(m.group(1))
    return None


def parse_numeric_citation(expr: str) -> set[int]:
    nums = [int(x) for x in re.findall(r"\d+", expr)]
    if not nums:
        return set()
    if any(ch in expr for ch in "-–") and len(nums) == 2:
        lo, hi = nums
        if 0 < hi - lo <= 200:
            return set(range(lo, hi + 1))
    return set(nums)


def shingles(tokens: list[str], n: int = 5) -> set[str]:
    if len(tokens) < n:
        return {" ".join(tokens)} if tokens else set()
    return {
        hashlib.sha1(" ".join(tokens[i : i + n]).encode("utf-8")).hexdigest()
        for i in range(len(tokens) - n + 1)
    }


def audit_docx(path: Path) -> tuple[dict, list[dict]]:
    with zipfile.ZipFile(path) as zf:
        styles = style_map(zf)
        root = ET.fromstring(zf.read("word/document.xml"))

    paragraphs: list[dict] = []
    for p in root.iter(f"{W}p"):
        text = paragraph_text(p)
        sid, sname = paragraph_style(p, styles)
        level = heading_level(sid, sname)
        paragraphs.append({"text": text, "style_id": sid, "style": sname, "heading_level": level})

    all_text = "\n".join(p["text"] for p in paragraphs if p["text"])
    all_words = words(all_text)
    citations = list(CIT_RE.finditer(all_text))
    cited_numbers: set[int] = set()
    for m in citations:
        cited_numbers |= parse_numeric_citation(m.group(1))

    headings = [p for p in paragraphs if p["text"] and p["heading_level"]]
    top_sections: list[dict] = []
    current: dict | None = None
    for p in paragraphs:
        if p["text"] and p["heading_level"] == 1:
            current = {"heading": p["text"], "words": 0}
            top_sections.append(current)
            continue
        if current is not None and p["text"]:
            current["words"] += len(words(p["text"]))

    ref_start: int | None = None
    for i, p in enumerate(paragraphs):
        if normalize(p["text"]).casefold() in REFERENCE_HEADINGS:
            ref_start = i
            break
    ref_entries: list[str] = []
    if ref_start is not None:
        for p in paragraphs[ref_start + 1 :]:
            if p["heading_level"] == 1 and p["text"]:
                break
            text = p["text"]
            if not text:
                continue
            if p["heading_level"]:
                continue
            ref_entries.append(text)

    captions = [
        p["text"]
        for p in paragraphs
        if p["text"]
        and (
            "caption" in p["style"].casefold()
            or re.match(r"^(?:Σχήμα|Πίνακας|Figure|Table)\s+\d+", p["text"], re.IGNORECASE)
        )
    ]
    placeholders = PLACEHOLDER_RE.findall(all_text)

    summary = {
        "path": path.relative_to(ROOT).as_posix(),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "bytes": path.stat().st_size,
        "word_count": len(all_words),
        "paragraph_count": len([p for p in paragraphs if p["text"]]),
        "heading_count": len(headings),
        "heading1_count": sum(1 for p in headings if p["heading_level"] == 1),
        "table_count": all_text.count("Πίνακας ") + all_text.count("Table "),
        "caption_count": len(captions),
        "in_text_numeric_citation_occurrences": len(citations),
        "unique_numeric_citation_numbers": sorted(cited_numbers),
        "unique_numeric_citation_count": len(cited_numbers),
        "reference_heading_found": ref_start is not None,
        "reference_entry_count": len(ref_entries),
        "placeholder_count": len(placeholders),
        "top_level_sections": top_sections,
        "headings": [
            {"level": p["heading_level"], "text": p["text"]}
            for p in headings
        ],
        "reference_entries": ref_entries,
        "captions": captions,
        "word_fingerprint_sha256": hashlib.sha256(
            " ".join(w.casefold() for w in all_words).encode("utf-8")
        ).hexdigest(),
    }
    return summary, paragraphs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="docs/thesis/audits/docx-corpus")
    args = parser.parse_args()
    out = ROOT / args.output
    out.mkdir(parents=True, exist_ok=True)

    paths = sorted((ROOT / "thesis" / "drafts").glob("*.docx")) + sorted(
        (ROOT / "thesis" / "archive").glob("*.docx")
    )
    if not paths:
        raise SystemExit("No retained thesis DOCX files found")

    summaries: list[dict] = []
    texts: dict[str, list[str]] = {}
    shingle_map: dict[str, set[str]] = {}
    for path in paths:
        summary, paragraphs = audit_docx(path)
        summaries.append(summary)
        rel = summary["path"]
        text_lines = [p["text"] for p in paragraphs if p["text"]]
        texts[rel] = text_lines
        toks = [w.casefold() for w in words(" ".join(text_lines))]
        shingle_map[rel] = shingles(toks)
        safe = path.stem.replace(" ", "_")
        (out / f"{safe}.txt").write_text("\n".join(text_lines) + "\n", encoding="utf-8")

    comparisons: list[dict] = []
    for i, a in enumerate(summaries):
        for b in summaries[i + 1 :]:
            sa = shingle_map[a["path"]]
            sb = shingle_map[b["path"]]
            union = len(sa | sb)
            inter = len(sa & sb)
            comparisons.append(
                {
                    "a": a["path"],
                    "b": b["path"],
                    "word_delta_b_minus_a": b["word_count"] - a["word_count"],
                    "five_word_shingle_jaccard": round(inter / union, 6) if union else 1.0,
                }
            )

    payload = {"documents": summaries, "comparisons": comparisons}
    (out / "audit.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Retained thesis DOCX corpus audit",
        "",
        "Generated mechanically from the tracked DOCX files. Word counts are whole-document OOXML text-token counts and include front matter/reference/appendix text; use section counts for composition diagnosis.",
        "",
        "| Document | Words | Paras | H1 | Numeric citation occurrences | Unique citation nos. | Reference entries | Placeholders |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for d in summaries:
        lines.append(
            f"| `{d['path']}` | {d['word_count']} | {d['paragraph_count']} | {d['heading1_count']} | "
            f"{d['in_text_numeric_citation_occurrences']} | {d['unique_numeric_citation_count']} | "
            f"{d['reference_entry_count']} | {d['placeholder_count']} |"
        )
        lines.append("")
        lines.append(f"## {d['path']}")
        lines.append("")
        for sec in d["top_level_sections"]:
            lines.append(f"- {sec['heading']}: {sec['words']} words")
        lines.append("")

    lines.extend([
        "## Selected comparisons",
        "",
        "Five-word-shingle Jaccard is a coarse content-retention indicator (1.0 identical token shingles, 0.0 no shared 5-word sequences).",
        "",
        "| A | B | Δ words B-A | 5-word Jaccard |",
        "|---|---|---:|---:|",
    ])
    interesting = {
        "stage3", "stage6", "stage8", "stage9", "T714_run66_full_review_ready", "T715_run98_audit_reconciled_reader_scoped"
    }
    for c in comparisons:
        if any(k in c["a"] for k in interesting) and any(k in c["b"] for k in interesting):
            lines.append(
                f"| `{c['a']}` | `{c['b']}` | {c['word_delta_b_minus_a']} | {c['five_word_shingle_jaccard']:.3f} |"
            )
    (out / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Audited {len(summaries)} DOCX files into {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
