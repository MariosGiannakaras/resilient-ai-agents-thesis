#!/usr/bin/env python3
"""T-715 appendix-heading compatibility fix.

The accepted T-714 preprocessing localizes appendix headings before the T-715 renderer
places registered diagnostics. Match semantic heading prefixes rather than the older
exact English/mixed-language heading strings. Scientific content and media are unchanged.
"""

from __future__ import annotations

import t711_build_entry_v21 as v21


v5 = v21.v5
t711 = v21.t711


def _find_exact(lines: list[str], value: str) -> int:
    for index, line in enumerate(lines):
        if line.strip() == value:
            return index
    raise ValueError(f"appendix placement anchor missing: {value}")


def _find_prefix(lines: list[str], prefix: str) -> int:
    for index, line in enumerate(lines):
        if line.strip().startswith(prefix):
            return index
    raise ValueError(f"appendix placement anchor missing: {prefix}*")


def _render_appendix_reader(doc, md: str, cmap, assets, inserted, inserted_rq_tables):
    cleaned = v5._strip_appendix_handoff_lines(v5._previous_preprocess(md, "appendix"))
    lines = cleaned.splitlines()

    b1 = _find_exact(lines, "### Β.1 RQ1")
    b2 = _find_exact(lines, "### Β.2 RQ2")
    b3 = _find_exact(lines, "### Β.3 RQ3")
    gamma = _find_prefix(lines, "## Παράρτημα Γ")

    v5._render_clean_chunk(
        doc, "\n".join(lines[:b1]), cmap, assets, inserted, inserted_rq_tables, False
    )
    v5._render_clean_chunk(
        doc,
        "### Β.0 Συμπληρωματικά αποτελέσματα ανάκαμψης\n\n"
        "Η ενότητα αυτή μεταφέρει από το κύριο κείμενο δύο εξειδικευμένα διαγνωστικά: "
        "τον χρόνο ανάκαμψης υπό συνθήκη επιτυχούς ανάκαμψης και την προκαθορισμένη "
        "ανάλυση ευαισθησίας. Χρησιμοποιούνται για πληρότητα και δεν αλλάζουν τα βασικά "
        "συμπεράσματα του Κεφαλαίου 5.",
        cmap,
        assets,
        inserted,
        inserted_rq_tables,
        False,
    )
    v5._add_registered_figures(
        doc,
        ["FIG-RQ3-019-CONDITIONAL", "FIG-RQ3-023-SENSITIVITY"],
        assets,
        inserted,
    )

    v5._render_clean_chunk(
        doc, "\n".join(lines[b1:b2]), cmap, assets, inserted, inserted_rq_tables, False
    )
    v5._add_registered_figures(
        doc, v5.APPENDIX_GROUPS["### Β.1 RQ1"], assets, inserted
    )

    v5._render_clean_chunk(
        doc, "\n".join(lines[b2:b3]), cmap, assets, inserted, inserted_rq_tables, False
    )
    v5._add_registered_figures(
        doc, v5.APPENDIX_GROUPS["### Β.2 RQ2"], assets, inserted
    )

    v5._render_clean_chunk(
        doc, "\n".join(lines[b3:gamma]), cmap, assets, inserted, inserted_rq_tables, False
    )
    v5._add_registered_figures(
        doc, v5.APPENDIX_GROUPS["### Β.3 RQ3"], assets, inserted
    )

    remaining = lines[gamma:]
    gamma2 = _find_prefix(remaining, "### Γ.2")
    v5._render_clean_chunk(
        doc,
        "\n".join(remaining[:gamma2]),
        cmap,
        assets,
        inserted,
        inserted_rq_tables,
        False,
    )
    v5._add_registered_figures(doc, ["FIG-METHOD-028-LINEAGE"], assets, inserted)
    v5._render_clean_chunk(
        doc,
        "\n".join(remaining[gamma2:]),
        cmap,
        assets,
        inserted,
        inserted_rq_tables,
        False,
    )


v5._render_appendix = _render_appendix_reader

if __name__ == "__main__":
    t711.builder.main()
