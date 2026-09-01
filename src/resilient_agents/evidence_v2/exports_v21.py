"""Protocol-v2.1 deterministic evidence export adapter.

The v2 table layouts remain valid for DEC-060; only the scientific recipe
identity and interval policy changed.  This adapter reuses the frozen v2 CSV
serialization, then writes a v2.1 manifest rather than mislabelling the package
as the older analysis recipe.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from .analysis_v21 import V21_ANALYSIS_RECIPE
from .exports import StudyExportEngine, _write_json_atomic


class StudyExportEngineV21:
    """Export the v2 table set while retaining protocol-v2.1 provenance."""

    def export(
        self,
        *,
        analysis_package: Mapping[str, Any],
        specification: Mapping[str, Any],
        output_dir: Path,
        source_analysis_artifact_id: str,
        source_analysis_sha256: str,
    ) -> dict[str, Any]:
        package = deepcopy(dict(analysis_package))
        if package.get("schema_version") != 2:
            raise ValueError("protocol-v2.1 export requires analysis package schema_version=2")
        if package.get("analysis_recipe") != V21_ANALYSIS_RECIPE:
            raise ValueError("protocol-v2.1 export requires the v2.1 analysis recipe")
        if not isinstance(package.get("interval_policy"), Mapping):
            raise ValueError("protocol-v2.1 export requires explicit interval_policy provenance")

        delegated = deepcopy(package)
        delegated["analysis_recipe"] = "protocol-v2-root-level-v2"
        exported = StudyExportEngine().export(
            analysis_package=delegated,
            specification=specification,
            output_dir=output_dir,
            source_analysis_artifact_id=source_analysis_artifact_id,
            source_analysis_sha256=source_analysis_sha256,
        )
        manifest = dict(exported["manifest"])
        manifest["analysis_recipe"] = V21_ANALYSIS_RECIPE
        manifest["protocol_extension"] = "v2.1-recovery-comparisons"
        manifest["interval_policy"] = deepcopy(package["interval_policy"])
        manifest_path = Path(exported["manifest_path"])
        manifest_sha = _write_json_atomic(manifest_path, manifest)
        return {
            **exported,
            "manifest": manifest,
            "manifest_path": manifest_path,
            "manifest_sha256": manifest_sha,
        }
