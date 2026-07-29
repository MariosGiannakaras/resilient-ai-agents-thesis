#!/usr/bin/env python3
"""Download the curated open-access related-work bibliography.

This script downloads only direct URLs listed as openly accessible in
bibliography/SOURCE_ACQUISITION_WORKFLOW.md. It does not bypass paywalls.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tempfile
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Final
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


REPOSITORY_ROOT: Final[Path] = Path(__file__).resolve().parents[1]
ORIGINAL_DIR: Final[Path] = REPOSITORY_ROOT / "bibliography" / "original"
MANIFEST_PATH: Final[Path] = REPOSITORY_ROOT / "bibliography" / "source_manifest.json"
USER_AGENT: Final[str] = "resilient-ai-agents-thesis/1.0 literature-acquisition"
TIMEOUT_SECONDS: Final[int] = 60
MAX_ATTEMPTS: Final[int] = 3


@dataclass(frozen=True)
class Source:
    source_id: str
    local_subdir: str
    filename: str
    title: str
    authors: str
    year: int
    publication_status: str
    source_url: str
    access_note: str


SOURCES: Final[tuple[Source, ...]] = (
    Source("SRC-RW-001", "related-work", "balloch_2022_novgrid.pdf", "NovGrid: A Flexible Grid World for Evaluating Agent Response to Novelty", "Jonathan Balloch et al.", 2022, "AAAI Spring Symposium paper / arXiv preprint", "https://arxiv.org/pdf/2203.12117", "Public author preprint"),
    Source("SRC-RW-002", "related-work", "leike_2017_ai_safety_gridworlds.pdf", "AI Safety Gridworlds", "Jan Leike et al.", 2017, "Research paper / arXiv preprint", "https://arxiv.org/pdf/1711.09883", "Public author preprint"),
    Source("SRC-RW-003", "related-work", "benjamins_2021_carl.pdf", "CARL: A Benchmark for Contextual and Adaptive Reinforcement Learning", "Carolin Benjamins et al.", 2021, "NeurIPS workshop paper / arXiv preprint", "https://arxiv.org/pdf/2110.02102", "Public author preprint"),
    Source("SRC-RW-004", "related-work", "sutton_1990_dyna.pdf", "Integrated Modeling and Control Based on Reinforcement Learning and Dynamic Programming", "Richard S. Sutton", 1990, "NeurIPS proceedings paper", "https://papers.nips.cc/paper_files/paper/1990/file/d9fc5b73a8d78fad3d6dffe419384e70-Paper.pdf", "Official proceedings PDF"),
    Source("SRC-RW-005", "related-work", "steinparz_2022_reactive_exploration.pdf", "Reactive Exploration to Cope With Non-Stationarity in Lifelong Reinforcement Learning", "Christian Alexander Steinparz et al.", 2022, "PMLR conference paper", "https://proceedings.mlr.press/v199/steinparz22a/steinparz22a.pdf", "Official PMLR PDF"),
    Source("SRC-RW-006", "related-work", "cheung_2020_nonstationary_mdp.pdf", "Reinforcement Learning for Non-Stationary Markov Decision Processes: The Blessing of (More) Optimism", "Wang Chi Cheung, David Simchi-Levi, Ruihao Zhu", 2020, "ICML / PMLR conference paper", "https://proceedings.mlr.press/v119/cheung20a/cheung20a.pdf", "Official PMLR PDF"),
    Source("SRC-RW-007", "related-work", "wei_luo_2021_nonstationary_blackbox.pdf", "Non-stationary Reinforcement Learning without Prior Knowledge: an Optimal Black-box Approach", "Chen-Yu Wei, Haipeng Luo", 2021, "COLT / PMLR conference paper", "https://proceedings.mlr.press/v134/wei21b/wei21b.pdf", "Official PMLR PDF"),
    Source("SRC-RW-008", "related-work", "de_la_rosa_2025_morphin.pdf", "Adapting the Behavior of Reinforcement Learning Agents to Changing Action Spaces and Reward Functions", "Raul de la Rosa, Ivana Dusparic, Nicolas Cardozo", 2025, "IEEE ACSOS Companion paper / arXiv author preprint", "https://arxiv.org/pdf/2601.20714", "Public author preprint"),
    Source("SRC-RW-010", "related-work", "alami_2023_change_point_detection.pdf", "Restarted Bayesian Online Change-point Detection for Non-Stationary Markov Decision Processes", "Reda Alami, Mohammed Mahfoud, Eric Moulines", 2023, "CoLLAs / PMLR conference paper", "https://proceedings.mlr.press/v232/alami23a/alami23a.pdf", "Official PMLR PDF"),
    Source("SRC-RW-011", "related-work", "tessler_2019_action_robust_rl.pdf", "Action Robust Reinforcement Learning and Applications in Continuous Control", "Chen Tessler, Yonathan Efroni, Shie Mannor", 2019, "Research paper / arXiv preprint", "https://arxiv.org/pdf/1901.09184", "Public author preprint"),
    Source("SRC-RW-012", "related-work", "zhang_2020_state_adversarial_mdp.pdf", "Robust Deep Reinforcement Learning against Adversarial Perturbations on State Observations", "Huan Zhang et al.", 2020, "Research paper / arXiv preprint", "https://arxiv.org/pdf/2003.08938", "Public author preprint"),
    Source("SRC-RW-013", "related-work", "peng_2024_complexity_nonstationary_rl.pdf", "The Complexity of Non-Stationary Reinforcement Learning", "Binghui Peng, Christos Papadimitriou", 2024, "ALT / PMLR conference paper", "https://proceedings.mlr.press/v237/peng24a/peng24a.pdf", "Official PMLR PDF"),
    Source("SRC-THESIS-001", "theses", "balloch_2024_sudden_environmental_change_dissertation.pdf", "Efficient Adaptation of Reinforcement Learning Agents to Sudden Environmental Change", "Jonathan Clifford Balloch", 2024, "Georgia Tech PhD dissertation / open manuscript", "https://arxiv.org/pdf/2505.10330", "Public manuscript; verify against institutional record https://hdl.handle.net/1853/76967"),
    Source("SRC-THESIS-002", "theses", "liu_2024_nonstationary_rl_thesis.pdf", "Deep Reinforcement Learning in Non-Stationary Environments", "Zihe Liu", 2024, "University of Technology Sydney thesis", "https://opus.lib.uts.edu.au/bitstream/10453/186408/1/thesis.pdf", "Official open institutional thesis"),
)

MANUAL_ACQUISITION: Final[tuple[dict[str, str], ...]] = (
    {"source_id": "SRC-RW-009", "title": "Adapt to Environment Sudden Changes by Learning a Context Sensitive Policy", "official_url": "https://doi.org/10.1609/aaai.v36i7.20730", "instruction": "Download from the official AAAI page or a lawful author copy if automated retrieval is unavailable."},
    {"source_id": "SRC-THESIS-003", "title": "Reinforcement Learning Approach for Inspect/Correct Tasks", "official_url": "https://doi.org/10.31390/gradschool_dissertations.5431", "instruction": "Use the official LSU repository download and record its license/version."},
    {"source_id": "SRC-THESIS-004", "title": "Adaptive Reinforcement Learning: Lean and Dynamic Agents for Robust Generalization", "official_url": "https://research.tue.nl/en/publications/adaptive-reinforcement-learning-lean-and-dynamic-agents-for-robus/", "instruction": "Follow the official TU/e open-access document link and record its license/version."},
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_pdf(path: Path) -> None:
    if path.stat().st_size < 1024:
        raise ValueError(f"Downloaded file is unexpectedly small: {path.stat().st_size} bytes")
    with path.open("rb") as handle:
        if handle.read(5) != b"%PDF-":
            raise ValueError("Downloaded content is not a PDF")


def download(source: Source, destination: Path) -> None:
    request = Request(source.source_url, headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        temporary_path: Path | None = None
        try:
            with urlopen(request, timeout=TIMEOUT_SECONDS) as response:  # noqa: S310
                with tempfile.NamedTemporaryFile(mode="wb", delete=False, dir=destination.parent, suffix=".partial") as temporary:
                    shutil.copyfileobj(response, temporary)
                    temporary_path = Path(temporary.name)
            validate_pdf(temporary_path)
            os.replace(temporary_path, destination)
            return
        except (HTTPError, URLError, TimeoutError, ValueError, OSError) as error:
            last_error = error
            try:
                if temporary_path is not None and temporary_path.exists():
                    temporary_path.unlink()
            except OSError:
                pass
            if attempt < MAX_ATTEMPTS:
                time.sleep(attempt * 2)
    raise RuntimeError(f"Failed after {MAX_ATTEMPTS} attempts: {last_error}")


def load_manifest() -> dict[str, object]:
    if not MANIFEST_PATH.exists():
        return {"schema_version": 1, "sources": [], "manual_acquisition": []}
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as error:
        raise RuntimeError(f"Cannot read existing manifest: {error}") from error
    if not isinstance(manifest, dict):
        raise RuntimeError("Source manifest must contain a JSON object")
    return manifest


def records_by_id(value: object) -> dict[str, dict[str, object]]:
    if not isinstance(value, list):
        return {}
    return {str(record["source_id"]): record for record in value if isinstance(record, dict) and record.get("source_id")}


def quarantine(path: Path, reason: str) -> Path:
    suffix = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    target = path.with_name(f"{path.name}.{reason}.{suffix}.quarantine")
    counter = 1
    while target.exists():
        target = path.with_name(f"{path.name}.{reason}.{suffix}.{counter}.quarantine")
        counter += 1
    path.replace(target)
    return target


def prepare_source_file(source: Source, destination: Path, previous: dict[str, object] | None) -> tuple[str, bool]:
    """Return the verified checksum and whether new bytes were downloaded."""
    if not destination.exists():
        print(f"  downloading {source.source_url}")
        download(source, destination)
        return sha256_file(destination), True
    validate_pdf(destination)
    current_checksum = sha256_file(destination)
    previous_checksum = str(previous.get("sha256")) if previous and previous.get("sha256") else None
    if previous_checksum and current_checksum == previous_checksum:
        print("  using existing PDF verified against manifest checksum")
        return current_checksum, False
    reason = "checksum-mismatch" if previous_checksum else "untracked"
    quarantined = quarantine(destination, reason)
    print(f"  quarantined existing PDF: {quarantined.name}")
    print(f"  downloading authoritative copy from {source.source_url}")
    download(source, destination)
    return sha256_file(destination), True


def merged_manual_acquisition(manifest: dict[str, object]) -> list[dict[str, object]]:
    existing = records_by_id(manifest.get("manual_acquisition"))
    merged: list[dict[str, object]] = []
    known_ids: set[str] = set()
    for default in MANUAL_ACQUISITION:
        source_id = default["source_id"]
        known_ids.add(source_id)
        merged.append({**default, **existing.get(source_id, {})})
    merged.extend(record for source_id, record in existing.items() if source_id not in known_ids)
    return merged


def main() -> int:
    ORIGINAL_DIR.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    existing_records = records_by_id(manifest.get("sources"))
    curated_ids = {source.source_id for source in SOURCES}
    failures: list[dict[str, str]] = []
    records: list[dict[str, object]] = []
    for source in SOURCES:
        destination_dir = ORIGINAL_DIR / source.local_subdir
        destination_dir.mkdir(parents=True, exist_ok=True)
        destination = destination_dir / source.filename
        previous = existing_records.get(source.source_id)
        print(f"[{source.source_id}] {source.title}")
        try:
            checksum, downloaded_now = prepare_source_file(source, destination, previous)
            same_revision = bool(previous and previous.get("sha256") == checksum)
            retrieved_at = str(previous.get("retrieved_at_utc")) if same_revision and previous and previous.get("retrieved_at_utc") else utc_now()
            record = {
                **asdict(source),
                "local_path": destination.relative_to(REPOSITORY_ROOT).as_posix(),
                "sha256": checksum,
                "bytes": destination.stat().st_size,
                "retrieved_at_utc": retrieved_at,
                "full_text_review_complete": bool(same_revision and previous and previous.get("full_text_review_complete", False)),
            }
            records.append(record)
            action = "downloaded" if downloaded_now else "verified"
            print(f"  {action}: {destination.name} sha256={checksum}")
        except Exception as error:
            failures.append({"source_id": source.source_id, "error": str(error)})
            print(f"  ERROR: {error}", file=sys.stderr)
    records.extend(record for source_id, record in existing_records.items() if source_id not in curated_ids)
    output = {
        "schema_version": 1,
        "generated_at_utc": utc_now(),
        "policy": "Lawful open-access, author-provided or institutional sources only; no paywall bypass.",
        "sources": records,
        "failures": failures,
        "manual_acquisition": merged_manual_acquisition(manifest),
    }
    MANIFEST_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Manifest written to {MANIFEST_PATH.relative_to(REPOSITORY_ROOT)}")
    if failures:
        print(f"Completed with {len(failures)} failure(s).", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
