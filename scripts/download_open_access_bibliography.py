#!/usr/bin/env python3
"""Retired compatibility entrypoint for the former local bibliography downloader."""
from __future__ import annotations

import sys

MESSAGE = """This command is retired.

Bibliography acquisition and source preservation now happen only in
MariosGiannakaras/ThesisBibliography. The thesis repository consumes the verified
generated package under research/bibliography/ via the Sync verified thesis
bibliography workflow.

See bibliography/README.md.
"""


def main() -> int:
    print(MESSAGE, file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
