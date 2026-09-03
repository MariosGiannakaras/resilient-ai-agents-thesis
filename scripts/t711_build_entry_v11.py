#!/usr/bin/env python3
"""T-711 post-synthesis final artifact reconciliation.

v10 inserts the composition-only results synthesis after the inherited v9 QA report has
already captured the pre-insertion DOCX hash/paragraph count. This layer re-opens the
*final* saved DOCX and reconciles those metadata fields to the actual artifact bytes.
No document content or scientific data changes are made here.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from docx import Document

import t711_build_entry_v10 as v10


t711 = v10.t711
_previous_build = t711.builder.build


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _build(output: Path, qa_output: Path) -> None:
    _previous_build(output, qa_output)

    report = json.loads(qa_output.read_text(encoding="utf-8"))
    doc = Document(output)
    final_sha = _sha256(output)
    final_paragraph_count = len(doc.paragraphs)

    report.update(
        {
            "output_sha256": final_sha,
            "paragraph_count": final_paragraph_count,
            "post_synthesis_paragraph_count": final_paragraph_count,
            "final_artifact_metadata_reconciled": True,
        }
    )

    if (
        report.get("status") != "pass"
        or report.get("results_synthesis_infographic") is not True
        or report.get("inline_shape_count_after_synthesis") != 25
        or report.get("registered_asset_bytes_modified") is not False
        or report.get("scientific_values_modified") is not False
    ):
        report["status"] = "fail"

    qa_output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if report["status"] != "pass":
        raise RuntimeError(f"T-711 v11 final artifact reconciliation failed: {report}")


t711.builder.build = _build

if __name__ == "__main__":
    t711.builder.main()
