#!/usr/bin/env python3
"""Focused T-534 exact-matched Phase-B render validation without execution."""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "0")

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from PySide6.QtCore import QSize  # noqa: E402

from resilient_agents.desktop.app import create_application  # noqa: E402
from resilient_agents.desktop.exploratory_study import DesktopExploratoryStudyModel  # noqa: E402
from resilient_agents.desktop.main_window import MainWindow  # noqa: E402
from render_ui_screenshots import capture, write_phase_b_pair_fixture  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="t534-ui-pair-") as directory:
        writable_root = Path(directory).resolve()
        study_id = "t534-dev-ui-review-pair"
        DesktopExploratoryStudyModel(repo_root=REPO_ROOT, writable_root=writable_root).create(
            selected_method_ids=("q_learning",), root_count=1, layout_count=1,
            study_label="Matched presentation QA", study_id=study_id,
        )
        write_phase_b_pair_fixture(writable_root=writable_root, study_id=study_id)
        if (writable_root / "results" / "runs").exists():
            raise RuntimeError("pair fixture unexpectedly executed a scientific run")

        app = create_application([])
        window = MainWindow(repo_root=REPO_ROOT, writable_root=writable_root)
        window.show()
        window.set_page(1)
        window.runs_page.refresh()
        window.runs_page.study_combo.setCurrentIndex(window.runs_page.study_combo.findData(study_id))
        window.runs_page.refresh_live()
        frame = window.runs_page._latest_frame
        if frame is None or frame.comparison is None:
            raise RuntimeError("exact FD/AD comparison was not exposed")
        pair = frame.comparison
        if (
            pair.frozen.method_id != pair.adaptive.method_id
            or pair.frozen.root_id != pair.adaptive.root_id
            or pair.frozen.layout_id != pair.adaptive.layout_id
            or pair.frozen.interaction_index != pair.adaptive.interaction_index
        ):
            raise RuntimeError("render attempted with a mismatched Phase-B pair")

        records = []
        for size, suffix in ((QSize(1440, 900), "1440x900"), (QSize(1366, 768), "1366x768")):
            window.resize(size)
            app.processEvents()
            records.append(capture(window, output, f"phase-b-exact-pair-{suffix}.png"))
        (output / "matched-resilience-manifest.json").write_text(
            json.dumps({
                "schema_version": 2,
                "purpose": "T-534 exact matched Phase-B presentation QA; not scientific evidence",
                "scientific_jobs_executed": 0,
                "environment_steps_executed": 0,
                "final_reserve_accessed": False,
                "pairing": "exact method/root/layout/interaction FD/AD transient presentation",
                "screenshots": records,
            }, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        window.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
