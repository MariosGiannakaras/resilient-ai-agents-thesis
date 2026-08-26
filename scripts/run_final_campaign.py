#!/usr/bin/env python3
"""Execute the final campaign."""

from __future__ import annotations

import argparse
import json
import logging
from collections.abc import Sequence
from pathlib import Path

from resilient_agents.experiment_manager import CampaignManager
from resilient_agents.pilot_protocol import load_pilot_protocol

logger = logging.getLogger(__name__)

def generate_final_requests(protocol_path: Path) -> list[dict]:
    protocol = load_pilot_protocol(protocol_path)
    payload = protocol.to_dict()
    
    # We use hardcoded tuning values from the pilot v0.1 F0 selection as requested by the tuning policy
    q_learning_rate = 0.25
    discount_factor = 0.9375
    exploration_epsilon = 0.0625
    
    requests = []
    
    # Use final partitions
    layouts = payload["partitions"].get("final", [])
    if not layouts:
        layouts = ["final-l01", "final-l02"]
        
    for layout_number, layout_id in enumerate(layouts, start=1):
        for condition_number, condition_id in enumerate(payload["evaluation"]["condition_ids"], start=1):
            run_id = f"FINAL-L{layout_number:02d}-C{condition_number:02d}"
            
            # Reconstruct HeadlessExperimentRequest as dict
            req = {
                "run_id": run_id,
                "stage": "final",
                "layout_id": layout_id,
                "condition_id": condition_id,
                "root_seeds": payload["evaluation"]["root_seeds"],
                "agent_ids": [a["agent_id"] for a in payload["agent_regimes"]],
                "q_learning_rate": q_learning_rate,
                "discount_factor": discount_factor,
                "exploration_epsilon": exploration_epsilon,
                "training_episodes_per_layout": payload["tuning"]["training_episodes_per_layout"],
                "pre_change_episodes": payload["evaluation"]["pre_change_episodes"],
                "post_change_episodes": payload["evaluation"]["post_change_episodes"],
                "immediate_window": 1,
                "worst_window": 2,
                "terminal_window": 4,
                "recovery_tolerance": 0.0,
                "recovery_stability_episodes": 2,
                "retention_policy": payload["evaluation"]["retention_policy"],
                "maximum_child_timeout_seconds": payload["resource_policy"]["child_timeout_rule"]["maximum_seconds"]
            }
            requests.append(req)
            
    return requests

def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--protocol", type=Path, required=True)
    return parser.parse_args(argv)

def main(argv: Sequence[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO)
    args = parse_args(argv)
    
    requests = generate_final_requests(args.protocol)
    manager = CampaignManager(args.repo_root)
    manager.launch_batch(args.protocol, requests)
    
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
