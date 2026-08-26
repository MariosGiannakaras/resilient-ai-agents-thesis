"""Run the bounded native-machine T-210 parity benchmark."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import inspect
import json
import platform
import statistics
import subprocess
import time
from pathlib import Path
from typing import Any

from prototypes.gridworld import candidates
from prototypes.gridworld.candidates import (
    Action,
    CustomGymnasiumPrototype,
    MiniGridPrototype,
    PrototypeResearchAdapter,
    scenario_json,
)
from prototypes.gridworld.fixtures import fixture_seeds, prototype_fixture


def _source_lines(*objects: Any) -> int:
    lines = []
    for object_ in objects:
        lines.extend(inspect.getsource(object_).splitlines())
    return sum(1 for line in lines if line.strip() and not line.lstrip().startswith("#"))


def _git(command: str) -> str:
    return subprocess.run(
        ["git", *command.split()],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    ).stdout.strip()


def _benchmark(candidate_type, *, episodes: int, repeats: int) -> dict[str, Any]:
    spec = prototype_fixture(
        action_failure_probability=0.0,
        observation_corruption_probability=0.0,
        max_steps=6,
        include_change=True,
    )
    seeds = fixture_seeds(action_disturbance=1, observation_disturbance=3)
    actions = (Action.RIGHT, Action.RIGHT, Action.RIGHT, Action.RIGHT)
    samples: list[float] = []
    transition_count = episodes * len(actions)
    for _ in range(repeats):
        candidate = candidate_type(spec)
        adapter = PrototypeResearchAdapter(candidate)
        started = time.perf_counter_ns()
        try:
            for _ in range(episodes):
                adapter.reset(seeds=seeds)
                final = None
                for action in actions:
                    final = adapter.step(action)
                if final is None or not final.terminated or final.truncated:
                    raise RuntimeError("benchmark fixture did not terminate as expected")
        finally:
            candidate.close()
        elapsed = time.perf_counter_ns() - started
        samples.append(elapsed / transition_count)
    return {
        "episodes_per_repeat": episodes,
        "repeats": repeats,
        "transitions_per_repeat": transition_count,
        "nanoseconds_per_transition": {
            "median": round(statistics.median(samples), 1),
            "minimum": round(min(samples), 1),
            "maximum": round(max(samples), 1),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, required=True)
    parser.add_argument("--repeats", type=int, required=True)
    args = parser.parse_args()
    if args.episodes <= 0 or args.repeats <= 0:
        raise SystemExit("episodes and repeats must be positive")

    spec = prototype_fixture(
        action_failure_probability=0.0,
        observation_corruption_probability=0.0,
        max_steps=6,
        include_change=True,
    )
    root = Path(__file__).resolve().parents[2]
    report = {
        "schema_version": 1,
        "purpose": "T-210 prototype feasibility benchmark; not experiment evidence",
        "source_commit": _git("rev-parse HEAD"),
        "source_dirty": bool(_git("status --porcelain --untracked-files=no")),
        "system": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "processor": platform.processor(),
        },
        "packages": {
            "gymnasium": importlib.metadata.version("gymnasium"),
            "minigrid": importlib.metadata.version("minigrid"),
        },
        "fixture_sha256": hashlib.sha256(scenario_json(spec).encode("utf-8")).hexdigest(),
        "fixture_seeds_are_test_only": True,
        "candidate_owned_source_lines": {
            "shared_harness": _source_lines(
                candidates.ResolvedPrototypeScenario,
                candidates._BasePrototype,
                candidates.PrototypeResearchAdapter,
            ),
            "custom_gymnasium": _source_lines(
                candidates._CustomMechanics,
                candidates.CustomGymnasiumPrototype,
            ),
            "minigrid_adaptation": _source_lines(
                candidates._FixtureMiniGridEnv,
                candidates._MiniGridMechanics,
                candidates.MiniGridPrototype,
            ),
        },
        "benchmarks": {
            "custom_gymnasium": _benchmark(
                CustomGymnasiumPrototype,
                episodes=args.episodes,
                repeats=args.repeats,
            ),
            "minigrid_adaptation": _benchmark(
                MiniGridPrototype,
                episodes=args.episodes,
                repeats=args.repeats,
            ),
        },
        "repository_root": str(root),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
