"""Finalize or verify the predeclared T-612 protocol-v2.1 analysis."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Finalize or verify the T-612 protocol-v2.1 analysis package."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--finalize", action="store_true")
    mode.add_argument("--verify", action="store_true")
    parser.add_argument("--analysis-source-git-commit")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root / "src") not in sys.path:
        sys.path.insert(0, str(repo_root / "src"))

    from resilient_agents.evidence_v2.final_analysis import (
        finalize_protocol_v21_t612,
        verify_protocol_v21_t612,
    )

    if args.finalize:
        if not args.analysis_source_git_commit:
            parser.error("--finalize requires --analysis-source-git-commit")
        result = finalize_protocol_v21_t612(
            repo_root,
            analysis_source_git_commit=args.analysis_source_git_commit,
        )
    else:
        if args.analysis_source_git_commit:
            parser.error("--analysis-source-git-commit is only valid with --finalize")
        result = verify_protocol_v21_t612(repo_root)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
