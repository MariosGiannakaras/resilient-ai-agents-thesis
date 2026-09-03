#!/usr/bin/env python3
"""T-711 appendix-anchor compatibility layer.

The accepted Appendix Γ heading contains a descriptive suffix after the stable
"Παράρτημα Γ" prefix. v5 used an exact equality check. This wrapper changes only that
anchor lookup to prefix matching while preserving all v5 completeness/reference gates.
"""

from __future__ import annotations

import t711_build_entry_v5 as v5


t711 = v5.t711


def _find_anchor(lines: list[str], anchor: str, *, prefix: bool = False) -> int:
    for index, line in enumerate(lines):
        value = line.strip()
        if (prefix and value.startswith(anchor)) or (not prefix and value == anchor):
            return index
    raise ValueError(f"appendix placement anchor missing: {anchor}")


def _render_appendix(doc, md: str, cmap, assets, inserted, inserted_rq_tables):
    cleaned = v5._strip_appendix_handoff_lines(v5._previous_preprocess(md, "appendix"))
    lines = cleaned.splitlines()

    b1 = _find_anchor(lines, "### Β.1 RQ1")
    b2 = _find_anchor(lines, "### Β.2 RQ2")
    b3 = _find_anchor(lines, "### Β.3 RQ3")
    gamma = _find_anchor(lines, "## Παράρτημα Γ", prefix=True)
    if not (b1 < b2 < b3 < gamma):
        raise ValueError("appendix placement anchors are out of canonical order")

    v5._render_clean_chunk(doc, "\n".join(lines[:b2]), cmap, assets, inserted, inserted_rq_tables, False)
    v5._add_registered_figures(doc, v5.APPENDIX_GROUPS["### Β.1 RQ1"], assets, inserted)

    v5._render_clean_chunk(doc, "\n".join(lines[b2:b3]), cmap, assets, inserted, inserted_rq_tables, False)
    v5._add_registered_figures(doc, v5.APPENDIX_GROUPS["### Β.2 RQ2"], assets, inserted)

    v5._render_clean_chunk(doc, "\n".join(lines[b3:gamma]), cmap, assets, inserted, inserted_rq_tables, False)
    v5._add_registered_figures(doc, v5.APPENDIX_GROUPS["### Β.3 RQ3"], assets, inserted)

    remaining = lines[gamma:]
    gamma2 = _find_anchor(remaining, "### Γ.2 Frozen identities")
    v5._render_clean_chunk(doc, "\n".join(remaining[:gamma2]), cmap, assets, inserted, inserted_rq_tables, False)
    v5._add_registered_figures(doc, ["FIG-METHOD-028-LINEAGE"], assets, inserted)
    v5._render_clean_chunk(doc, "\n".join(remaining[gamma2:]), cmap, assets, inserted, inserted_rq_tables, False)


v5._render_appendix = _render_appendix


if __name__ == "__main__":
    t711.builder.main()
