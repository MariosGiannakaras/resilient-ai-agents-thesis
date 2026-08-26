#!/usr/bin/env python3
"""Execute the final campaign using the frozen protocol and validated tuning selection.

Scientific configuration is resolved entirely from the authoritative frozen
protocol and the pilot campaign's validated tuning-selection evidence.  No
scientific parameter is hardcoded in this launcher.

This script enforces the lifecycle gate: final-stage execution requires
explicit opt-in via --allow-final.  Without it, the launcher refuses to
proceed, protecting the uncontaminated final-reserve partition.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from collections.abc import Sequence
from pathlib import Path

logger = logging.getLogger(__name__)


def _load_selected_configuration(repo_root: Path) -> dict[str, float]:
    """Resolve the validated tuning selection from pilot campaign evidence.

    Reads the canonical campaign-state.json (pilot-v0.2 amended campaign)
    and extracts the 'selected.configuration' that was determined through
    the staged-dyadic tuning procedure.

    Raises ValueError if the evidence is missing or malformed.
    """
    # Try amended campaign first, then original
    for campaign_dir in ("pilot-v0.2", "pilot-v0.1"):
        state_path = (
            repo_root / "results" / "campaigns" / campaign_dir / "campaign-state.json"
        )
        if state_path.exists():
            state = json.loads(state_path.read_text(encoding="utf-8"))
            selected = state.get("tuning", {}).get("selected", {})
            config = selected.get("configuration", {})
            if all(
                key in config
                for key in ("learning_rate", "discount_factor", "exploration_epsilon")
            ):
                return {
                    "learning_rate": float(config["learning_rate"]),
                    "discount_factor": float(config["discount_factor"]),
                    "exploration_epsilon": float(config["exploration_epsilon"]),
                }

    raise ValueError(
        "Cannot resolve tuning selection: no valid campaign-state.json found "
        "with a selected configuration in results/campaigns/"
    )


def generate_final_requests(
    protocol_path: Path, repo_root: Path
) -> list[dict]:
    """Build the complete final evaluation request matrix.

    All scientific parameters are resolved from the frozen protocol and
    validated tuning evidence — nothing is hardcoded.
    """
    from resilient_agents.pilot_protocol import load_pilot_protocol

    protocol = load_pilot_protocol(protocol_path)
    payload = protocol.to_dict()

    if payload.get("status") != "frozen":
        raise ValueError(
            f"Protocol status is {payload.get('status')!r}; "
            "final campaign requires a frozen protocol"
        )

    # Resolve tuning configuration from evidence
    tuning_config = _load_selected_configuration(repo_root)
    logger.info(
        "Resolved tuning configuration: lr=%.4f, gamma=%.5f, eps=%.4f",
        tuning_config["learning_rate"],
        tuning_config["discount_factor"],
        tuning_config["exploration_epsilon"],
    )

    evaluation = payload["evaluation"]
    metric_sensitivity = payload["metric_sensitivity"]
    agent_ids = [a["agent_id"] for a in payload["agent_regimes"]]
    layouts = payload["partitions"].get("final", [])
    if not layouts:
        raise ValueError("Protocol has no final partition layouts")

    requests = []
    for layout_number, layout_id in enumerate(layouts, start=1):
        for condition_number, condition_id in enumerate(
            evaluation["condition_ids"], start=1
        ):
            run_id = f"FINAL-L{layout_number:02d}-C{condition_number:02d}"

            req: dict = {
                "run_id": run_id,
                "stage": "final",
                "layout_id": layout_id,
                "condition_id": condition_id,
                "root_seeds": evaluation["root_seeds"],
                "agent_ids": agent_ids,
                "q_learning_rate": tuning_config["learning_rate"],
                "discount_factor": tuning_config["discount_factor"],
                "exploration_epsilon": tuning_config["exploration_epsilon"],
                "training_episodes_per_layout": payload["tuning"][
                    "training_episodes_per_layout"
                ],
                "pre_change_episodes": evaluation["pre_change_episodes"],
                "post_change_episodes": evaluation["post_change_episodes"],
                # Metric sensitivity: use the first value from each
                # predeclared list (the protocol's primary setting)
                "immediate_window": metric_sensitivity["immediate_windows"][0],
                "worst_window": metric_sensitivity["worst_windows"][0],
                "terminal_window": metric_sensitivity["terminal_windows"][0],
                "recovery_tolerance": metric_sensitivity[
                    "recovery_tolerances_step_reward_units"
                ][0],
                "recovery_stability_episodes": metric_sensitivity[
                    "recovery_stability_episodes"
                ][0],
                "retention_policy": evaluation["retention_policy"],
                "auto_publish": True,
                "execution_timeout_seconds": 3600,
            }
            requests.append(req)

    return requests


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument(
        "--allow-final",
        action="store_true",
        help=(
            "Explicitly allow final-stage execution. Without this flag, "
            "the launcher refuses to proceed, protecting the final reserve."
        ),
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO)
    args = parse_args(argv)

    if not args.allow_final:
        logger.error(
            "Final campaign execution requires --allow-final. "
            "This gate protects the uncontaminated final-reserve partition. "
            "Do not use --allow-final until T-511 acceptance is satisfied."
        )
        return 1

    from resilient_agents.experiment_manager import CampaignManager

    requests = generate_final_requests(args.protocol, args.repo_root)
    logger.info("Generated %d final evaluation requests.", len(requests))

    manager = CampaignManager(args.repo_root)
    manager.launch_batch(args.protocol, requests)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
