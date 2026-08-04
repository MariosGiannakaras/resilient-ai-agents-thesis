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
- self-explanatory through precise labels, helper text, messages, symbols, semantic colors and clear visual hierarchy,
- suitable for screenshots and presentation,
- responsive for normal desktop and laptop use,
- built from useful dashboards, cards, charts, filters, tables and status indicators,
- based only on real backend data and scientific definitions.

Non-obvious scientific/technical controls and terminology should have concise tooltips or contextual explanations. Status, warnings and errors should use consistent text plus symbols/visual treatment; color must not be the only carrier of meaning. Empty states and unavailable actions should explain what is missing and what the user can do next.

Before an experiment launches, the application should show a concise resolved-configuration/validation summary so the user can understand what will actually run. Destructive or high-impact actions should request confirmation only when useful; harmless navigation/configuration should not be interrupted unnecessarily.

After the final dashboard structure is stable, add a lightweight first-run onboarding/tutorial covering the essential workflow. It should be short, skippable, replayable from Help/Getting Started, support Previous/Next/Skip/Finish navigation, and avoid a heavy custom frontend/JavaScript tour framework unless native Streamlit capabilities prove genuinely insufficient.

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
- speculative extensibility and future-proofing,
- heavyweight custom onboarding/coach-mark frontend infrastructure for behavior achievable with lightweight native UI primitives.

Features such as advanced checkpoint management, complex sweeps, queue priorities, plugin systems or AI-assisted interpretation must remain optional until the core thesis workflow proves that they are necessary.

## Research and design constraints

- Previous model, stack, metric and feature proposals are not binding.
- The experimental design must remain small enough to understand, execute, validate and explain.
- The UI must not expose an unmanageable number of models or parameters.
- Defaults and available settings must come from the frozen protocol or validated exploratory scope.
- Results must be visible, comparable and exportable before aesthetic extras are added.
- Every feature must map to a research, reproducibility, usability or thesis-delivery requirement.
- UI explanations must remain synchronized with the actual protocol/metric definitions and implemented behavior rather than becoming a separate manual that can drift.

## Completion criterion

The target is not a minimal demo and not a production platform. It is a complete research tool with:

- a validated independent core,
- a controlled experimental design,
- reliable result provenance,
- a polished bounded and self-explanatory dashboard,
- lightweight contextual help/onboarding sufficient for normal use without separate training,
- enough functionality to execute and present the thesis experiments confidently.
