#!/usr/bin/env python3
"""Run protocol-v2.1 pre-final checks without authorizing final execution."""
from __future__ import annotations

import json
from pathlib import Path

from resilient_agents.study.pre_t610 import run_pre_t610_readiness_package


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    report = run_pre_t610_readiness_package(repo_root)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
