# DEC-045 — Visual analytics, infographics, live charts and thesis-ready figures

**Date:** 2026-08-27  
**Status:** Accepted pre-WP7 application design decision  
**Depends on:** DEC-044 native NiceGUI application

## Goal

The application must do more than show dashboard widgets. It must make agent behavior and experimental evidence easy to understand live, and it must produce clean comparative visuals that can be captured directly for the thesis and presentation without rebuilding the same analysis in a separate plotting application.

The visualization stack must remain truthful: live displays are provisional backend-derived telemetry, while thesis/final comparison figures are generated from stored analysis/evidence. UI animation never changes scientific execution.

## Decision

Use a small role-specific visualization stack rather than one library for every visual.

### Plotly — scientific and publication/presentation figures

Use Plotly for stable analysis and comparison views derived from stored evidence:

- agent × condition grouped comparisons;
- paired effects with 95% confidence intervals when T-522 provides them;
- box, violin, strip and ECDF distribution views where raw paired observations are available;
- condition/layout/agent heatmaps;
- degradation, cumulative-deficit and terminal-performance figures;
- thesis-final historical v1.0 evidence views and future v1.1 evidence views;
- interactive hover/details while keeping screenshot-friendly titles, units, legends and annotations.

NiceGUI `ui.plotly` accepts Plotly figures/dicts, supports plot updates and Plotly events. Configure the Plotly modebar with image export enabled so a user can save a chart from the application. Static automated export through Kaleido is optional and must not become a normal runtime dependency because Kaleido v1 requires a compatible Chrome/Chromium installation; repository/CI screenshots remain the guaranteed review/export path.

### Apache ECharts — live operational telemetry

Use NiceGUI's built-in `ui.echart` for high-frequency live charts because ECharts updates data/options through differential `setOption` updates with animation. Intended live views include:

- episode return by agent/run;
- rolling return or other explicitly defined provisional smoothing;
- cumulative reward and, where definition is available online, provisional cumulative deficit;
- episode/step progress;
- goal distance/steps-to-goal when exposed by the read-only observer;
- disturbance/event markers;
- side-by-side or overlaid traces for multiple selected agents or experiment settings.

Live charts must clearly display `LIVE / PROVISIONAL`; they are never thesis-final evidence until the run finalizes and the canonical analysis pipeline produces stored metrics.

### Mermaid — model and experiment infographics

Use NiceGUI `ui.mermaid` for self-explanatory diagrams such as:

- F0 frozen Q-learning information/update flow;
- C0 continual Q-learning update flow;
- D0 Dyna-Q+ real experience → empirical model → planning updates → policy flow;
- evaluator-visible versus agent-visible information boundary;
- experiment lifecycle from configuration through finalized evidence.

Diagrams are explanatory presentation artifacts, not scientific data.

### AG Grid Community — analytical data tables

Use the NiceGUI built-in AG Grid Community module for run history, comparison selections, raw/processed result tables and artifact indexes when filtering/sorting/selection materially improves inspection. Do not enable AG Grid Enterprise or CDN-only features.

## Visual consistency contract

All scientific figures share one application figure theme:

- consistent agent names/order and semantic identity across every page;
- same metric names and units as the canonical analysis definitions;
- titles state what is being compared, not a conclusion;
- subtitles/captions state protocol/stage/layout/condition/sample size where relevant;
- color is never the only differentiator: combine color with labels, markers, line dash or direct annotation;
- no 3D charts, decorative gauges, pie charts for agent-performance comparison, or unlabeled composite resilience score;
- show uncertainty/distributions rather than only averages whenever the underlying evidence supports it;
- no hidden axis truncation that exaggerates effects;
- screenshot layout targets thesis/presentation use at common 16:9 and document-width proportions.

## Live-vs-final boundary

The application treats visual data in three explicit classes:

1. **Live/provisional:** active-run telemetry from T-530 runtime/observer service. It may change and is never cited as final evidence.
2. **Finalized run:** integrity-validated run bundle data. It is immutable but may still be an individual run rather than an inferential aggregate.
3. **Analysis/evidence:** stored, versioned aggregation/statistics artifacts. These are the source for thesis-ready comparison figures.

No UI page may silently promote class 1 or 2 into class 3.

## Live comparison contract

When multiple agents/settings run under compatible matched configuration, the Runs workspace may overlay their real live series. Each trace must identify run/agent/configuration and share the same axis definition. If runs are not directly compatible, the UI shows them separately or displays a compatibility warning rather than implying a controlled comparison.

Visualization refresh cadence is independent of the scientific episode/step cadence. Dropped/skipped display frames are acceptable; dropped scientific events are not.

## Dependencies

No new standalone plotting framework is required beyond the existing Plotly dependency and NiceGUI's bundled ECharts/Mermaid/AG Grid integrations. Statistical calculations such as paired bootstrap confidence intervals remain owned by the versioned Python analysis layer, not by the UI chart library.
