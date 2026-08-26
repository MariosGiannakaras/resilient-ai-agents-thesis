#!/usr/bin/env python3
"""Execute or resume the complete predeclared pilot-v0.1 campaign."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from resilient_agents.pilot_campaign import execute_pilot_campaign
from resilient_agents.pilot_protocol import load_pilot_protocol


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--protocol", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    state_path = execute_pilot_campaign(
        repo_root=args.repo_root,
        protocol=load_pilot_protocol(args.protocol),
    )
    print(json.dumps({"campaign_state": str(state_path)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
