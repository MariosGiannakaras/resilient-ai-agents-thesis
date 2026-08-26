#!/usr/bin/env python3
"""Derive deterministic validated summaries from finalized experiment bundles."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from resilient_agents.analysis import write_analysis


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--analysis-id", required=True)
    parser.add_argument("--run-id", action="append", required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = write_analysis(
        repo_root=args.repo_root,
        analysis_id=args.analysis_id,
        run_ids=args.run_id,
    )
    print(
        json.dumps(
            {
                "analysis_dir": str(result.analysis_dir),
                "unit_count": result.unit_count,
                "sensitivity_record_count": result.sensitivity_record_count,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
