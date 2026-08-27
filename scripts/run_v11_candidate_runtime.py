#!/usr/bin/env python3
"""Run one protocol-v1.1 candidate experiment with read-only live telemetry."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from resilient_agents.runtime_observer import (
    ObservedV11CandidateRunner,
    RuntimeTelemetrySink,
)
from resilient_agents.v11_candidate_runner import V11CandidateExperimentRequest
from resilient_agents.v11_protocol import load_v11_candidate_protocol


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--telemetry", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        payload = json.loads(args.request.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read candidate runtime request: {args.request}") from exc
    request = V11CandidateExperimentRequest.from_dict(payload)
    result = ObservedV11CandidateRunner(
        repo_root=args.repo_root,
        protocol=load_v11_candidate_protocol(args.protocol),
        request=request,
        runtime_telemetry_sink=RuntimeTelemetrySink(args.telemetry),
    ).run()
    print(
        json.dumps(
            {
                "run_dir": str(result.run_dir),
                "publication_commit": result.publication_commit,
                "telemetry": str(args.telemetry),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
