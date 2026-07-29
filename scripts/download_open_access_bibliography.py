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
TARGET_DIR: Final[Path] = REPOSITORY_ROOT / "bibliography" / "original" / "related-work"
MANIFEST_PATH: Final[Path] = REPOSITORY_ROOT / "bibliography" / "source_manifest.json"
USER_AGENT: Final[str] = "resilient-ai-agents-thesis/1.0 literature-acquisition"
TIMEOUT_SECONDS: Final[int] = 60
MAX_ATTEMPTS: Final[int] = 3


@dataclass(frozen=True)
class Source:
    source_id: str
    filename: str
    title: str
    authors: str
    year: int
    publication_status: str
    source_url: str
    access_note: str


SOURCES: Final[tuple[Source, ...]] = (
    Source(
        "SRC-RW-001",
        "balloch_2022_novgrid.pdf",
        "NovGrid: A Flexible Grid World for Evaluating Agent Response to Novelty",
        "Jonathan Balloch et al.",
        2022,
        "AAAI Spring Symposium paper / arXiv preprint",
        "https://arxiv.org/pdf/2203.12117",
        "Public author preprint",
    ),
    Source(
        "SRC-RW-002",
        "leike_2017_ai_safety_gridworlds.pdf",
        "AI Safety Gridworlds",
        "Jan Leike et al.",
        2017,
        "Research paper / arXiv preprint",
        "https://arxiv.org/pdf/1711.09883",
        "Public author preprint",
    ),
    Source(
        "SRC-RW-003",
        "benjamins_2021_carl.pdf",
        "CARL: A Benchmark for Contextual and Adaptive Reinforcement Learning",
        "Carolin Benjamins et al.",
        2021,
        "NeurIPS workshop paper / arXiv preprint",
        "https://arxiv.org/pdf/2110.02102",
        "Public author preprint",
    ),
    Source(
        "SRC-RW-004",
        "sutton_1990_dyna.pdf",
        "Integrated Modeling and Control Based on Reinforcement Learning and Dynamic Programming",
        "Richard S. Sutton",
        1990,
        "NeurIPS proceedings paper",
        "https://papers.nips.cc/paper_files/paper/1990/file/d9fc5b73a8d78fad3d6dffe419384e70-Paper.pdf",
        "Official proceedings PDF",
    ),
    Source(
        "SRC-RW-005",
        "steinparz_2022_reactive_exploration.pdf",
        "Reactive Exploration to Cope With Non-Stationarity in Lifelong Reinforcement Learning",
        "Christian Alexander Steinparz et al.",
        2022,
        "PMLR conference paper",
        "https://proceedings.mlr.press/v199/steinparz22a/steinparz22a.pdf",
        "Official PMLR PDF",
    ),
    Source(
        "SRC-RW-006",
        "cheung_2020_nonstationary_mdp.pdf",
        "Reinforcement Learning for Non-Stationary Markov Decision Processes: The Blessing of (More) Optimism",
        "Wang Chi Cheung, David Simchi-Levi, Ruihao Zhu",
        2020,
        "ICML / PMLR conference paper",
        "https://proceedings.mlr.press/v119/cheung20a/cheung20a.pdf",
        "Official PMLR PDF",
    ),
    Source(
        "SRC-RW-007",
        "wei_luo_2021_nonstationary_blackbox.pdf",
        "Non-stationary Reinforcement Learning without Prior Knowledge: an Optimal Black-box Approach",
        "Chen-Yu Wei, Haipeng Luo",
        2021,
        "COLT / PMLR conference paper",
        "https://proceedings.mlr.press/v134/wei21b/wei21b.pdf",
        "Official PMLR PDF",
    ),
    Source(
        "SRC-RW-008",
        "de_la_rosa_2025_morphin.pdf",
        "Adapting the Behavior of Reinforcement Learning Agents to Changing Action Spaces and Reward Functions",
        "Raul de la Rosa, Ivana Dusparic, Nicolas Cardozo",
        2025,
        "IEEE ACSOS Companion paper / arXiv author preprint",
        "https://arxiv.org/pdf/2601.20714",
        "Public author preprint",
    ),
)


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
        try:
            with urlopen(request, timeout=TIMEOUT_SECONDS) as response:  # noqa: S310
                with tempfile.NamedTemporaryFile(
                    mode="wb", delete=False, dir=destination.parent, suffix=".partial"
                ) as temporary:
                    shutil.copyfileobj(response, temporary)
                    temporary_path = Path(temporary.name)

            validate_pdf(temporary_path)
            os.replace(temporary_path, destination)
            return
        except (HTTPError, URLError, TimeoutError, ValueError, OSError) as error:
            last_error = error
            try:
                if "temporary_path" in locals() and temporary_path.exists():
                    temporary_path.unlink()
            except OSError:
                pass
            if attempt < MAX_ATTEMPTS:
                time.sleep(attempt * 2)

    raise RuntimeError(f"Failed after {MAX_ATTEMPTS} attempts: {last_error}")


def load_manifest() -> dict[str, object]:
    if not MANIFEST_PATH.exists():
        return {"schema_version": 1, "sources": []}
    try:
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as error:
        raise RuntimeError(f"Cannot read existing manifest: {error}") from error


def main() -> int:
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    existing_records = {
        record.get("source_id"): record
        for record in manifest.get("sources", [])
        if isinstance(record, dict)
    }

    failures: list[dict[str, str]] = []
    records: list[dict[str, object]] = []

    for source in SOURCES:
        destination = TARGET_DIR / source.filename
        print(f"[{source.source_id}] {source.title}")
        try:
            if destination.exists():
                validate_pdf(destination)
                print("  using existing valid PDF")
            else:
                print(f"  downloading {source.source_url}")
                download(source, destination)

            checksum = sha256_file(destination)
            record = {
                **asdict(source),
                "local_path": destination.relative_to(REPOSITORY_ROOT).as_posix(),
                "sha256": checksum,
                "bytes": destination.stat().st_size,
                "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                "full_text_review_complete": bool(
                    existing_records.get(source.source_id, {}).get(
                        "full_text_review_complete", False
                    )
                ),
            }
            records.append(record)
            print(f"  ok: {destination.name} sha256={checksum}")
        except Exception as error:  # Continue so all failures are reported together.
            failures.append({"source_id": source.source_id, "error": str(error)})
            print(f"  ERROR: {error}", file=sys.stderr)

    output = {
        "schema_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "policy": "Lawful open-access or author-provided sources only; no paywall bypass.",
        "sources": records,
        "failures": failures,
        "manual_acquisition": [
            {
                "source_id": "SRC-RW-009",
                "title": "Adapt to Environment Sudden Changes by Learning a Context Sensitive Policy",
                "official_url": "https://doi.org/10.1609/aaai.v36i7.20730",
                "instruction": "Download from the official AAAI page or a lawful author copy if automated retrieval is unavailable.",
            }
        ],
    }
    MANIFEST_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Manifest written to {MANIFEST_PATH.relative_to(REPOSITORY_ROOT)}")
    if failures:
        print(f"Completed with {len(failures)} failure(s).", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
