#!/usr/bin/env python3
"""Strict decoding helpers for byte-preserved bibliography text."""
from __future__ import annotations

from pathlib import Path

LEGACY_ENCODING = "cesu-8"


class BibliographyTextError(ValueError):
    """Raised when imported text cannot be decoded under the consumer contract."""


def _validate_text_shape(text: str, relative: Path) -> None:
    if "\x00" in text:
        raise BibliographyTextError(f"NUL byte is not permitted in text file: {relative.as_posix()}")
    invalid_controls = sum(ord(char) < 32 and char not in "\n\r\t\f" for char in text)
    if invalid_controls:
        raise BibliographyTextError(
            f"Control characters are not permitted in text file: {relative.as_posix()}"
        )


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
    decoded = "".join(output)
    _validate_text_shape(decoded, relative)
    return decoded


def decode_corpus_text(data: bytes, relative: Path, *, expected_encoding: str | None = None) -> tuple[str, str]:
    """Return decoded text and the deterministic encoding label used."""
    if expected_encoding not in {None, "utf-8", LEGACY_ENCODING}:
        raise BibliographyTextError(
            f"Unsupported recorded text encoding {expected_encoding!r}: {relative.as_posix()}"
        )
    if expected_encoding != LEGACY_ENCODING:
        try:
            decoded = data.decode("utf-8")
        except UnicodeDecodeError:
            if expected_encoding == "utf-8":
                raise BibliographyTextError(f"Invalid UTF-8 text file: {relative.as_posix()}")
        else:
            _validate_text_shape(decoded, relative)
            return decoded, "utf-8"

    # Legacy decoding is deliberately limited to canonical full-source Markdown.
    if len(relative.parts) < 2 or relative.parts[0] != "sources" or relative.suffix.casefold() != ".md":
        raise BibliographyTextError(f"Invalid UTF-8 text file: {relative.as_posix()}")
    return _decode_cesu8(data, relative), LEGACY_ENCODING


def read_corpus_text(path: Path, relative: Path, *, expected_encoding: str | None = None) -> tuple[str, str]:
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise BibliographyTextError(f"Cannot read text file {relative.as_posix()}: {exc}") from exc
    return decode_corpus_text(data, relative, expected_encoding=expected_encoding)
