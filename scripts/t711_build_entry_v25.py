#!/usr/bin/env python3
"""Compatibility entry point for the active T-715 reader composition build.

The current implementation lives in t711_build_entry_v26, which adds the two
DEVELOPMENT-only application screenshots and the visual-QA front-matter/appendix fixes.
"""

from t711_build_entry_v26 import t711


if __name__ == "__main__":
    t711.builder.main()
