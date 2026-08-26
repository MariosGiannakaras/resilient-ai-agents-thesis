#!/usr/bin/env python3
"""Execute one explicit headless experiment request without the dashboard."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from resilient_agents.experiment_runner import (
    HeadlessExperimentRequest,
    HeadlessExperimentRunner,
)
from resilient_agents.pilot_protocol import load_pilot_protocol


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--request", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        request_payload = json.loads(args.request.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read headless request: {args.request}") from exc
    request = HeadlessExperimentRequest.from_dict(request_payload)
    result = HeadlessExperimentRunner(
        repo_root=args.repo_root,
        protocol=load_pilot_protocol(args.protocol),
        request=request,
    ).run()
    print(
        json.dumps(
            {
                "run_dir": str(result.run_dir),
                "publication_commit": result.publication_commit,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
