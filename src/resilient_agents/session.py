"""Whole-experiment lifecycle with exactly one optional Git publication."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .git_publish import PublishResult, publish_finalized_run
from .run_bundle import RunBundle


class ExperimentSession:
    def __init__(self, bundle: RunBundle) -> None:
        self.bundle = bundle
        self._finalized = False

    def record_event(self, payload: Mapping[str, Any]) -> None:
        self.bundle.append_event(payload)

    def record_trace(self, payload: Mapping[str, Any]) -> None:
        self.bundle.append_trace(payload)

    def finalize(
        self,
        *,
        status: str,
        summary: Mapping[str, Any],
        auto_publish: bool,
    ) -> tuple[Path, PublishResult | None]:
        if self._finalized:
            raise RuntimeError("experiment session is already finalized")
        run_dir = self.bundle.finalize(status=status, summary=summary)
        self._finalized = True
        publication = None
        if auto_publish:
            publication = publish_finalized_run(
                repo_root=self.bundle.repo_root, run_id=self.bundle.run_id
            )
        return run_dir, publication
