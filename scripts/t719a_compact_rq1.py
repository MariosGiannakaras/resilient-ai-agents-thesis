from __future__ import annotations

from pathlib import Path

import t719a_targeted_final_pass as build

# Keep the requested examiner-facing interpretation while minimizing pagination pressure.
# The content remains a semantic clarification only: no result, protocol value, estimand,
# threshold, horizon, seed, layout, root, budget, or registered asset changes.
build.RQ1_EXPLANATION = (
    "Με βέλτιστη διαδρομή 12 ενεργειών, το −0,100 είναι η απόδοση μιας shortest-path "
    "επίλυσης του task: 11×(−0,1)+1,0=−0,1, αφού το goal reward +1,0 αντικαθιστά το "
    "final step reward."
)


def ensure_source_replacement(path: Path, old: str, new: str) -> None:
    """Align a durable prose source once, while remaining safe on CI/PR reruns."""
    text = path.read_text(encoding="utf-8")
    new_count = text.count(new)
    if new_count == 1:
        return
    if new_count > 1:
        raise RuntimeError(f"{path}: targeted source block appears {new_count} times")
    old_count = text.count(old)
    if old_count != 1:
        raise RuntimeError(
            f"{path}: expected exactly one old source anchor or one aligned target block; "
            f"old={old_count}, new={new_count}"
        )
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


# The push workflow archives the aligned durable prose sources. A subsequent PR workflow
# must be able to rebuild the exact candidate from the immutable T-719 base without
# duplicating already-aligned source prose or failing because the old source anchor is gone.
build.replace_once = ensure_source_replacement


if __name__ == "__main__":
    build.main()
