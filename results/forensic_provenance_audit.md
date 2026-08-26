# Forensic Provenance Audit for FINAL-* Runs

## The Incident
During the final experiment campaign (T-600), the `HeadlessExperimentRunner` successfully executed all 14 final evaluation runs. As mandated by the protocol, each run automatically committed its results and pushed to the remote branch `feature/t-600-final-campaign` to ensure sequential, tamper-evident publication.

This created a chain of 15 commits (1 enabling commit + 14 execution commits). The `source_git_commit` in the `manifest.json` for each run correctly records the exact commit hash of the repository *at the moment the run started* (e.g., `5cee5ef99fcbffb49d6b3a1c4c5b4e79fb869676` for `FINAL-L01-C01`).

However, when merging PR #78 to `main`, the standard repository workflow performed a **squash merge**. This collapsed the entire 15-commit chain into a single new commit on `main`. As a result, the precise execution commits recorded in the run manifests became unreachable (dangling) from `main`, severing the durable cryptographic link between the recorded `source_git_commit` and the repository history.

## Resolution
Rewriting the manifest files to point to the squashed `main` commit would constitute scientific falsification, as the runs were objectively not executed from that squashed state.

Instead, we fetched the original execution commit chain from the closed PR #78 ref (`refs/pull/78/head`) and pushed it to a permanent, protected archive branch: `archive/final-campaign-execution`.

By doing this, the exact execution commits (such as `5cee5ef...`) are now durably reachable in the remote repository. A forensic auditor can checkout any `source_git_commit` recorded in any `FINAL-*` manifest and cryptographically verify the exact source code state that produced the run. 

The squashed state in `main` remains the canonical development history, while the archive branch serves as the immutable evidence ledger for the execution provenance. The scientific validity and provenance of all 14 runs is fully restored without rewriting history.
