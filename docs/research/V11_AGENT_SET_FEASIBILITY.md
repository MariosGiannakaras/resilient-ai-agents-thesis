# Candidate v1.1 Five-Strategy Feasibility Baseline

**Date:** 2026-08-27  
**Status:** T-523 pre-freeze feasibility accounting; not a final runtime claim

## Purpose

Quantify the effect of DEC-047's five main agent strategies before candidate-v1.1 freeze. This is a resource/scale check, not scientific evidence and not authorization to run final layouts.

## Current candidate dimensions

Main scientific strategies:

1. Fixed Q-Learning;
2. Adaptive Q-Learning;
3. SARSA;
4. Dyna-Q;
5. Dyna-Q+.

Current retained experimental target:

- 4 fresh final layouts;
- 7 single-factor conditions per layout;
- 32 paired root seeds per layout/condition whole experiment;
- 512 nominal checkpoint-training episodes per root;
- 16 pre-change + 32 post-change evaluation episodes = 48 evaluation episodes per branch;
- matched reference + disrupted branch for each scientific strategy.

The GridWorld is the controlled testbed. These dimensions are used to compare agent strategies; they do not redefine the thesis as a GridWorld study.

## Exact episode accounting

With the current runner design, one root for one layout/condition whole experiment contains:

- common nominal checkpoint training: `512` episodes;
- each main strategy: `2 branches × 48 episodes = 96` evaluation episodes;
- five strategies: `5 × 96 = 480` evaluation episodes.

Therefore:

- episodes/root = `512 + 480 = 992`;
- episodes/layout-condition run = `992 × 32 = 31,744`;
- whole final runs = `4 layouts × 7 conditions = 28`;
- candidate full-matrix episodes = `31,744 × 28 = 888,832`.

This count excludes optional reference-only Random/privileged bounds from the fair final matrix. They are not allowed to silently expand the main scientific denominator.

## Comparison with immutable v1.0

Historical v1.0 used two main scientific regimes, two layouts and seven conditions:

- per root: `512 training + 2 strategies × 2 branches × 48 = 704` episodes;
- per whole run: `704 × 32 = 22,528` episodes;
- 14 whole runs: `315,392` episodes.

The current five-strategy/four-layout target is therefore:

`888,832 / 315,392 ≈ 2.818`

or about **2.82× the historical v1.0 episode count**.

## Empirical historical timing anchor

The immutable manifests provide real target-machine anchors rather than a synthetic benchmark:

- `FINAL-L01-C01`: 2026-08-26 20:42:49 UTC → 20:44:47 UTC = **118 s** for 22,528 episodes;
- `FINAL-L02-C07`: 2026-08-26 21:11:46 UTC → 21:14:04 UTC = **138 s** for 22,528 episodes.

Those timings include the historical two-strategy computation and filesystem/event overhead. They do **not** measure SARSA/Dyna planning overhead and must not be presented as a v1.1 runtime measurement.

A planning-free episode-count extrapolation places the five-strategy/four-layout campaign in roughly the same order as `~2.82×` the historical total campaign time. Using the two verified historical run examples only as anchors gives an order-of-magnitude baseline around **80–90 minutes before additional Dyna planning cost**. This is explicitly an extrapolation, not an accepted runtime forecast.

## Planning-cost uncertainty

Dyna-Q and Dyna-Q+ perform additional planning backups per real transition. Their actual cost depends materially on the predeclared `planning_steps` candidates selected for non-final evaluation. Therefore an exact full-campaign duration cannot be honestly fixed in T-523 before that tuning surface is defined and measured.

Required next resource gate:

1. T-521 predeclares the bounded Dyna planning-step values and any SARSA-specific fairness tuning values.
2. T-522 measures representative **non-final** development/tuning runtime on the validated thesis machine.
3. The resource gate records wall time, episode/step counts, planning-update counts and artifact size.
4. If runtime is disproportionate, adjust only through an explicit pre-final amendment; do not inspect or trim final outcomes.
5. Final layouts/seeds remain untouched until protocol freeze/application gates authorize them.

## Feasibility conclusion

The five-strategy design is **computationally plausible enough to continue to bounded non-final validation**: the matrix remains below one million environment episodes under the current target and the historical CPU baseline completed the smaller frozen campaign in practical desktop time.

T-523 does not claim final runtime acceptance from this accounting alone. The unmeasured planning multiplier is intentionally carried into the T-521/T-522 non-final resource gate. No scientific model is removed merely to make a runtime estimate look better.
