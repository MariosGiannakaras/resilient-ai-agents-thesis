# Bibliography Markdown Conversions

This folder contains searchable derivatives of original sources.

## Conversion requirements

- Link each Markdown file to the exact original file and checksum.
- Preserve title, authors, year, sections and page boundaries where possible.
- Preserve tables, equations, captions and references accurately.
- Mark extraction/OCR uncertainty explicitly.
- Do not silently “correct” source content.
- Keep figure/table placeholders with original page references.
- Include conversion tool/version and date.
- Use the original PDF/page for exact quotations and citations; Markdown does not replace the authoritative source.

Suggested front matter:

```yaml
source_file:
source_sha256:
title:
authors:
year:
doi:
conversion_tool:
conversion_date:
quality_notes:
```
