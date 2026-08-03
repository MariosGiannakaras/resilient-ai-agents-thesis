#!/usr/bin/env python3
"""Strict decoding helpers for byte-preserved bibliography text."""
from __future__ import annotations

from collections import Counter
from pathlib import Path

LEGACY_ENCODING = "cesu-8"
BYTE_PRESERVED_CONTROL_LAYERS = {"sources", "materials"}
_ALLOWED_LAYOUT_CONTROLS = "\n\r\t\f"


class BibliographyTextError(ValueError):
    """Raised when imported text cannot be decoded under the consumer contract."""


def _control_counts(text: str) -> dict[str, int]:
    counts = Counter(
        ord(char) for char in text if ord(char) < 32 and char not in _ALLOWED_LAYOUT_CONTROLS
    )
    return {f"U+{codepoint:04X}": counts[codepoint] for codepoint in sorted(counts)}


def _allow_byte_preserved_controls(relative: Path) -> bool:
    return (
        len(relative.parts) >= 2
        and relative.parts[0] in BYTE_PRESERVED_CONTROL_LAYERS
        and relative.suffix.casefold() == ".md"
    )


def _validate_text_shape(
    text: str,
    relative: Path,
    *,
    expected_controls: dict[str, int] | None = None,
) -> dict[str, int]:
    controls = _control_counts(text)
    if controls and not _allow_byte_preserved_controls(relative):
        raise BibliographyTextError(
            f"Control characters are not permitted in text file: {relative.as_posix()}"
        )
    if expected_controls is not None and controls != expected_controls:
        raise BibliographyTextError(
            f"Recorded control-character map differs from text file: {relative.as_posix()}"
        )
    return controls


def _decode_cesu8(data: bytes, relative: Path) -> str:
    """Decode valid UTF-8 plus well-formed CESU-8 surrogate pairs.

    The immutable baseline contains a small number of source Markdown files whose
    PDF conversion preserved supplementary-plane Unicode characters as CESU-8.
    This decoder accepts only paired surrogates and converts them to canonical
    Unicode for search. It never rewrites the imported bytes.
    """
    try:
        intermediate = data.decode("utf-8", errors="surrogatepass")
    except UnicodeDecodeError as exc:
        raise BibliographyTextError(
            f"Text is neither UTF-8 nor valid CESU-8: {relative.as_posix()}"
        ) from exc

    output: list[str] = []
    pairs = 0
    index = 0
    while index < len(intermediate):
        codepoint = ord(intermediate[index])
        if 0xD800 <= codepoint <= 0xDBFF:
            if index + 1 >= len(intermediate):
                raise BibliographyTextError(
                    f"Unpaired CESU-8 high surrogate: {relative.as_posix()}"
                )
            low = ord(intermediate[index + 1])
            if not 0xDC00 <= low <= 0xDFFF:
                raise BibliographyTextError(
                    f"Unpaired CESU-8 high surrogate: {relative.as_posix()}"
                )
            scalar = 0x10000 + ((codepoint - 0xD800) << 10) + (low - 0xDC00)
            output.append(chr(scalar))
            pairs += 1
            index += 2
            continue
        if 0xDC00 <= codepoint <= 0xDFFF:
            raise BibliographyTextError(
                f"Unpaired CESU-8 low surrogate: {relative.as_posix()}"
            )
        output.append(intermediate[index])
        index += 1

    if pairs == 0:
        raise BibliographyTextError(
            f"Text is not valid UTF-8 and contains no CESU-8 surrogate pair: {relative.as_posix()}"
        )
    return "".join(output)


def decode_corpus_text(
    data: bytes,
    relative: Path,
    *,
    expected_encoding: str | None = None,
    expected_controls: dict[str, int] | None = None,
) -> tuple[str, str, dict[str, int]]:
    """Return decoded text, deterministic encoding label, and low-control counts.

    Canonical full-source and research-material Markdown can contain byte-preserved
    PDF-extraction controls. Those bytes remain part of the immutable upstream
    checksum surface. The consumer records their exact Unicode code points and
    counts and normalizes them only when building the ignored search index.
    """
    if expected_encoding not in {None, "utf-8", LEGACY_ENCODING}:
        raise BibliographyTextError(
            f"Unsupported recorded text encoding {expected_encoding!r}: {relative.as_posix()}"
        )
    if expected_controls is not None:
        if not isinstance(expected_controls, dict) or any(
            not isinstance(key, str)
            or not key.startswith("U+")
            or not isinstance(value, int)
            or value <= 0
            for key, value in expected_controls.items()
        ):
            raise BibliographyTextError(
                f"Invalid recorded control-character map: {relative.as_posix()}"
            )

    if expected_encoding != LEGACY_ENCODING:
        try:
            decoded = data.decode("utf-8")
        except UnicodeDecodeError:
            if expected_encoding == "utf-8":
                raise BibliographyTextError(f"Invalid UTF-8 text file: {relative.as_posix()}")
        else:
            controls = _validate_text_shape(
                decoded, relative, expected_controls=expected_controls
            )
            return decoded, "utf-8", controls

    # Legacy decoding is deliberately limited to canonical full-source Markdown.
    if len(relative.parts) < 2 or relative.parts[0] != "sources" or relative.suffix.casefold() != ".md":
        raise BibliographyTextError(f"Invalid UTF-8 text file: {relative.as_posix()}")
    decoded = _decode_cesu8(data, relative)
    controls = _validate_text_shape(decoded, relative, expected_controls=expected_controls)
    return decoded, LEGACY_ENCODING, controls


def normalize_search_text(text: str) -> str:
    """Replace byte-preserved extraction controls with deterministic spaces."""
    return "".join(
        " " if ord(char) < 32 and char not in _ALLOWED_LAYOUT_CONTROLS else char
        for char in text
    )


def read_corpus_text(
    path: Path,
    relative: Path,
    *,
    expected_encoding: str | None = None,
    expected_controls: dict[str, int] | None = None,
) -> tuple[str, str, dict[str, int]]:
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise BibliographyTextError(f"Cannot read text file {relative.as_posix()}: {exc}") from exc
    return decode_corpus_text(
        data,
        relative,
        expected_encoding=expected_encoding,
        expected_controls=expected_controls,
    )
