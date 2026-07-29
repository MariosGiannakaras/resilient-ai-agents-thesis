# Scope Refinement — Thesis Completion First

**Date:** 2026-07-29  
**Status:** Accepted user direction

## Core objective

The project must produce a scientifically adequate, correct and realistically completable thesis without unnecessary technical complexity.

The application is not the main research contribution and must not become a production-grade platform. It remains an important deliverable and must provide a polished, modern and easy-to-use research dashboard so the user can configure, run, monitor, understand and export the required experiments without writing code or using console commands.

## Product principle

**Polished outside, bounded inside.**

Simplification applies to architecture, feature count and engineering overhead. It does not justify a rough, outdated or scientifically incomplete interface.

The dashboard must hide irrelevant technical complexity while keeping scientifically important information visible and traceable.

## Priority order

1. Clear and bounded research question.
2. Simple, validated GridWorld.
3. Small, scientifically justified set of models and uncertainty types.
4. Fair and reproducible experimental protocol.
5. Reliable and comparable results.
6. Modern, complete UI for execution, monitoring and interpretation.
7. Advanced features only when they solve a real need and do not threaten completion.

## Required user workflows

The final application must support the scientifically necessary workflows:

- choose validated model, environment and experiment settings,
- create and run the required single or batched runs,
- show truthful status, progress, warnings, errors and useful logs,
- visualize the GridWorld and agent behavior,
- retain run history and the resolved parameters of every execution,
- compare models, seeds, settings and uncertainty conditions,
- present understandable metrics, charts and tables,
- export real data, figures, tables and supporting material for the thesis.

## UI quality

The interface must be:

- modern and visually polished,
- consistent and readable,
- suitable for screenshots and presentation,
- responsive for normal desktop and laptop use,
- built from useful dashboards, cards, charts, filters, tables and status indicators,
- based only on real backend data and scientific definitions.

A visually minimal or outdated interface is not an acceptable interpretation of architectural simplicity.

## Complexity budget

The following are outside the required scope unless a documented need appears:

- public or cloud deployment,
- multi-user support,
- authentication, roles and permission systems,
- microservices and distributed orchestration,
- production observability infrastructure,
- complex queue scheduling or remote workers,
- mobile applications,
- non-essential AI assistants,
- speculative extensibility and future-proofing.

Features such as advanced checkpoint management, complex sweeps, queue priorities, plugin systems or AI-assisted interpretation must remain optional until the core thesis workflow proves that they are necessary.

## Research and design constraints

- Previous model, stack, metric and feature proposals are not binding.
- The experimental design must remain small enough to understand, execute, validate and explain.
- The UI must not expose an unmanageable number of models or parameters.
- Defaults and available settings must come from the frozen protocol or validated exploratory scope.
- Results must be visible, comparable and exportable before aesthetic extras are added.
- Every feature must map to a research, reproducibility, usability or thesis-delivery requirement.

## Completion criterion

The target is not a minimal demo and not a production platform. It is a complete research tool with:

- a validated independent core,
- a controlled experimental design,
- reliable result provenance,
- a polished bounded dashboard,
- enough functionality to execute and present the thesis experiments confidently.
