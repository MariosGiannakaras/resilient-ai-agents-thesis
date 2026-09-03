#!/usr/bin/env python3
"""T-711 builder entrypoint with manifest-safe table caption normalization.

Some finalized T-613 table records intentionally omit the optional `caption` key.
This adapter supplies a deterministic non-scientific display caption from the
registered asset ID, without changing table contents or any scientific value.
"""

from __future__ import annotations

import build_review_ready_thesis_docx as builder

_original_add_asset_table = builder.add_asset_table


def _manifest_safe_add_asset_table(doc, asset, inserted):
    normalized = dict(asset)
    normalized.setdefault("caption", normalized.get("title") or normalized["asset_id"])
    return _original_add_asset_table(doc, normalized, inserted)


builder.add_asset_table = _manifest_safe_add_asset_table

if __name__ == "__main__":
    builder.main()
