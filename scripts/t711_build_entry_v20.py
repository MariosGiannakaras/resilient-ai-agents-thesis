#!/usr/bin/env python3
"""T-715 pagination adapter for the reader-scoped Chapter 4."""

from __future__ import annotations

import t711_build_entry_v19 as v19


# T-714's final pagination guard is still useful, but the original architecture-flow
# sentence was intentionally simplified by T-715. Point the same keep-together check at
# the new reader-facing experiment-flow paragraph rather than weakening the guard.
v19.v18.FLOW_PREFIX = "Η ροή ξεκινά από μία καθορισμένη πειραματική ρύθμιση."

if __name__ == "__main__":
    v19.t711.builder.main()
