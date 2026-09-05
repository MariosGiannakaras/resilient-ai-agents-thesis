#!/usr/bin/env python3
"""Audit the synchronized ThesisBibliography corpus for thesis-writing coverage.

This is a writing-selection audit, not a change to bibliography authority. It ranks
already citation-ready records by relevance to the final thesis and separately
surfaces non-citation research materials (notably technical talks/transcripts).
"""
from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "research/bibliography"
MANIFEST = BIB / "citation-ready/manifest.csv"

CURRENT_TITLES = [
    "Reinforcement Learning: An Introduction",
    "Reactive Exploration to Cope with Non-Stationarity in Lifelong Reinforcement Learning",
    "Loss of plasticity in deep continual learning",
    "The Primacy Bias in Deep Reinforcement Learning",
    "Empirical Design in Reinforcement Learning",
    "Deep Reinforcement Learning That Matters",
    "Online Reinforcement Learning in Non-Stationary Context-Driven Environments",
    "Partial Models for Building Adaptive Model-Based Reinforcement Learning Agents",
    "Q-learning: Off-policy TD Control",
    "Playing Atari with Deep Reinforcement Learning",
    "Revisiting Fundamentals of Experience Replay",
    "Proximal Policy Optimization Algorithms",
    "Implementation Matters in Deep Policy Gradients",
    "A Survey of Continual Reinforcement Learning",
    "Deep Reinforcement Learning in Non-stationary Environments",
    "Deep Reinforcement Learning at the Edge of the Statistical Precipice",
    "Time Limits in Reinforcement Learning",
]

CATEGORIES = {
    "RL foundations and tabular methods": [
        "reinforcement learning", "markov decision", "q-learning", "sarsa", "temporal difference"
    ],
    "DQN / replay / deep value learning": [
        "dqn", "deep q", "experience replay", "target network", "deep reinforcement"
    ],
    "PPO / policy gradients": [
        "ppo", "proximal policy", "policy gradient", "actor-critic", "gae"
    ],
    "Dyna / model-based adaptation": [
        "dyna", "model-based", "partial model", "planning", "learned model"
    ],
    "non-stationarity and continual RL": [
        "non-station", "continual", "lifelong", "changing", "dynamic", "plasticity", "primacy"
    ],
    "resilience / recovery / adaptation": [
        "resilien", "recovery", "adaptation", "adaptive", "novelty", "failure profile"
    ],
    "robustness / uncertainty / disturbances": [
        "robust", "uncertainty", "noise", "corrupt", "perturb", "partial observ", "ood", "out-of-distribution"
    ],
    "empirical design / statistics / reproducibility": [
        "empirical design", "statistical", "reproduc", "confidence", "few-run", "performance profile", "time limit", "evaluation"
    ],
    "generalization / benchmarks / GridWorld": [
        "generalization", "benchmark", "gridworld", "grid world", "novgrid", "environment randomization"
    ],
    "safety / constrained adaptation": [
        "safe", "safety", "constraint", "cmdp", "risk-sensitive", "runtime assurance"
    ],
}


def norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.casefold()).strip()


def title_is_current(title: str) -> bool:
    nt = norm(title)
    for current in CURRENT_TITLES:
        nc = norm(current)
        if nc in nt or nt in nc:
            return True
        at = set(nt.split())
        ac = set(nc.split())
        if at and ac and len(at & ac) / len(at | ac) >= 0.58:
            return True
    return False


def analysis_excerpt(source_id: str) -> str:
    candidates = [
        BIB / "citation-ready/analyses" / f"{source_id}.md",
        BIB / "analyses" / f"{source_id}.md",
    ]
    for path in candidates:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        # Prefer explicit note/decision/value sections, then useful non-heading prose.
        blocks = re.split(r"\n(?=##?\s)", text)
        preferred: list[str] = []
        for block in blocks:
            low = block.casefold()
            if any(k in low for k in ("απόφαση", "αξιολόγηση", "thesis", "χρή", "value", "συνεισ")):
                preferred.append(block)
        pool = "\n".join(preferred) if preferred else text
        lines = []
        for line in pool.splitlines():
            line = line.strip(" -*\t")
            if not line or line.startswith("#") or line.startswith("---") or ":" in line[:35]:
                continue
            if len(line) >= 45:
                lines.append(line)
            if len(" ".join(lines)) >= 500:
                break
        return " ".join(lines)[:650]
    return ""


def score_row(row: dict[str, str], keywords: list[str]) -> int:
    fields = " ".join(
        row.get(k, "") for k in ("Τίτλος", "Θέματα", "Κεφάλαια", "Σημείωση", "Ρόλος")
    ).casefold()
    score = sum(3 if kw in row.get("Τίτλος", "").casefold() else 1 for kw in keywords if kw in fields)
    if row.get("Ρόλος", "").casefold() == "κύρια":
        score += 2
    if row.get("Κατάσταση", "").casefold() == "επαληθευμένη":
        score += 1
    return score


