"""Strict immutable recipe envelope for development and confirmatory studies."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping

from .model import EvidenceClass

STUDY_RECIPE_SCHEMA_VERSION = 1
_ALLOWED_KEYS = {
    "schema_version",
    "recipe_id",
    "protocol_version",
    "evidence_class",
    "scientific_status",
    "frozen",
    "study",
}


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def _plain_json(value: Any, *, field: str) -> Any:
    """Round-trip through strict JSON to reject opaque/non-finite runtime values."""

    try:
        encoded = _canonical_json(value)
        return json.loads(encoded)
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise ValueError(f"{field} must contain strict JSON-compatible data") from exc


@dataclass(frozen=True)
class StudyRecipe:
    """Immutable content-addressed recipe snapshot.

    The backend never edits a recipe after a study is created. Development and
    tuning recipes may be superseded by a different recipe ID/hash, while a
    confirmatory recipe must be explicitly marked frozen before it can be used
    for final evidence.
    """

    recipe_id: str
    protocol_version: str
    evidence_class: EvidenceClass
    scientific_status: str
    frozen: bool
    study: Mapping[str, Any]
    schema_version: int = STUDY_RECIPE_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != STUDY_RECIPE_SCHEMA_VERSION:
            raise ValueError("unsupported study recipe schema_version")
        if not isinstance(self.recipe_id, str) or not self.recipe_id.strip():
            raise ValueError("recipe_id must be non-empty")
        if self.recipe_id != self.recipe_id.strip() or any(
            char.isspace() for char in self.recipe_id
        ):
            raise ValueError("recipe_id must not contain whitespace")
        if not isinstance(self.protocol_version, str) or not self.protocol_version.strip():
            raise ValueError("protocol_version must be non-empty")
        if not isinstance(self.evidence_class, EvidenceClass):
            raise ValueError("evidence_class must be EvidenceClass")
        if not isinstance(self.scientific_status, str) or not self.scientific_status.strip():
            raise ValueError("scientific_status must be non-empty")
        if not isinstance(self.frozen, bool):
            raise ValueError("frozen must be bool")
        if not isinstance(self.study, Mapping) or not self.study:
            raise ValueError("study must be a non-empty mapping")
        normalized = _plain_json(dict(self.study), field="study")
        object.__setattr__(self, "study", normalized)
        if self.evidence_class is EvidenceClass.CONFIRMATORY and not self.frozen:
            raise ValueError("confirmatory recipes must be frozen")
        if self.evidence_class in {EvidenceClass.DERIVED, EvidenceClass.HISTORICAL}:
            raise ValueError(
                "derived/historical evidence cannot be launched as a study recipe"
            )

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "StudyRecipe":
        if not isinstance(payload, Mapping):
            raise ValueError("study recipe must be an object")
        if set(payload) != _ALLOWED_KEYS:
            missing = sorted(_ALLOWED_KEYS - set(payload))
            unknown = sorted(set(payload) - _ALLOWED_KEYS)
            raise ValueError(
                f"study recipe keys mismatch; missing={missing}, unknown={unknown}"
            )
        try:
            evidence_class = EvidenceClass(str(payload["evidence_class"]))
        except ValueError as exc:
            raise ValueError("unsupported study recipe evidence_class") from exc
        return cls(
            schema_version=payload["schema_version"],
            recipe_id=payload["recipe_id"],
            protocol_version=payload["protocol_version"],
            evidence_class=evidence_class,
            scientific_status=payload["scientific_status"],
            frozen=payload["frozen"],
            study=payload["study"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "recipe_id": self.recipe_id,
            "protocol_version": self.protocol_version,
            "evidence_class": self.evidence_class.value,
            "scientific_status": self.scientific_status,
            "frozen": self.frozen,
            "study": _plain_json(dict(self.study), field="study"),
        }

    def sha256(self) -> str:
        return hashlib.sha256(_canonical_json(self.to_dict()).encode("utf-8")).hexdigest()
