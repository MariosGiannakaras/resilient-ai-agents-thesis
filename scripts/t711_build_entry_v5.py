#!/usr/bin/env python3
"""T-711 final planned-asset completeness and reference-cleanup layer.

This wrapper closes the last content defects found by the full v4 rendered-page review:

- all 24 figures enumerated by the accepted T-710 MANUSCRIPT_INDEX handoff are inserted
  exactly once in their planned main-text/appendix roles;
- Appendix B contains the registered diagnostic figures themselves rather than visible
  T-711 asset-ID handoff bullets;
- the two methodology figures that are main-thesis assets but lacked inline placement
  markers are inserted at the end of Chapter 3;
- the verified Q-learning chapter excerpt is rendered as a conventional bibliographic
  identity using only verified Sutton/Barto book/chapter metadata already present in
  the citation-ready records.

The layer changes composition only. It does not modify scientific values, estimands,
intervals, denominators, censoring decisions, source assets, or bibliography evidence.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from docx import Document

import t711_build_entry_v4 as v4


t711 = v4.t711


PLANNED_FIGURE_IDS = [
    "FIG-METHOD-026-EXPERIMENT-FLOW",
    "FIG-METHOD-027-RQ-MAP",
    "FIG-RQ1-002-FINAL",
    "FIG-RQ1-003-TIME-AVERAGE",
    "FIG-RQ2-008-ADAPTATION",
    "FIG-RQ2-009-LOSSES",
    "FIG-RQ2-010-CONDITIONS",
    "FIG-RQ3-016-TRAJECTORIES",
    "FIG-RQ3-017-RECOVERED",
    "FIG-RQ3-018-RESTRICTED",
    "FIG-RQ3-019-CONDITIONAL",
    "FIG-RQ3-023-SENSITIVITY",
    "FIG-RQ1-004-FINAL-ROOTS",
    "FIG-RQ1-005-TIME-ROOTS",
    "FIG-RQ1-007-CONTRASTS",
    "FIG-RQ2-012-BENEFIT-ROOTS",
    "FIG-RQ2-013-HEATMAP",
    "FIG-RQ2-014-CONTRASTS",
    "FIG-RQ2-015-PAIRED-ROOTS",
    "FIG-RQ3-021-ROOT-TRAJECTORIES",
    "FIG-RQ3-022-CENSORING",
    "FIG-RQ3-024-CONTRASTS",
    "FIG-RQ3-025-TIMELINE",
    "FIG-METHOD-028-LINEAGE",
]

APPENDIX_GROUPS = {
    "### Β.1 RQ1": [
        "FIG-RQ1-004-FINAL-ROOTS",
        "FIG-RQ1-005-TIME-ROOTS",
        "FIG-RQ1-007-CONTRASTS",
    ],
    "### Β.2 RQ2": [
        "FIG-RQ2-012-BENEFIT-ROOTS",
        "FIG-RQ2-013-HEATMAP",
        "FIG-RQ2-014-CONTRASTS",
        "FIG-RQ2-015-PAIRED-ROOTS",
    ],
    "### Β.3 RQ3": [
        "FIG-RQ3-021-ROOT-TRAJECTORIES",
        "FIG-RQ3-022-CENSORING",
        "FIG-RQ3-024-CONTRASTS",
        "FIG-RQ3-025-TIMELINE",
    ],
}

_previous_preprocess = t711._preprocess_markdown
_previous_identity = t711._analysis_identity
_previous_enhanced_qa = t711._enhanced_qa
_previous_builder_render = t711.builder.render_markdown


def _figure_cache_lines() -> list[str]:
    assets = t711.builder.load_assets()
    lines: list[str] = []
    for number, asset_id in enumerate(PLANNED_FIGURE_IDS, 1):
        asset = assets.get(asset_id)
        if asset is None or asset.get("kind") != "figure":
            raise ValueError(f"planned T-613 figure missing from manifest: {asset_id}")
        lines.append(f"Σχήμα {number} — {asset.get('caption') or asset_id}")
    return lines


def _strip_appendix_handoff_lines(cleaned: str) -> str:
    """Remove placement-only text before the appendix is rendered.

    The accepted appendix Markdown is a handoff authority. Asset IDs are instructions to
    T-711 and must not remain as thesis prose once the corresponding figures are inserted.
    """
    result: list[str] = []
    for raw in cleaned.splitlines():
        stripped = raw.strip()
        if "Προτεινόμενη T-711 τοποθέτηση" in stripped:
            continue
        if re.match(r"^[-*]\s+.*FIG-(?:RQ|METHOD)-", stripped):
            continue
        if "αντίστοιχα registered T-613 tables/CSVs" in stripped:
            continue
        result.append(raw)
    return "\n".join(result)


def _render_clean_chunk(doc, markdown: str, cmap, assets, inserted, inserted_rq_tables, start_new_page=False):
    if not markdown.strip():
        return
    # The markdown has already passed the appendix-aware v1 preprocessing, so use the
    # original parser directly and avoid a second handoff transformation pass.
    return t711._original_render_markdown(
        doc,
        markdown,
        cmap,
        assets,
        inserted,
        inserted_rq_tables,
        start_new_page,
    )


def _add_registered_figures(doc, ids: list[str], assets: dict[str, dict], inserted: list[str]):
    for asset_id in ids:
        if asset_id in inserted:
            continue
        asset = assets.get(asset_id)
        if asset is None:
            raise ValueError(f"planned T-613 figure missing from manifest: {asset_id}")
        if asset.get("kind") != "figure":
            raise ValueError(f"planned figure is not a figure in manifest: {asset_id}")
        t711._add_figure(doc, asset, inserted)


def _render_appendix(doc, md: str, cmap, assets, inserted, inserted_rq_tables):
    cleaned = _strip_appendix_handoff_lines(_previous_preprocess(md, "appendix"))
    lines = cleaned.splitlines()

    anchors = ["### Β.2 RQ2", "### Β.3 RQ3", "## Παράρτημα Γ"]
    positions: dict[str, int] = {}
    for anchor in ["### Β.1 RQ1", *anchors]:
        try:
            positions[anchor] = next(i for i, line in enumerate(lines) if line.strip() == anchor)
        except StopIteration as exc:
            raise ValueError(f"appendix placement anchor missing: {anchor}") from exc

    # Render through each B subsection, then insert only the appendix diagnostics that
    # are not already used in the main Results chapter.
    b2 = positions["### Β.2 RQ2"]
    b3 = positions["### Β.3 RQ3"]
    gamma = positions["## Παράρτημα Γ"]

    _render_clean_chunk(doc, "\n".join(lines[:b2]), cmap, assets, inserted, inserted_rq_tables, False)
    _add_registered_figures(doc, APPENDIX_GROUPS["### Β.1 RQ1"], assets, inserted)

    _render_clean_chunk(doc, "\n".join(lines[b2:b3]), cmap, assets, inserted, inserted_rq_tables, False)
    _add_registered_figures(doc, APPENDIX_GROUPS["### Β.2 RQ2"], assets, inserted)

    _render_clean_chunk(doc, "\n".join(lines[b3:gamma]), cmap, assets, inserted, inserted_rq_tables, False)
    _add_registered_figures(doc, APPENDIX_GROUPS["### Β.3 RQ3"], assets, inserted)

    # Split Γ.1 from Γ.2 so the evidence-lineage figure appears with the lineage prose,
    # not as a detached final appendix artifact.
    remaining = lines[gamma:]
    gamma2 = next((i for i, line in enumerate(remaining) if line.strip() == "### Γ.2 Frozen identities"), None)
    if gamma2 is None:
        raise ValueError("appendix placement anchor missing: ### Γ.2 Frozen identities")
    _render_clean_chunk(doc, "\n".join(remaining[:gamma2]), cmap, assets, inserted, inserted_rq_tables, False)
    _add_registered_figures(doc, ["FIG-METHOD-028-LINEAGE"], assets, inserted)
    _render_clean_chunk(doc, "\n".join(remaining[gamma2:]), cmap, assets, inserted, inserted_rq_tables, False)


def _render_markdown_v5(doc, md: str, cmap, assets, inserted, inserted_rq_tables, start_new_page=True):
    if re.search(r"^#\s+Παραρτήματα", md, re.MULTILINE):
        return _render_appendix(doc, md, cmap, assets, inserted, inserted_rq_tables)

    result = _previous_builder_render(
        doc,
        md,
        cmap,
        assets,
        inserted,
        inserted_rq_tables,
        start_new_page,
    )
    if re.search(r"^#\s+Κεφάλαιο 3\b", md, re.MULTILINE):
        _add_registered_figures(
            doc,
            ["FIG-METHOD-026-EXPERIMENT-FLOW", "FIG-METHOD-027-RQ-MAP"],
            assets,
            inserted,
        )
    return result


def _analysis_identity(source_id: str) -> str:
    if source_id == "SRC-D52DF7B9A4":
        # Verified by the citation-ready chapter record (Chapter 6, pp. 131–135,
        # Sutton/Barto, 2018) and the citation-ready canonical book identity.
        return (
            "Richard S. Sutton and Andrew G. Barto, “Q-learning: Off-policy TD Control,” "
            "in Reinforcement Learning: An Introduction, 2nd ed., The MIT Press, 2018, "
            "pp. 131–135."
        )
    return _previous_identity(source_id)


def _enhanced_qa(output: Path, qa_output: Path):
    _previous_enhanced_qa(output, qa_output)
    report = json.loads(qa_output.read_text(encoding="utf-8"))
    doc = Document(output)
    full_text = "\n".join(paragraph.text for paragraph in doc.paragraphs)

    inserted = report.get("inserted_asset_ids", [])
    missing = [asset_id for asset_id in PLANNED_FIGURE_IDS if asset_id not in inserted]
    unexpected = [asset_id for asset_id in inserted if asset_id not in PLANNED_FIGURE_IDS]
    duplicates = sorted({asset_id for asset_id in inserted if inserted.count(asset_id) > 1})
    visible_handoff_ids = sorted(set(re.findall(r"FIG-(?:RQ|METHOD)-[A-Z0-9-]+", full_text)))
    bad_reference_phrases = [
        phrase
        for phrase in (
            "για το κεφάλαιο του εγχειριδίου",
            "για τη 2η έκδοση του εγχειριδίου",
            "εκπαιδευτικό αντίγραφο κεφαλαίου",
        )
        if phrase in full_text
    ]

    report.update(
        {
            "planned_figure_count": len(PLANNED_FIGURE_IDS),
            "missing_planned_figure_ids": missing,
            "unexpected_inserted_figure_ids": unexpected,
            "duplicate_inserted_figure_ids": duplicates,
            "visible_asset_id_residue": visible_handoff_ids,
            "bad_reference_phrases": bad_reference_phrases,
        }
    )
    if (
        len(inserted) != len(PLANNED_FIGURE_IDS)
        or missing
        or unexpected
        or duplicates
        or visible_handoff_ids
        or bad_reference_phrases
        or report.get("cached_figure_entry_count") != len(PLANNED_FIGURE_IDS)
    ):
        report["status"] = "fail"

    qa_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if report["status"] != "pass":
        raise RuntimeError(f"T-711 v5 structural QA failed: {report}")


t711._mentioned_figure_cache_lines = _figure_cache_lines
t711._analysis_identity = _analysis_identity
t711._enhanced_qa = _enhanced_qa
t711.builder.render_markdown = _render_markdown_v5


if __name__ == "__main__":
    t711.builder.main()