def research_materials() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    analyses = BIB / "analyses"
    if not analyses.is_dir():
        return rows
    for path in sorted(analyses.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        low = text.casefold()
        if not any(k in low for k in ("youtube", "seminar", "transcript", "workshop", "talk")):
            continue
        source_id = path.stem
        title = ""
        for line in text.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        decision = ""
        if "keep for thesis theory synthesis" in low or "διατήρηση" in low and "theory" in low:
            decision = "useful-theory"
        elif "απόρριψη" in low or "rejected" in low:
            decision = "discovery/rejected-as-citation"
        else:
            decision = "reviewed-material"
        src = BIB / "sources" / f"{source_id}.md"
        url = ""
        if src.is_file():
            first = src.read_text(encoding="utf-8", errors="replace").splitlines()[:6]
            for line in first:
                m = re.search(r"https?://\S+", line)
                if m:
                    url = m.group(0).rstrip(")>,")
                    break
        rows.append({
            "id": source_id,
            "title": title,
            "decision": decision,
            "url": url,
            "excerpt": analysis_excerpt(source_id),
        })
    return rows


def main() -> int:
    with MANIFEST.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    current = [r for r in rows if title_is_current(r.get("Τίτλος", ""))]
    out_lines = [
        "# ThesisBibliography writing audit",
        "",
        "This report audits the repository-synchronized, citation-ready corpus for thesis-writing coverage. It does not promote rejected material or alter bibliography authority.",
        "",
        f"- Citation-ready records inspected: **{len(rows)}**.",
        f"- Records heuristically matching the current 17-entry thesis bibliography: **{len(current)}** (book-chapter/reference-title variants can make this differ from 17).",
        f"- Citation-ready records not represented by the current narrow bibliography: **{len(rows) - len(current)}**.",
        "",
        "## Category candidate shortlists",
        "",
        "Each shortlist favors already verified citation-ready sources with explicit relevance in the canonical manifest. Inclusion in the final thesis still requires a concrete claim/section role; this is not a quota list.",
        "",
    ]

    selected_ids: set[str] = set()
    for category, keywords in CATEGORIES.items():
        scored = []
        for row in rows:
            if title_is_current(row.get("Τίτλος", "")):
                continue
            score = score_row(row, keywords)
            if score > 0:
                scored.append((score, row))
        scored.sort(key=lambda x: (-x[0], x[1].get("Τίτλος", "")))
        top = scored[:12]
        out_lines.extend([f"### {category}", ""])
        if not top:
            out_lines.append("- No additional citation-ready candidate identified by metadata keywords.")
        for score, row in top:
            sid = row.get("Κωδικός", "")
            selected_ids.add(sid)
            excerpt = analysis_excerpt(sid)
            note = row.get("Σημείωση", "").strip()
            out_lines.append(
                f"- **{sid} — {row.get('Τίτλος','')}** (score {score}; role {row.get('Ρόλος','')}). "
                f"Chapters: {row.get('Κεφάλαια','') or '—'}. Topics: {row.get('Θέματα','') or '—'}. "
                f"Canonical note: {note or '—'}"
            )
            if excerpt:
                out_lines.append(f"  - Analysis excerpt: {excerpt}")
        out_lines.append("")

    out_lines.extend([
        "## Cross-category de-duplicated candidate pool",
        "",
        f"Metadata ranking surfaced **{len(selected_ids)}** distinct additional citation-ready records across the thesis-relevant categories above.",
        "",
    ])
    index = {r.get("Κωδικός", ""): r for r in rows}
    for sid in sorted(selected_ids):
        row = index[sid]
        out_lines.append(f"- {sid}: {row.get('Τίτλος','')}")

    materials = research_materials()
    useful = [r for r in materials if r["decision"] == "useful-theory"]
    out_lines.extend([
        "",
        "## Technical talks / YouTube / informal research material",
        "",
        f"- Talk/transcript/workshop analysis records inspected: **{len(materials)}**.",
        f"- Explicitly retained as useful thesis-theory material: **{len(useful)}**.",
        "- Policy: these can shape explanation and discovery, but exact claims should cite the underlying primary papers whenever available.",
        "",
    ])
    for r in materials:
        out_lines.append(f"### {r['id']} — {r['title'] or '(untitled analysis)'}")
        out_lines.append("")
        out_lines.append(f"- Decision: **{r['decision']}**")
        if r["url"]:
            out_lines.append(f"- Source URL: {r['url']}")
        if r["excerpt"]:
            out_lines.append(f"- Review: {r['excerpt']}")
        out_lines.append("")

    out = ROOT / "docs/thesis/audits/bibliography-writing-audit.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    print(f"Citation-ready={len(rows)}; additional candidate pool={len(selected_ids)}; informal materials={len(materials)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
