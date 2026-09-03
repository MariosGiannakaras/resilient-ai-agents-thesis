#!/usr/bin/env python3
"""T-711 final visual-QA compatibility layer.

This wrapper keeps the v1 composition hardening and v2 verified bibliography parser,
then fixes two defects discovered in the second rendered-page review:

- LaTeX command replacement is longest-token-first so ``\\leftarrow`` cannot be
  corrupted by the shorter ``\\le`` replacement.
- Cached lists of figures/tables are derived from the same manuscript placement and
  appendix preprocessing contract used by the renderer, so they describe only items
  that actually appear in the DOCX and include their cached sequence numbers.

Automatic Word TOC/list fields remain present and are still expected to update page
numbers in Microsoft Word. No scientific values or registered asset bytes are changed.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from docx import Document

import t711_build_entry_v2 as v2


t711 = v2.t711


_MATH_REPLACEMENTS = {
    r"\mathbb{R}": "ℝ",
    r"\leftarrow": "←",
    r"\rightarrow": "→",
    r"\operatorname": "",
    r"\varepsilon": "ε",
    r"\epsilon": "ε",
    r"\gamma": "γ",
    r"\alpha": "α",
    r"\beta": "β",
    r"\sigma": "σ",
    r"\Delta": "Δ",
    r"\delta": "δ",
    r"\times": "×",
    r"\pm": "±",
    r"\leq": "≤",
    r"\geq": "≥",
    r"\left": "",
    r"\right": "",
    r"\mathcal": "",
    r"\mathrm": "",
    r"\text": "",
    r"\sum": "Σ",
    r"\max": "max",
    r"\min": "min",
    r"\mid": "|",
    r"\mu": "μ",
    r"\pi": "π",
    r"\in": "∈",
    r"\le": "≤",
    r"\ge": "≥",
    r"\;": " ",
    r"\,": " ",
    r"\!": "",
}


def _normalize_math_text(value: str) -> str:
    out = value.strip()
    # First flatten braced text-like commands while the command boundary is intact.
    out = re.sub(r"\\(?:mathcal|mathrm|text|operatorname)\{([^{}]+)\}", r"\1", out)
    for source in sorted(_MATH_REPLACEMENTS, key=len, reverse=True):
        out = out.replace(source, _MATH_REPLACEMENTS[source])
    out = out.replace(r"\{", "{").replace(r"\}", "}")
    out = out.replace("\\", "")
    return out


def _placement_ids_from_main() -> list[str]:
    ids: list[str] = []
    for path in t711.builder.MANUSCRIPT_FILES:
        for raw in path.read_text(encoding="utf-8").splitlines():
            if "Προτεινόμενη T-711" in raw:
                ids.extend(t711.builder.ASSET_RE.findall(raw))
    return ids


def _placement_ids_from_appendix() -> list[str]:
    ids: list[str] = []
    lines = t711.builder.APPENDIX_FILE.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped == "Προτεινόμενα assets:":
            i += 1
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                ids.extend(t711.builder.ASSET_RE.findall(lines[i]))
                i += 1
            continue
        if "Κύριο οπτικό asset:" in stripped:
            ids.extend(t711.builder.ASSET_RE.findall(stripped))
        i += 1
    return ids


def _mentioned_figure_cache_lines() -> list[str]:
    assets = t711.builder.load_assets()
    result: list[str] = []
    seen: set[str] = set()
    ordered_candidates = [
        *(('main', asset_id) for asset_id in _placement_ids_from_main()),
        *(('appendix', asset_id) for asset_id in _placement_ids_from_appendix()),
    ]
    for mode, asset_id in ordered_candidates:
        if asset_id in seen:
            continue
        asset = assets.get(asset_id)
        if not asset or asset.get("kind") != "figure":
            continue
        intended = set(asset.get("intended_use", []))
        if mode == "main" and "main-thesis" not in intended:
            continue
        if mode == "appendix" and "appendix" not in intended:
            continue
        seen.add(asset_id)
        result.append(f"Σχήμα {len(result) + 1} — {asset.get('caption') or asset_id}")
    return result


def _table_cache_lines() -> list[str]:
    result: list[str] = []
    sources = [(path, 'main') for path in t711.builder.MANUSCRIPT_FILES] + [(t711.builder.APPENDIX_FILE, 'appendix')]
    for path, mode in sources:
        md = t711._preprocess_markdown(path.read_text(encoding="utf-8"), mode)
        lines = md.splitlines()
        current = path.stem
        i = 0
        while i < len(lines):
            stripped = lines[i].strip()
            if stripped.startswith("#"):
                current = t711.builder.strip_markdown_inline(stripped.lstrip("#").strip())
            if stripped.startswith("|") and i + 1 < len(lines) and lines[i + 1].strip().startswith("|"):
                result.append(f"Πίνακας {len(result) + 1} — Σύνοψη για την ενότητα «{current}»")
                while i < len(lines) and lines[i].strip().startswith("|"):
                    i += 1
                continue
            i += 1
    return result


_original_enhanced_qa = t711._enhanced_qa


def _enhanced_qa(output: Path, qa_output: Path):
    _original_enhanced_qa(output, qa_output)
    report = json.loads(qa_output.read_text(encoding="utf-8"))
    doc = Document(output)
    full_text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
    corrupt_math = sorted({token for token in ("≤ftarrow", "≥q", "≤q", "ftarrow") if token in full_text})
    expected_figure_lines = _mentioned_figure_cache_lines()
    expected_table_lines = _table_cache_lines()
    report.update({
        "corrupt_math_tokens": corrupt_math,
        "cached_figure_entry_count": len(expected_figure_lines),
        "cached_table_entry_count": len(expected_table_lines),
    })
    if corrupt_math:
        report["status"] = "fail"
    qa_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if report["status"] != "pass":
        raise RuntimeError(f"T-711 v3 structural QA failed: {report}")


# Runtime global lookups in the v1 hardening functions make these targeted patches
# apply without duplicating or rewriting the underlying composition implementation.
t711._normalize_math_text = _normalize_math_text
t711._mentioned_figure_cache_lines = _mentioned_figure_cache_lines
t711._markdown_table_cache_lines = _table_cache_lines
t711._enhanced_qa = _enhanced_qa

if __name__ == "__main__":
    t711.builder.main()
