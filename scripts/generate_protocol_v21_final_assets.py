#!/usr/bin/env python3
"""Generate or verify the finalized protocol-v2.1 T-613 evidence assets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
if str(repo_root / "src") not in sys.path:
    sys.path.insert(0, str(repo_root / "src"))

from resilient_agents.evidence_v2.final_assets import (
    generate_final_assets,
    validate_final_assets,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--generate", action="store_true")
    mode.add_argument("--verify", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--generator-commit")
    args = parser.parse_args()
    if args.generate:
        if not args.generator_commit:
            parser.error("--generator-commit is required with --generate")
        result = generate_final_assets(repo_root, args.output, args.generator_commit)
    else:
        result = validate_final_assets(repo_root, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
