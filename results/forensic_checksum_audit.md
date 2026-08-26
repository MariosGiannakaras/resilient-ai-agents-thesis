# Forensic Checksum Audit for FINAL-* Runs

## The Incident
During the final campaign execution (T-600), the `HeadlessExperimentRunner` generated runs and wrote JSON artifacts (`resolved-config.json`, `summary.json`, etc.). On the Windows execution environment, Python's default `open(..., "w")` wrote these files with `\r\n` (CRLF) line endings. The `RunBundle` finalization logic hashed the files exactly as they were written on disk, producing CRLF-based SHA256 checksums (e.g., `30545...` for `FINAL-L01-C01/resolved-config.json`).

When the Git publisher automatically committed these files, the `.gitattributes` rule `* text=auto eol=lf` instructed Git to normalize the line endings to `\n` (LF) in the repository blob. 

During the WP6 evidence freeze (T-601), checking out the repository resulted in LF-based files. Re-hashing them produced LF-based checksums (e.g., `9f7c...`). Because this mismatched the CRLF-based checksums recorded in the `manifest.json`, the validation failed. 

In PR #80, `patch_checksums.py` was used to retroactively rewrite the `manifest.json` and `checksums.sha256` files to contain the LF-based hashes, masking the original discrepancy without creating a forensic record.

## Forensic Proof of Semantic Equivalence
We extracted the original blobs from the execution commit (`0cf4011`) and compared them to the LF-normalized files. 

For `FINAL-L01-C01/resolved-config.json`:
- Original recorded hash in manifest: `30545d15989f83493139f91ad2254025134ca9c234c49772410d07acfe442c71` (CRLF)
- Git blob hash (after normalization): `9f7c4bc89782d5b3c0a51bbc94049d3e9d25fdadf3aa6452d1e01ebb40b87ac7` (LF)
- Current local hash: `9f7c4bc89782d5b3c0a51bbc94049d3e9d25fdadf3aa6452d1e01ebb40b87ac7` (LF)

A direct JSON parse of both the CRLF and LF byte streams demonstrates that the parsed objects are semantically identical. The only change was the byte-level representation of line endings enforced by Git.

## Resolution
The scientific payload is demonstrably unchanged. We accept the LF-normalized byte streams as the canonical frozen artifacts, because they are what Git immutably stores and distributes. 

To prevent this in the future, the `RunBundle` writer MUST be patched to explicitly specify `newline="\n"` when writing text artifacts, ensuring that the hash computed at execution time exactly matches the Git-normalized blob.

Because the runs are valid, we do not need to discard them or rerun the final matrix. We will preserve the current LF-patched manifests but acknowledge their provenance through this explicit validated freeze layer.
