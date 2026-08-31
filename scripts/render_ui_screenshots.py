#!/usr/bin/env python3
"""Render deterministic PySide6 T-528 review screenshots in offscreen mode.

These screenshots are presentation QA artifacts, never scientific evidence. The
script reads frozen protocol metadata and DEVELOPMENT preview plans but does not
create, execute, resume or finalize any Study.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "0")

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from PySide6.QtCore import QSize  # noqa: E402

from resilient_agents.desktop.app import create_application  # noqa: E402
from resilient_agents.desktop.main_window import MainWindow  # noqa: E402


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def capture(window: MainWindow, output: Path, filename: str) -> dict[str, object]:
    app = create_application([])
    app.processEvents()
    image = window.grab()
    target = output / filename
    if not image.save(str(target), "PNG"):
        raise RuntimeError(f"failed to save screenshot: {target}")
    return {
        "file": filename,
        "width": image.width(),
        "height": image.height(),
        "sha256": sha256(target),
    }


def prepare_review(study) -> None:
    study.show_customize()
    study.customize.study_label.setText("GridWorld adaptation check")
    study.customize.root_count.setCurrentIndex(1)
    study.customize.layout_count.setCurrentIndex(1)
    study._show_review()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    app = create_application([])
    window = MainWindow(repo_root=REPO_ROOT)
    window.show()
    app.processEvents()

    records: list[dict[str, object]] = []
    study = window.study_page

    # Historical accepted references are 1480x920. Capture the key Study journey
    # states at this exact viewport so visual review is not confounded by size.
    window.resize(QSize(1480, 920))
    window.set_page(0)

    study.show_home()
    app.processEvents()
    records.append(capture(window, output, "reference-size-choose-study.png"))

    study.show_thesis()
    app.processEvents()
    records.append(capture(window, output, "reference-size-thesis-study.png"))

    study.show_exploratory()
    app.processEvents()
    records.append(capture(window, output, "reference-size-exploratory-models.png"))

    study.show_customize()
    app.processEvents()
    records.append(capture(window, output, "reference-size-exploratory-customize.png"))

    prepare_review(study)
    app.processEvents()
    records.append(capture(window, output, "reference-size-exploratory-review.png"))

    window.resize(QSize(1440, 900))
    window.set_page(0)
    study.show_home()
    app.processEvents()
    records.append(capture(window, output, "01-choose-study.png"))

    study.show_thesis()
    app.processEvents()
    records.append(capture(window, output, "02-thesis-study.png"))

    study.show_exploratory()
    app.processEvents()
    records.append(capture(window, output, "03-exploratory-models.png"))

    study.show_customize()
    app.processEvents()
    records.append(capture(window, output, "04-exploratory-customize.png"))

    prepare_review(study)
    app.processEvents()
    records.append(capture(window, output, "05-exploratory-review.png"))

    for index, filename in (
        (1, "06-runs-empty.png"),
        (2, "07-results-empty.png"),
        (3, "08-artifacts-empty.png"),
    ):
        window.set_page(index)
        app.processEvents()
        records.append(capture(window, output, filename))

    window.resize(QSize(1366, 768))
    window.set_page(0)
    study.show_home()
    app.processEvents()
    records.append(capture(window, output, "09-choose-study-1366x768.png"))

    study.show_exploratory()
    app.processEvents()
    records.append(capture(window, output, "10-exploratory-models-1366x768.png"))

    study.show_customize()
    app.processEvents()
    records.append(capture(window, output, "11-exploratory-customize-1366x768.png"))

    prepare_review(study)
    app.processEvents()
    records.append(capture(window, output, "12-exploratory-review-1366x768.png"))

    protocol_path = REPO_ROOT / "configs" / "protocols" / "protocol-v2.0-final.json"
    manifest = {
        "schema_version": 4,
        "purpose": "T-528 deterministic presentation review; not scientific evidence",
        "visual_reference_viewport": [1480, 920],
        "final_reserve_execution": "not-authorized-and-not-executed",
        "development_preview_only": True,
        "protocol_file_sha256": sha256(protocol_path),
        "screenshots": records,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    window.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
