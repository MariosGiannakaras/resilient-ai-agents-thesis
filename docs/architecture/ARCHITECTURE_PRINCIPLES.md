# Architecture Principles

## Central principle

**Polished outside, bounded inside.**

The application must look and behave like a complete research dashboard while keeping its internal architecture proportional to a local single-user thesis tool.

## Core principles

1. **Core without UI.** Environment, agents, runner, storage and analysis operate through CLI or programmatic interfaces.
2. **Dashboard as control and presentation layer.** It uses validated commands and real state; it does not duplicate scientific logic.
3. **One canonical configuration path.** CLI and UI resolve the same schemas, defaults and validation rules.
4. **Immutable raw results.** Storage does not depend on UI state.
5. **Simple lifecycle.** Implement only the states and controls required by the selected runner and thesis workflows.
6. **Stable identifiers and provenance.** Runs, experiments and artifacts remain traceable.
7. **Structured logs and events.** Human-readable views derive from real backend records.
8. **Version everything that affects results.** Code, configs, environment, agent, metric and processing versions.
9. **Simple local architecture.** Prefer a modular monolith or equally bounded local design.
10. **Dependency restraint.** Add libraries only for correctness, reproducibility or clear usability value.
11. **No hidden notebook state.** Canonical code and configs live outside notebooks.
12. **Schema validation at boundaries.** Invalid config or result data fails clearly.
13. **Scientific errors are first-class.** Invalid environments, failed metrics and protocol misuse remain visible.
14. **Small reviewable changes.** Avoid speculative frameworks and future-proofing.
15. **Security proportional to private local scope.** Protect secrets and private documents without inventing public-service architecture.

## Explicit non-goals

Unless a documented requirement changes the scope, do not introduce:

- microservices or Kubernetes,
- cloud-only infrastructure,
- distributed or remote workers,
- multi-user authentication, roles or permissions,
- enterprise monitoring/telemetry stacks,
- plugin ecosystems,
- complex priority schedulers,
- production deployment pipelines,
- mobile clients,
- speculative AI features.

## UI architecture rules

- Consolidate the experience into a small number of research workflows.
- Do not mirror every backend component as a separate page.
- Keep execution, monitoring, comparison and export easy to discover.
- Use modern reusable visual components and a consistent design system.
- Responsive behavior targets normal desktop and laptop use; mobile app parity is not required.
- Scientific metadata remains accessible even when progressive disclosure is used.
- Expensive live visualization is optional and must not alter scientific execution.
- Feature complexity must be justified against thesis value and completion risk.
