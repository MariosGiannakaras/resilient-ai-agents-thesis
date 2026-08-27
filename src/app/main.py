"""Native NiceGUI application for the resilient-agents thesis workspace.

The UI is a presentation/control layer over the headless Python scientific core.
At this checkpoint only truthful finalized evidence and read-only workspace state
are surfaced. Active-run supervision is added by T-530 and must never be faked.
"""
from __future__ import annotations

import multiprocessing
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from nicegui import ui

from app.state import AGENT_PROFILES, ApplicationReadModel, bytes_to_gib
from app.visualizations import (
    METRIC_LABELS,
    PLOTLY_CONFIG,
    agent_infographic_mermaid,
    aggregated_metric_figure,
    live_series_options,
    metric_heatmap_figure,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
READ_MODEL = ApplicationReadModel(REPO_ROOT)
APP_TITLE = "Resilient AI Agents Lab"

NAVIGATION = (
    ("/", "Dashboard", "dashboard"),
    ("/experiment", "New Experiment", "science"),
    ("/runs", "Runs", "play_circle"),
    ("/compare", "Compare", "compare_arrows"),
    ("/artifacts", "Artifacts", "inventory_2"),
)

GLOBAL_CSS = r"""
:root {
  --app-bg: #f5f7fb;
  --surface: rgba(255,255,255,0.96);
  --surface-soft: #f8fafc;
  --border: #e2e8f0;
  --text: #0f172a;
  --muted: #64748b;
  --primary-soft: #eff6ff;
  --warning-soft: #fff7ed;
  --warning-border: #fed7aa;
  --success-soft: #ecfdf5;
  --danger-soft: #fef2f2;
  --shadow: 0 10px 28px rgba(15,23,42,.07);
}
body { background: var(--app-bg); color: var(--text); }
.app-page { width: 100%; max-width: 1540px; margin: 0 auto; padding: 28px 34px 48px; gap: 22px; }
.app-header { backdrop-filter: blur(14px); border-bottom: 1px solid rgba(226,232,240,.9); }
.app-drawer { border-right: 1px solid var(--border); }
.hero-card, .panel-card, .metric-card, .agent-card {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  box-shadow: var(--shadow) !important;
  border-radius: 18px !important;
}
.hero-card { padding: 24px !important; }
.panel-card { padding: 20px !important; }
.metric-card { padding: 18px !important; min-height: 116px; }
.agent-card { padding: 20px !important; min-height: 360px; }
.eyebrow { color: #2563eb; font-size: 12px; font-weight: 800; letter-spacing: .1em; text-transform: uppercase; }
.page-title { font-size: 30px; line-height: 1.15; font-weight: 760; letter-spacing: -.025em; }
.section-title { font-size: 18px; font-weight: 720; letter-spacing: -.012em; }
.metric-value { font-size: 26px; font-weight: 760; letter-spacing: -.025em; }
.muted { color: var(--muted); }
.status-strip { border-radius: 14px; padding: 13px 15px; border: 1px solid var(--border); background: var(--surface-soft); }
.status-warning { background: var(--warning-soft); border-color: var(--warning-border); }
.status-success { background: var(--success-soft); border-color: #a7f3d0; }
.live-placeholder { min-height: 390px; border-radius: 16px; border: 1px dashed #cbd5e1; background: #fbfdff; }
.infographic-shell { min-height: 220px; border-radius: 14px; background: #fbfdff; border: 1px solid #edf2f7; padding: 12px; }
.q-drawer { background: rgba(255,255,255,.98) !important; }
.q-table__container, .ag-root-wrapper { border-radius: 14px !important; }
@media (max-width: 900px) {
  .app-page { padding: 20px 16px 36px; }
  .page-title { font-size: 25px; }
}
"""


def _safe_runs() -> tuple[list[dict], str | None]:
    try:
        return READ_MODEL.finalized_runs(), None
    except (OSError, ValueError) as exc:
        return [], str(exc)


def _plot_payload(figure) -> dict:
    payload = figure.to_dict()
    payload["config"] = PLOTLY_CONFIG
    return payload


def _status_badge(text: str, *, color: str = "grey-7") -> None:
    ui.badge(text, color=color).props('rounded').classes('text-weight-medium')


@contextmanager
def page_shell(title: str, subtitle: str, *, eyebrow: str) -> Iterator[None]:
    ui.add_css(GLOBAL_CSS)
    ui.colors(
        primary="#2563eb",
        secondary="#475569",
        accent="#7c3aed",
        positive="#15803d",
        negative="#b91c1c",
        warning="#c2410c",
        info="#0369a1",
    )

    with ui.header(elevated=False).classes('app-header bg-white text-slate-900 h-16 items-center'):
        with ui.row().classes('w-full items-center no-wrap px-4'):
            ui.icon('hub', size='26px').classes('text-primary')
            with ui.column().classes('gap-0 ml-1'):
                ui.label(APP_TITLE).classes('font-semibold text-[15px]')
                ui.label('Local thesis research application').classes('text-[11px] text-slate-500')
            ui.space()
            _status_badge('WP7 BLOCKED · pre-writing refinement', color='orange-8')

    with ui.left_drawer(value=True, fixed=True).classes('app-drawer pt-3'):
        ui.label('Workspace').classes('eyebrow px-4 pt-2 pb-1')
        for path, label, icon in NAVIGATION:
            ui.button(
                label,
                icon=icon,
                on_click=lambda target=path: ui.navigate.to(target),
            ).props('flat no-caps align=left').classes('w-full justify-start rounded-xl')
        ui.separator().classes('my-4')
        ui.label('Scientific state').classes('eyebrow px-4 pb-1')
        with ui.column().classes('px-4 gap-2 text-sm'):
            with ui.row().classes('items-center gap-2'):
                ui.icon('verified', size='17px').classes('text-green-700')
                ui.label('protocol-v1.0 preserved')
            with ui.row().classes('items-center gap-2'):
                ui.icon('pending', size='17px').classes('text-violet-700')
                ui.label('protocol-v1.1 candidate')
            with ui.row().classes('items-center gap-2'):
                ui.icon('lock', size='17px').classes('text-orange-700')
                ui.label('No thesis writing yet')

    with ui.column().classes('app-page'):
        with ui.card().classes('hero-card w-full'):
            ui.label(eyebrow).classes('eyebrow')
            ui.label(title).classes('page-title')
            ui.label(subtitle).classes('muted text-[14px] max-w-5xl')
        yield


def _metric_card(label: str, value: str, helper: str, icon: str) -> None:
    with ui.card().classes('metric-card w-full'):
        with ui.row().classes('w-full items-start no-wrap'):
            with ui.column().classes('gap-1'):
                ui.label(label).classes('muted text-xs font-semibold uppercase tracking-wide')
                ui.label(value).classes('metric-value')
                ui.label(helper).classes('muted text-xs')
            ui.space()
            ui.icon(icon, size='27px').classes('text-primary')


def _render_protocol_state() -> None:
    records = READ_MODEL.protocol_inventory()
    if not records:
        ui.label('No protocol files were found.').classes('muted')
        return
    with ui.row().classes('gap-2 flex-wrap'):
        for record in records:
            status = record['status']
            color = 'green-7' if status == 'frozen' else 'purple-7'
            _status_badge(f"{record['protocol_version']} · {status}", color=color)


def _render_agent_profile(agent) -> None:
    with ui.card().classes('agent-card w-full'):
        with ui.row().classes('w-full items-start no-wrap'):
            with ui.column().classes('gap-1'):
                ui.label(agent.name).classes('section-title')
                ui.label(agent.role).classes('muted text-sm')
            ui.space()
            color = 'purple-7' if agent.status == 'candidate-v1.1' else 'green-7'
            _status_badge(agent.status, color=color)
        ui.label(agent.description).classes('text-sm leading-relaxed')
        with ui.column().classes('gap-1 text-xs'):
            ui.label(f"Adaptation · {agent.adaptation}")
            ui.label(f"Planning · {agent.planning}")
        with ui.element('div').classes('infographic-shell w-full'):
            ui.mermaid(agent_infographic_mermaid(agent.agent_id)).classes('w-full')


@ui.page('/', title=f'{APP_TITLE} · Dashboard')
def dashboard_page() -> None:
    with page_shell(
        'Research workspace overview',
        'Real repository state, finalized experiment history and machine capability. No synthetic status or progress is shown.',
        eyebrow='Dashboard',
    ):
        runs, run_error = _safe_runs()
        system = READ_MODEL.system_snapshot()
        cpu = system.get('cpu', {}) if isinstance(system, dict) else {}
        memory = system.get('memory', {}) if isinstance(system, dict) else {}
        storage = system.get('storage', {}) if isinstance(system, dict) else {}

        with ui.grid(columns=4).classes('w-full gap-4'):
            _metric_card('Finalized runs', str(len(runs)), 'Integrity-validated registry entries', 'fact_check')
            _metric_card('Logical processors', str(cpu.get('logical_processors') or 'Unavailable'), 'Current machine snapshot', 'memory')
            _metric_card('Total memory', bytes_to_gib(memory.get('total_bytes')), 'Current machine snapshot', 'dns')
            _metric_card('Free workspace disk', bytes_to_gib(storage.get('repository_filesystem_free_bytes')), 'Repository filesystem', 'hard_drive')

        if run_error:
            with ui.row().classes('status-strip status-warning w-full items-center gap-2'):
                ui.icon('error_outline')
                ui.label(f'Run registry integrity/read error: {run_error}')

        with ui.grid(columns=2).classes('w-full gap-5'):
            with ui.card().classes('panel-card w-full'):
                ui.label('Protocol state').classes('section-title')
                ui.label('v1.0 evidence remains immutable; v1.1 is not frozen until D0 tuning/pilot gates pass.').classes('muted text-sm')
                _render_protocol_state()
            with ui.card().classes('panel-card w-full'):
                ui.label('Current application capability').classes('section-title')
                with ui.column().classes('gap-2 text-sm'):
                    ui.label('✓ Finalized run history and evidence inspection')
                    ui.label('✓ Thesis-final v1.0 comparison visualizations')
                    ui.label('✓ F0/C0/D0 explanatory model infographics')
                    ui.label('○ Active-run supervision and live GridWorld: T-530 in progress').classes('text-orange-800')

        with ui.card().classes('panel-card w-full'):
            with ui.row().classes('w-full items-center'):
                ui.label('Recent finalized runs').classes('section-title')
                ui.space()
                ui.button('Open Runs', icon='arrow_forward', on_click=lambda: ui.navigate.to('/runs')).props('flat no-caps')
            if not runs:
                ui.label('No finalized runs are available in the canonical registry.').classes('muted')
            else:
                rows = runs[:8]
                ui.aggrid({
                    'columnDefs': [
                        {'headerName': 'Run', 'field': 'run_id', 'minWidth': 210},
                        {'headerName': 'Status', 'field': 'status', 'width': 120},
                        {'headerName': 'Protocol', 'field': 'protocol_version', 'width': 135},
                        {'headerName': 'Stage', 'field': 'stage', 'width': 120},
                        {'headerName': 'Started (UTC)', 'field': 'started_at_utc', 'minWidth': 185},
                    ],
                    'rowData': rows,
                    'defaultColDef': {'sortable': True, 'filter': True, 'resizable': True},
                }, modules='community').classes('w-full h-80')


@ui.page('/experiment', title=f'{APP_TITLE} · New Experiment')
def experiment_page() -> None:
    with page_shell(
        'Configure an experiment',
        'Understand the agent regimes first, then choose only scientifically permitted configurations. Launch controls stay disabled until protocol-v1.1 and the truthful runtime service are ready.',
        eyebrow='New Experiment',
    ):
        with ui.row().classes('status-strip status-warning w-full items-start gap-3'):
            ui.icon('lock_clock', size='22px')
            with ui.column().classes('gap-0'):
                ui.label('Launch is intentionally unavailable at this checkpoint.').classes('font-semibold')
                ui.label('T-521 must freeze an allowed v1.1 configuration surface and T-530 must provide truthful active-run supervision. The UI will not expose controls that the backend cannot yet honor.').classes('text-sm')

        ui.label('Agent regimes').classes('section-title')
        ui.label('These are scientifically distinct behaviors, not cosmetic model labels.').classes('muted text-sm')
        with ui.grid(columns=3).classes('w-full gap-5'):
            for profile in AGENT_PROFILES:
                _render_agent_profile(profile)

        with ui.card().classes('panel-card w-full'):
            ui.label('Resolved configuration review · planned').classes('section-title')
            ui.label('The completed configurator will expose agent(s), held-out/development layout, uncertainty condition, seed/repetition plan and only protocol-approved parameters. Before launch it will show the exact resolved request and run count.').classes('muted text-sm')


@ui.page('/runs', title=f'{APP_TITLE} · Runs')
def runs_page() -> None:
    with page_shell(
        'Runs and live experiment workspace',
        'Finalized history is available now. Active-run status, GridWorld state and telemetry will attach to the T-530 runtime observer; until then the live panel remains explicitly unavailable.',
        eyebrow='Runs',
    ):
        with ui.tabs().classes('w-full') as tabs:
            live_tab = ui.tab('live', label='Live', icon='monitor_heart')
            history_tab = ui.tab('history', label='History', icon='history')
        with ui.tab_panels(tabs, value=live_tab).classes('w-full bg-transparent'):
            with ui.tab_panel(live_tab).classes('px-0'):
                with ui.grid(columns=2).classes('w-full gap-5'):
                    with ui.card().classes('panel-card w-full'):
                        with ui.row().classes('w-full items-center'):
                            ui.label('Live GridWorld').classes('section-title')
                            ui.space()
                            _status_badge('T-530 pending', color='orange-8')
                        ui.label('This surface will render only the read-only backend observer state from a real active run. Historical runs without retained step trace will never be reconstructed.').classes('muted text-sm')
                        with ui.column().classes('live-placeholder w-full items-center justify-center gap-2'):
                            ui.icon('grid_on', size='52px').classes('text-slate-300')
                            ui.label('No truthful active-run observer is connected yet.').classes('font-semibold')
                            ui.label('GridWorld animation will appear here when T-530 is implemented.').classes('muted text-sm')
                    with ui.card().classes('panel-card w-full'):
                        ui.label('Live performance telemetry').classes('section-title')
                        ui.label('ECharts is ready for differential animated updates from real run DTOs; the chart is intentionally empty rather than populated with demo values.').classes('muted text-sm')
                        ui.echart(
                            live_series_options({}, title='Episode return comparison', y_axis_label='Episode return')
                        ).classes('w-full h-[390px]')
                with ui.card().classes('panel-card w-full'):
                    ui.label('Planned live comparison channels').classes('section-title')
                    ui.label('Compatible matched runs can overlay F0/C0/D0 or different approved settings on shared axes. Live values are always labelled provisional and do not become thesis evidence until canonical finalization/analysis.').classes('muted text-sm')
            with ui.tab_panel(history_tab).classes('px-0'):
                runs, run_error = _safe_runs()
                if run_error:
                    with ui.row().classes('status-strip status-warning w-full items-center gap-2'):
                        ui.icon('error_outline')
                        ui.label(run_error)
                elif not runs:
                    ui.label('No finalized runs are available.').classes('muted')
                else:
                    ui.aggrid({
                        'columnDefs': [
                            {'headerName': 'Run', 'field': 'run_id', 'minWidth': 220, 'pinned': 'left'},
                            {'headerName': 'Status', 'field': 'status', 'width': 120, 'filter': True},
                            {'headerName': 'Protocol', 'field': 'protocol_version', 'width': 140, 'filter': True},
                            {'headerName': 'Stage', 'field': 'stage', 'width': 120, 'filter': True},
                            {'headerName': 'Started (UTC)', 'field': 'started_at_utc', 'minWidth': 190},
                            {'headerName': 'Finished (UTC)', 'field': 'finished_at_utc', 'minWidth': 190},
                        ],
                        'rowData': runs,
                        'defaultColDef': {'sortable': True, 'filter': True, 'resizable': True},
                        'pagination': True,
                        'paginationPageSize': 20,
                    }, modules='community').classes('w-full h-[620px]')


@ui.page('/compare', title=f'{APP_TITLE} · Compare')
def compare_page() -> None:
    with page_shell(
        'Compare agent resilience',
        'Interactive thesis-ready views from stored analysis evidence. Historical v1.0 charts label their existing error bars as SD; paired 95% CIs are added only when the versioned T-522 analysis produces them.',
        eyebrow='Compare',
    ):
        frame = READ_MODEL.v10_aggregated_summary()
        if frame is None:
            with ui.row().classes('status-strip status-warning w-full items-center gap-2'):
                ui.icon('warning_amber')
                ui.label('The historical aggregated summary artifact is unavailable or unreadable.')
            return

        metrics = [
            metric
            for metric in ('post_change_mean', 'cumulative_deficit', 'immediate_degradation', 'nominal_mean')
            if (metric, 'mean') in frame.columns
        ]
        with ui.card().classes('panel-card w-full'):
            with ui.row().classes('w-full items-end gap-4'):
                metric_select = ui.select(
                    {metric: METRIC_LABELS.get(metric, metric) for metric in metrics},
                    value=metrics[0],
                    label='Metric',
                ).props('outlined dense').classes('min-w-72')
                ui.label('Bars = mean; v1.0 error bars = SD. Use the Plotly camera control for a high-resolution PNG.').classes('muted text-xs pb-2')
            plot = ui.plotly(
                _plot_payload(aggregated_metric_figure(frame, metrics[0]))
            ).classes('w-full h-[620px]')

            def change_metric(event) -> None:
                plot.figure = _plot_payload(aggregated_metric_figure(frame, str(event.value)))
                plot.update()

            metric_select.on_value_change(change_metric)

        with ui.card().classes('panel-card w-full'):
            ui.label('Condition × agent overview').classes('section-title')
            ui.label('A compact heatmap is useful for presentation screenshots, while the chart above preserves the actual magnitudes and SD.').classes('muted text-sm')
            ui.plotly(
                _plot_payload(metric_heatmap_figure(frame, 'cumulative_deficit'))
            ).classes('w-full h-[520px]')


@ui.page('/artifacts', title=f'{APP_TITLE} · Artifacts')
def artifacts_page() -> None:
    with page_shell(
        'Evidence and export artifacts',
        'Inspect and download the stored thesis-final artifacts that already exist in the repository. Files are presented as evidence; the UI does not regenerate or silently replace them.',
        eyebrow='Artifacts',
    ):
        artifacts = READ_MODEL.thesis_final_artifacts()
        if not artifacts:
            ui.label('No thesis-final artifacts were found.').classes('muted')
            return
        rows = [
            {
                'name': item['name'],
                'type': item['suffix'].lstrip('.').upper() or 'FILE',
                'size_kib': round(item['size_bytes'] / 1024, 1),
            }
            for item in artifacts
        ]
        with ui.grid(columns=2).classes('w-full gap-5'):
            with ui.card().classes('panel-card w-full'):
                ui.label('Artifact index').classes('section-title')
                ui.aggrid({
                    'columnDefs': [
                        {'headerName': 'Artifact', 'field': 'name', 'flex': 1},
                        {'headerName': 'Type', 'field': 'type', 'width': 100},
                        {'headerName': 'Size (KiB)', 'field': 'size_kib', 'width': 120},
                    ],
                    'rowData': rows,
                    'defaultColDef': {'sortable': True, 'filter': True, 'resizable': True},
                }, modules='community').classes('w-full h-96')
            with ui.card().classes('panel-card w-full'):
                ui.label('Downloads').classes('section-title')
                ui.label('These are the existing repository artifacts; downloading does not modify scientific evidence.').classes('muted text-sm')
                with ui.column().classes('w-full gap-2'):
                    for item in artifacts:
                        with ui.row().classes('w-full items-center no-wrap border border-slate-200 rounded-xl p-2'):
                            ui.icon('description').classes('text-primary')
                            ui.label(item['name']).classes('text-sm')
                            ui.space()
                            ui.button(
                                'Download',
                                icon='download',
                                on_click=lambda path=item['path']: ui.download.file(str(path)),
                            ).props('flat dense no-caps')


def main() -> None:
    """Start the application in native desktop mode or explicit CI/browser mode."""
    multiprocessing.freeze_support()
    browser_mode = os.environ.get('THESIS_APP_BROWSER_MODE', '').strip().lower() in {
        '1', 'true', 'yes', 'on'
    }
    if browser_mode:
        port = int(os.environ.get('THESIS_APP_PORT', '8501'))
        ui.run(
            title=APP_TITLE,
            host='127.0.0.1',
            port=port,
            native=False,
            show=False,
            reload=False,
        )
    else:
        ui.run(
            title=APP_TITLE,
            native=True,
            window_size=(1480, 920),
            reload=False,
        )


if __name__ in {'__main__', '__mp_main__'}:
    main()
