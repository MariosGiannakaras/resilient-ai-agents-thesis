# Pilot Campaign Execution

`src/resilient_agents/pilot_campaign.py` and `scripts/run_pilot_campaign.py` are the fail-closed execution path used by `T-410`. The driver supports the full `pilot-v0.1` campaign and its exact bounded `pilot-v0.2` amendment, only from durable `main`, and resumes by validating deterministic run identities rather than overwriting output.

```text
uv run python scripts/run_pilot_campaign.py \
  --repo-root <repository-root> \
  --protocol configs/protocols/pilot-v0.1.json
```

## Precommitted campaign

The driver expands the protocol without reading outcomes to alter the matrix:

1. execute one full first-stage tuning child as the representative preflight;
2. derive the child timeout as `max(60 seconds, ceil(20 x preflight duration))` and stop for an amendment if it exceeds 7,200 seconds;
3. evaluate the 16 learning-rate/exploration configurations at discount `15/16` on both tuning layouts;
4. select the stage-one winner by the protocol's ordered criteria;
5. evaluate only that winner's learning-rate/exploration pair at discounts `7/8` and `31/32` on both tuning layouts, producing 18 unique configurations and 36 tuning runs in total;
6. select across all 18 configurations and execute both pilot layouts under all seven declared conditions, producing 14 pilot runs;
7. derive `PV01-PILOT-ANALYSIS` through the validated analysis pipeline and write the campaign state under `results/campaigns/pilot-v0.1/`; the amended v0.2 path instead revalidates/reuses the F0-only tuning evidence, executes the complete `PV02-*` matrix, and derives `PV02-PILOT-ANALYSIS` plus its separate campaign state.

The stored primary diagnostic setting is fixed before pilot outcomes at immediate `1`, worst `4`, terminal `8`, recovery tolerance `1`, and stability `4`. It is only a central descriptive view; analysis always computes all 54 predeclared sensitivity combinations, so this setting cannot suppress sensitivity or become an unrecorded final choice.

## Tuning score and collision definition

Each configuration's mean nominal return uses every frozen-F0 matched-reference episode across both tuning layouts and all four precommitted roots. The second criterion is the lower of the two layout means. The third criterion is nominal collision steps divided by executed nominal reference transitions. Collision steps are exactly recoverable under the fixed reward contract from episode return, length, and termination status; inconsistent values fail closed. Final ties use lexicographically smallest canonical hyperparameter JSON exactly as declared.

Every tuning input is first passed through finalized-bundle validation and semantic analysis reproduction. The pilot driver cannot select from a partial, failed, corrupted, mismatched, or non-reproducible run.

## Runtime, failure, publication, and recovery

The headless request records the operational child timeout. The runner checks it between roots, episodes, and transitions; expiry finalizes the bundle as `failed` with `ExperimentTimeoutError` and retained partial state/events. Completed and failed whole experiments use the same optional one-publication boundary.

Every child has a stable run ID and `auto_publish=true`. A finalized existing child is skipped only after its full request, marker, manifest, checksums, and run-index record match the campaign plan. Each newly completed child is committed and pushed from `main` before the next begins. This keeps every substantial real result remotely recoverable and preserves its source commit as a durable ancestor. Unfinished root-boundary state continues to use the headless runner's existing verified recovery contract.

Campaign analysis and the final pilot interpretation/report are committed only after all planned children complete. Pilot outputs remain diagnostic evidence and cannot be used as final thesis results.

## v0.2 implementation amendment

The first real v0.1 observation-corruption child exposed the R0 terminal-observation alias defect described in `PILOT_PROTOCOL_V0_2.md`. The original failed and completed pilot attempts remain published. The v0.2 driver reused only the unaffected F0 tuning evidence, recomputed the same selection, and completed all 14 pilot children under new `PV02-*` identities and the same precommitted pilot seeds. The final amended analysis excludes no poor outcome; it selects the complete consistent v0.2 matrix while campaign state separately inventories every superseded v0.1 attempt and its reason. `PILOT_REPORT_V0_2.md` records the resulting feasibility and protocol constraints.
