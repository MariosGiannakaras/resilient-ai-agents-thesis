#!/usr/bin/env python3
"""Scan the complete synchronized research corpus, including non-citation material."""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "research/bibliography"
MANIFEST = BIB / "citation-ready/manifest.csv"

TOPIC_TERMS = {
    "nonstationarity": ("non-station", "nonstation", "changing environment", "dynamic environment", "lifelong", "continual"),
    "resilience_recovery": ("resilien", "recovery", "recover", "adaptation", "adaptive"),
    "uncertainty_robustness": ("robust", "uncertainty", "observation noise", "observation corrupt", "action failure", "perturb", "out-of-distribution", "ood"),
    "methods": ("q-learning", "sarsa", "dqn", "deep q", "ppo", "proximal policy", "dyna", "model-based"),
    "evaluation": ("empirical design", "reproduc", "statistical", "confidence interval", "seed", "benchmark", "evaluation", "time limit"),
    "gridworld_testbed": ("gridworld", "grid world", "novgrid", "navigation"),
    "safety": ("safe reinforcement", "safety", "constraint mdp", "cmdp", "risk-sensitive"),
}
ALL_TERMS = tuple(dict.fromkeys(t for terms in TOPIC_TERMS.values() for t in terms))


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def first_title(doc: str) -> str:
    for line in doc.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def status_from_analysis(doc: str) -> str:
    low = doc.casefold()
    for label in ("επαληθευμένη", "μερικώς επαληθευμένη", "απόρριψη", "reviewed", "verified", "rejected"):
        if label in low[:900]:
            return label
    return "unspecified"


def score(doc: str) -> tuple[int, list[str]]:
    low = doc.casefold()
    cats = []
    score_value = 0
    for category, terms in TOPIC_TERMS.items():
        hits = sum(low.count(term) for term in terms)
        if hits:
            cats.append(category)
            score_value += min(hits, 8)
    return score_value, cats


def excerpt(doc: str) -> str:
    lines = []
    for line in doc.splitlines():
        s = line.strip(" -*\t")
        if not s or s.startswith("#") or s.startswith("---"):
            continue
        if len(s) < 50:
            continue
        lines.append(s)
        if len(" ".join(lines)) >= 520:
            break
    return " ".join(lines)[:700]


def source_url(source_id: str) -> str:
    path = BIB / "sources" / f"{source_id}.md"
    if not path.is_file():
        return ""
    m = re.search(r"https?://\S+", "\n".join(text(path).splitlines()[:10]))
    return m.group(0).rstrip(")>,") if m else ""


def main() -> int:
    with MANIFEST.open(encoding="utf-8-sig", newline="") as fh:
        citation_rows = list(csv.DictReader(fh))
    citation_ids = {r.get("Κωδικός", "") for r in citation_rows}

    source_files = sorted((BIB / "sources").glob("SRC-*.md"))
    analysis_files = sorted((BIB / "analyses").glob("SRC-*.md"))
    evidence_files = sorted((BIB / "evidence").glob("SRC-*.*"))
    material_files = [p for p in (BIB / "materials").rglob("*") if p.is_file()]
    note_files = [p for p in (BIB / "notes").rglob("*") if p.is_file()]

    relevant_nonready = []
    talk_material = []
    for path in analysis_files:
        sid = path.stem
        doc = text(path)
        s, cats = score(doc)
        low = doc.casefold()
        if any(term in low for term in ("youtube", "seminar", "transcript", "workshop", " talk")):
            talk_material.append((s, sid, first_title(doc), status_from_analysis(doc), cats, source_url(sid), excerpt(doc)))
        if sid not in citation_ids and s:
            relevant_nonready.append((s, sid, first_title(doc), status_from_analysis(doc), cats, source_url(sid), excerpt(doc)))

    relevant_nonready.sort(key=lambda row: (-row[0], row[1]))
    talk_material.sort(key=lambda row: (-row[0], row[1]))

    material_hits = []
    for path in material_files:
        try:
            doc = text(path)
        except OSError:
            continue
        s, cats = score(doc)
        if s:
            material_hits.append((s, path.relative_to(BIB).as_posix(), cats, excerpt(doc)))
    material_hits.sort(key=lambda row: (-row[0], row[1]))

    note_hits = []
    for path in note_files:
        try:
            doc = text(path)
        except OSError:
            continue
        s, cats = score(doc)
        if s:
            note_hits.append((s, path.relative_to(BIB).as_posix(), cats, excerpt(doc)))
    note_hits.sort(key=lambda row: (-row[0], row[1]))

    lines = [
        "# Complete ThesisBibliography corpus audit",
        "",
        "This scan covers the complete synchronized research corpus, not only the citation-ready layer. Non-citation material is never automatically promoted to formal evidence.",
        "",
        f"- Canonical source records scanned: **{len(source_files)}**.",
        f"- Scientific analysis records scanned: **{len(analysis_files)}**.",
        f"- Evidence records present: **{len(evidence_files)}**.",
        f"- Citation-ready records: **{len(citation_ids)}**.",
        f"- Extracted research-material files scanned: **{len(material_files)}**.",
        f"- Working/research-note files scanned: **{len(note_files)}**.",
        f"- Thesis-relevant analyzed records outside citation-ready: **{len(relevant_nonready)}**.",
        f"- Talk/seminar/transcript/workshop analysis records: **{len(talk_material)}**.",
        "",
        "## Highest-relevance analyzed records outside citation-ready",
        "",
        "These are useful for discovery/synthesis only unless bibliography governance later promotes them.",
        "",
    ]
    for s, sid, title, status, cats, url, ex in relevant_nonready[:60]:
        lines.append(f"### {sid} — {title or '(untitled)'}")
        lines.append("")
        lines.append(f"- Relevance score: {s}; categories: {', '.join(cats)}; analysis status: {status}")
        if url:
            lines.append(f"- URL: {url}")
        if ex:
            lines.append(f"- Analysis: {ex}")
        lines.append("")

    lines.extend(["## Talks, seminars, workshops and transcripts", ""])
    for s, sid, title, status, cats, url, ex in talk_material:
        lines.append(f"### {sid} — {title or '(untitled)'}")
        lines.append("")
        lines.append(f"- Relevance score: {s}; categories: {', '.join(cats)}; analysis status: {status}")
        if url:
            lines.append(f"- URL: {url}")
        if ex:
            lines.append(f"- Review: {ex}")
        lines.append("")

    lines.extend(["## Relevant extracted materials", ""])
    for s, path, cats, ex in material_hits[:40]:
        lines.append(f"- **{path}** — score {s}; {', '.join(cats)}. {ex}")

    lines.extend(["", "## Relevant research/working notes", ""])
    for s, path, cats, ex in note_hits[:40]:
        lines.append(f"- **{path}** — score {s}; {', '.join(cats)}. {ex}")

    out = ROOT / "docs/thesis/audits/bibliography-full-corpus-audit.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"sources={len(source_files)} analyses={len(analysis_files)} citation_ready={len(citation_ids)} "
        f"nonready_relevant={len(relevant_nonready)} talks={len(talk_material)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
