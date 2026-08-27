"""Native NiceGUI application for the resilient-agents thesis workspace.

NiceGUI is a presentation/control layer over the UI-independent scientific and
runtime services. Live state comes exclusively from RuntimeService telemetry;
finalized evidence comes from stored run bundles/artifacts. The UI never invents
progress, trajectories, metrics or capabilities.
"""
from __future__ import annotations

import json
import multiprocessing
import os
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from nicegui import ui

from app.live import build_runtime_telemetry_view, gridworld_html
from app.state import (
    AGENT_PROFILE_BY_ID,
    AGENT_PROFILES,
    ApplicationReadModel,
    CandidateExperimentForm,
    bytes_to_gib,
    setting_summary,
    shortened_hash,
)
from app.visualizations import (
    CONDITION_LABELS,
    METRIC_LABELS,
    PLOTLY_CONFIG,
    agent_infographic_mermaid,
    aggregated_metric_figure,
    live_series_options,
    metric_heatmap_figure,
)
from resilient_agents.contracts import ProtocolStage
from resilient_agents.runtime_service import RuntimeRunSnapshot, RuntimeStatus

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

STATUS_COLORS = {
    RuntimeStatus.QUEUED: "blue-grey-7",
    RuntimeStatus.RUNNING: "blue-7",
    RuntimeStatus.COMPLETED: "green-7",
    RuntimeStatus.FAILED: "red-7",
    RuntimeStatus.CANCELLED: "orange-8",
    RuntimeStatus.INTERRUPTED: "deep-orange-7",
}

GLOBAL_CSS = r"""
:root {
  --app-bg: #f5f7fb;
  --surface: rgba(255,255,255,0.97);
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
.status-danger { background: var(--danger-soft); border-color: #fecaca; }
.infographic-shell { min-height: 220px; border-radius: 14px; background: #fbfdff; border: 1px solid #edf2f7; padding: 12px; }
.tech-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px; }
.gw-board { display: grid; gap: 5px; width: min(100%, 520px); aspect-ratio: 1 / 1; margin: 10px auto; }
.gw-cell { display:flex; align-items:center; justify-content:center; border:1px solid #dbe3ef; border-radius:7px; background:#fff; font-weight:800; font-size:16px; transition:transform .15s ease, box-shadow .15s ease; }
.gw-obstacle { background:#334155; color:#fff; border-color:#334155; }
.gw-start { box-shadow: inset 0 0 0 2px #60a5fa; color:#1d4ed8; }
.gw-goal { background:#dcfce7; color:#166534; border-color:#86efac; }
.gw-agent { background:#dbeafe; color:#1d4ed8; border-color:#60a5fa; transform:scale(1.04); box-shadow:0 4px 12px rgba(37,99,235,.22); }
.gw-observation { background:#fef3c7; color:#92400e; border-color:#fbbf24; }
.grid-empty { min-height:390px; border:1px dashed #cbd5e1; border-radius:16px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; color:#64748b; background:#fbfdff; }
.grid-empty-icon { font-size:52px; color:#cbd5e1; }
.q-drawer { background: rgba(255,255,255,.98) !important; }
.q-table__container, .ag-root-wrapper { border-radius: 14px !important; }
@media (prefers-reduced-motion: reduce) { .gw-cell { transition:none; } }
@media (max-width: 900px) { .app-page { padding: 20px 16px 36px; } .page-title { font-size: 25px; } }
"""


def _plot_payload(figure: Any) -> dict[str, Any]:
    payload = figure.to_dict()
    payload["config"] = PLOTLY_CONFIG
    return payload


def _status_badge(text: str, *, color: str = "grey-7") -> None:
    ui.badge(text, color=color).props("rounded").classes("text-weight-medium")


def _runtime_badge(status: RuntimeStatus) -> None:
    _status_badge(status.value.replace("_", " ").title(), color=STATUS_COLORS[status])


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
    with ui.header(elevated=False).classes("app-header bg-white text-slate-900 h-16 items-center"):
        with ui.row().classes("w-full items-center no-wrap px-4"):
            ui.icon("hub", size="26px").classes("text-primary")
            with ui.column().classes("gap-0 ml-1"):
                ui.label(APP_TITLE).classes("font-semibold text-[15px]")
                ui.label("Local thesis research application").classes("text-[11px] text-slate-500")
            ui.space()
            _status_badge("WP7 BLOCKED · pre-writing refinement", color="orange-8")

    with ui.left_drawer(value=True, fixed=True).classes("app-drawer pt-3"):
        ui.label("Workspace").classes("eyebrow px-4 pt-2 pb-1")
        for path, label, icon in NAVIGATION:
            ui.button(
                label,
                icon=icon,
                on_click=lambda target=path: ui.navigate.to(target),
            ).props("flat no-caps align=left").classes("w-full justify-start rounded-xl")
        ui.separator().classes("my-4")
        ui.label("Scientific state").classes("eyebrow px-4 pb-1")
        with ui.column().classes("px-4 gap-2 text-sm"):
            with ui.row().classes("items-center gap-2"):
                ui.icon("verified", size="17px").classes("text-green-700")
                ui.label("protocol-v1.0 preserved")
            with ui.row().classes("items-center gap-2"):
                ui.icon("science", size="17px").classes("text-violet-700")
                ui.label("protocol-v1.1 candidate")
            with ui.row().classes("items-center gap-2"):
                ui.icon("lock", size="17px").classes("text-orange-700")
                ui.label("Final reserve locked")

    with ui.column().classes("app-page"):
        with ui.card().classes("hero-card w-full"):
            ui.label(eyebrow).classes("eyebrow")
            ui.label(title).classes("page-title")
            ui.label(subtitle).classes("muted text-[14px] max-w-5xl")
        yield


def _metric_card(label: str, value: str, helper: str, icon: str) -> None:
    with ui.card().classes("metric-card w-full"):
        with ui.row().classes("w-full items-start no-wrap"):
            with ui.column().classes("gap-1"):
                ui.label(label).classes("muted text-xs font-semibold uppercase tracking-wide")
                ui.label(value).classes("metric-value")
                ui.label(helper).classes("muted text-xs")
            ui.space()
            ui.icon(icon, size="27px").classes("text-primary")


def _safe_runtime_runs() -> tuple[list[RuntimeRunSnapshot], str | None]:
    try:
        return READ_MODEL.runtime_runs(), None
    except (OSError, ValueError, RuntimeError) as exc:
        return [], str(exc)


def _render_protocol_state() -> None:
    records = READ_MODEL.protocol_inventory()
    if not records:
        ui.label("No protocol files were found.").classes("muted")
        return
    with ui.row().classes("gap-2 flex-wrap"):
        for record in records:
            status = record["status"]
            color = "green-7" if status == "frozen" else "purple-7"
            _status_badge(f"{record['protocol_version']} · {status}", color=color)


def _render_agent_profile(agent: Any) -> None:
    with ui.card().classes("agent-card w-full"):
        with ui.row().classes("w-full items-start no-wrap"):
            with ui.column().classes("gap-1"):
                ui.label(agent.name).classes("section-title")
                ui.label(agent.role).classes("muted text-sm")
            ui.space()
            color = "purple-7" if agent.status == "candidate-v1.1" else "green-7"
            _status_badge(agent.mechanism_badge, color=color)
        ui.label(agent.description).classes("text-sm leading-relaxed")
        with ui.column().classes("gap-1 text-xs"):
            ui.label(f"Adaptation · {agent.adaptation}")
            ui.label(f"Planning · {agent.planning}")
        with ui.element("div").classes("infographic-shell w-full"):
            ui.mermaid(agent_infographic_mermaid(agent.agent_id)).classes("w-full")
        with ui.expansion("Technical details / Reproducibility", icon="fingerprint").classes("w-full text-xs"):
            ui.label(f"Internal agent ID: {agent.agent_id}").classes("muted")
            ui.label(f"Lifecycle: {agent.status}").classes("muted")


def _runtime_table_rows(runs: list[RuntimeRunSnapshot]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": item.run_id,
            "status": item.status.value,
            "progress": (
                "—"
                if item.progress.total_roots == 0
                else f"{item.progress.completed_roots}/{item.progress.total_roots} roots"
            ),
            "attempt": item.attempt,
            "started_at_utc": item.created_at_utc,
            "updated_at_utc": item.updated_at_utc,
        }
        for item in runs
    ]


@ui.page("/", title=f"{APP_TITLE} · Dashboard")
def dashboard_page() -> None:
    with page_shell(
        "Research workspace overview",
        "Real runtime state, scientific protocol state and machine resources. No synthetic progress or status is shown.",
        eyebrow="Dashboard",
    ):
        runtime_runs, runtime_error = _safe_runtime_runs()
        active = [
            item
            for item in runtime_runs
            if item.status in {RuntimeStatus.QUEUED, RuntimeStatus.RUNNING}
        ]
        system = READ_MODEL.system_snapshot()
        cpu = system.get("cpu", {}) if isinstance(system, dict) else {}
        memory = system.get("memory", {}) if isinstance(system, dict) else {}
        storage = system.get("storage", {}) if isinstance(system, dict) else {}
        protocol = READ_MODEL.candidate_protocol_summary()

        with ui.grid(columns=4).classes("w-full gap-4"):
            _metric_card("Active / queued", str(len(active)), "RuntimeService records", "monitor_heart")
            _metric_card("All visible runs", str(len(runtime_runs)), "Runtime + historical history", "history")
            _metric_card("Total memory", bytes_to_gib(memory.get("total_bytes")), "Current machine snapshot", "dns")
            _metric_card("Free workspace disk", bytes_to_gib(storage.get("repository_filesystem_free_bytes")), "Repository filesystem", "hard_drive")

        if runtime_error:
            with ui.row().classes("status-strip status-danger w-full items-center gap-2"):
                ui.icon("error_outline")
                ui.label(f"Runtime/history read error: {runtime_error}")

        with ui.grid(columns=2).classes("w-full gap-5"):
            with ui.card().classes("panel-card w-full"):
                with ui.row().classes("w-full items-center"):
                    ui.label("Candidate protocol").classes("section-title")
                    ui.space()
                    _status_badge(str(protocol["status"]), color="purple-7")
                ui.label(
                    f"{protocol['strategy_count']} strategies · {protocol['condition_count']} conditions · "
                    f"{protocol['final_layout_count']} fresh final layouts · {protocol['final_root_count']} final roots"
                ).classes("text-sm")
                ui.label("Final evidence access is blocked until the scientific freeze and later user gate.").classes("muted text-sm")
                with ui.expansion("Technical details / Reproducibility", icon="fingerprint").classes("w-full"):
                    ui.label(f"Protocol SHA-256: {protocol['sha256']}").classes("text-xs break-all")
                _render_protocol_state()
            with ui.card().classes("panel-card w-full"):
                ui.label("Current application capability").classes("section-title")
                with ui.column().classes("gap-2 text-sm"):
                    ui.label("✓ Five protocol-v1.1 Agent strategies and bounded configurations")
                    ui.label("✓ Truthful runtime lifecycle, resources and controls")
                    ui.label("✓ Read-only live GridWorld telemetry with non-interference test")
                    ui.label("✓ Historical v1.0 evidence inspection")
                    ui.label("○ Final v1.1 mode remains correctly locked").classes("text-orange-800")

        with ui.card().classes("panel-card w-full"):
            with ui.row().classes("w-full items-center"):
                ui.label("Active and recent runs").classes("section-title")
                ui.space()
                ui.button("New Experiment", icon="add", on_click=lambda: ui.navigate.to("/experiment")).props("flat no-caps")
                ui.button("Open Runs", icon="arrow_forward", on_click=lambda: ui.navigate.to("/runs")).props("flat no-caps")
            if not runtime_runs:
                ui.label("No runtime or historical runs are visible yet.").classes("muted")
            else:
                ui.aggrid(
                    {
                        "columnDefs": [
                            {"headerName": "Run", "field": "run_id", "minWidth": 220},
                            {"headerName": "Status", "field": "status", "width": 125},
                            {"headerName": "Progress", "field": "progress", "width": 145},
                            {"headerName": "Attempt", "field": "attempt", "width": 95},
                            {"headerName": "Updated (UTC)", "field": "updated_at_utc", "minWidth": 190},
                        ],
                        "rowData": _runtime_table_rows(runtime_runs[:10]),
                        "defaultColDef": {"sortable": True, "filter": True, "resizable": True},
                    },
                    modules="community",
                ).classes("w-full h-80")


@ui.page("/experiment", title=f"{APP_TITLE} · New Experiment")
def experiment_page() -> None:
    with page_shell(
        "Configure an experiment",
        "Choose only protocol-approved non-final candidate configurations. Repetitions are the complete predeclared root bank, not an unrestricted seed playground.",
        eyebrow="New Experiment",
    ):
        with ui.row().classes("status-strip status-warning w-full items-start gap-3"):
            ui.icon("verified_user", size="22px")
            with ui.column().classes("gap-0"):
                ui.label("Development and tuning only").classes("font-semibold")
                ui.label(
                    "Final-evidence execution is intentionally unavailable until T-522 freezes retained configurations and the later application/user gates pass."
                ).classes("text-sm")

        form: dict[str, Any] = {
            "stage": ProtocolStage.DEVELOPMENT.value,
            "run_id": f"APP-DEV-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
            "layout_id": READ_MODEL.stage_layout_ids(ProtocolStage.DEVELOPMENT)[0],
            "condition_id": "nominal",
            "agents": ["f0", "c0"],
            "configs": {},
        }

        def _normalise_configs() -> None:
            stage = ProtocolStage(form["stage"])
            options = READ_MODEL.candidate_configuration_options(stage=stage)
            selected = set(form["agents"])
            form["configs"] = {
                agent_id: (
                    form["configs"].get(agent_id)
                    if form["configs"].get(agent_id) in {item.configuration_id for item in options[agent_id]}
                    else options[agent_id][0].configuration_id
                )
                for agent_id in selected
            }

        _normalise_configs()

        @ui.refreshable
        def configurator() -> None:
            stage = ProtocolStage(form["stage"])
            layouts = READ_MODEL.stage_layout_ids(stage)
            conditions = READ_MODEL.stage_condition_ids(stage)
            roots = READ_MODEL.stage_root_seeds(stage)
            configuration_options = READ_MODEL.candidate_configuration_options(stage=stage)

            with ui.grid(columns=2).classes("w-full gap-5"):
                with ui.card().classes("panel-card w-full"):
                    ui.label("Experiment scope").classes("section-title")
                    ui.input(
                        "Run ID",
                        value=form["run_id"],
                        on_change=lambda event: form.update(run_id=str(event.value)),
                    ).props("outlined dense").classes("w-full").tooltip("Stable identifier for this run bundle. It must be unique and contain no path separators.")

                    def change_stage(event: Any) -> None:
                        form["stage"] = str(event.value)
                        selected_stage = ProtocolStage(form["stage"])
                        form["layout_id"] = READ_MODEL.stage_layout_ids(selected_stage)[0]
                        form["condition_id"] = READ_MODEL.stage_condition_ids(selected_stage)[0]
                        _normalise_configs()
                        configurator.refresh()

                    ui.select(
                        {
                            ProtocolStage.DEVELOPMENT.value: "Development · non-final exploration",
                            ProtocolStage.TUNING.value: "Tuning · predeclared selection evidence",
                        },
                        value=form["stage"],
                        label="Stage",
                        on_change=change_stage,
                    ).props("outlined dense").classes("w-full").tooltip("Candidate protocol permits only development/tuning. Final is deliberately locked.")
                    ui.select(
                        list(layouts),
                        value=form["layout_id"],
                        label="GridWorld layout",
                        on_change=lambda event: form.update(layout_id=str(event.value)),
                    ).props("outlined dense").classes("w-full")
                    ui.select(
                        {condition: CONDITION_LABELS.get(condition, condition) for condition in conditions},
                        value=form["condition_id"],
                        label="Uncertainty / change condition",
                        on_change=lambda event: form.update(condition_id=str(event.value)),
                    ).props("outlined dense").classes("w-full")
                    with ui.row().classes("status-strip w-full items-center gap-2"):
                        ui.icon("repeat")
                        ui.label(f"Repetitions: {len(roots)} predeclared root seeds · complete bank required")
                    with ui.expansion("Root seeds", icon="numbers").classes("w-full"):
                        ui.label(", ".join(str(seed) for seed in roots)).classes("text-xs break-all muted")

                with ui.card().classes("panel-card w-full"):
                    ui.label("Agent strategy").classes("section-title")
                    ui.label("Select one or more mechanism-distinct strategies. Internal IDs stay secondary.").classes("muted text-sm")

                    def change_agents(event: Any) -> None:
                        values = list(event.value or [])
                        form["agents"] = [value for value in READ_MODEL.candidate_protocol().strategy_ids() if value in values]
                        _normalise_configs()
                        configurator.refresh()

                    ui.select(
                        {profile.agent_id: profile.name for profile in AGENT_PROFILES},
                        value=form["agents"],
                        label="Agent strategy",
                        multiple=True,
                        on_change=change_agents,
                    ).props("outlined dense use-chips").classes("w-full")
                    if not form["agents"]:
                        ui.label("Select at least one strategy.").classes("text-red-700 text-sm")
                    for agent_id in form["agents"]:
                        profile = AGENT_PROFILE_BY_ID[agent_id]
                        options = configuration_options[agent_id]
                        with ui.card().classes("w-full border border-slate-200 shadow-none rounded-xl p-3"):
                            with ui.row().classes("w-full items-center"):
                                ui.label(profile.name).classes("font-semibold")
                                ui.space()
                                _status_badge(profile.mechanism_badge, color="blue-grey-7")
                            ui.label(profile.description).classes("muted text-xs")

                            def config_changed(event: Any, selected_agent: str = agent_id) -> None:
                                form["configs"][selected_agent] = str(event.value)
                                configurator.refresh()

                            ui.select(
                                {option.configuration_id: setting_summary(option.settings) for option in options},
                                value=form["configs"][agent_id],
                                label="Approved configuration",
                                on_change=config_changed,
                            ).props("outlined dense").classes("w-full")
                            selected_option = next(
                                item for item in options if item.configuration_id == form["configs"][agent_id]
                            )
                            with ui.expansion("Technical details / Reproducibility", icon="fingerprint").classes("w-full"):
                                ui.label(f"Configuration ID: {selected_option.configuration_id}").classes("text-xs")
                                ui.label(f"SHA-256: {selected_option.sha256}").classes("text-xs break-all muted")

            request = None
            error: str | None = None
            try:
                request = READ_MODEL.resolved_candidate_request(
                    CandidateExperimentForm(
                        run_id=str(form["run_id"]),
                        stage=stage,
                        layout_id=str(form["layout_id"]),
                        condition_id=str(form["condition_id"]),
                        agent_configuration_ids=dict(form["configs"]),
                    )
                )
            except (ValueError, KeyError) as exc:
                error = str(exc)

            with ui.card().classes("panel-card w-full"):
                with ui.row().classes("w-full items-center"):
                    ui.label("Resolved configuration review").classes("section-title")
                    ui.space()
                    _status_badge("NON-FINAL CANDIDATE", color="purple-7")
                ui.label("This exact validated request is what the runtime service will queue. Review it before launch.").classes("muted text-sm")
                if error:
                    with ui.row().classes("status-strip status-danger w-full items-center gap-2"):
                        ui.icon("error_outline")
                        ui.label(error)
                elif request is not None:
                    ui.code(json.dumps(request.to_dict(), indent=2, sort_keys=True), language="json").classes("w-full max-h-96 overflow-auto")

                    def launch() -> None:
                        assert request is not None
                        try:
                            queued = READ_MODEL.queue_candidate(request)
                            started = READ_MODEL.start_next_runtime_run()
                        except (OSError, ValueError, RuntimeError, FileExistsError) as exc:
                            ui.notify(str(exc), type="negative", close_button=True)
                            return
                        if started is not None and started.run_id == queued.run_id:
                            ui.notify(f"Run {queued.run_id} started.", type="positive")
                        else:
                            ui.notify(f"Run {queued.run_id} queued.", type="positive")
                        ui.navigate.to("/runs")

                    ui.button("Queue and start", icon="play_arrow", on_click=launch).props("unelevated no-caps").classes("self-end")

        configurator()

        ui.label("Agent strategy guide").classes("section-title")
        with ui.grid(columns=3).classes("w-full gap-5"):
            for profile in AGENT_PROFILES:
                _render_agent_profile(profile)


def _render_live_run(run: RuntimeRunSnapshot) -> None:
    try:
        rows = READ_MODEL.runtime_telemetry(run.run_id, after_sequence=-1, limit=10_000)
        telemetry = build_runtime_telemetry_view(rows)
    except (OSError, ValueError, RuntimeError) as exc:
        with ui.row().classes("status-strip status-danger w-full items-center gap-2"):
            ui.icon("error_outline")
            ui.label(f"Live telemetry error: {exc}")
        return

    with ui.row().classes("w-full items-center gap-3"):
        ui.label(run.run_id).classes("section-title")
        _runtime_badge(run.status)
        if run.progress.total_roots:
            ui.label(f"{run.progress.completed_roots}/{run.progress.total_roots} roots").classes("muted text-sm")
        ui.space()
        if run.capabilities.can_cancel:
            def cancel() -> None:
                try:
                    READ_MODEL.cancel_runtime_run(run.run_id)
                    ui.notify(f"Cancelled {run.run_id}", type="warning")
                except (RuntimeError, OSError) as exc:
                    ui.notify(str(exc), type="negative")
            ui.button("Cancel", icon="stop_circle", on_click=cancel).props("outline no-caps color=negative")
        if run.capabilities.can_restart:
            def restart() -> None:
                try:
                    READ_MODEL.restart_runtime_run(run.run_id)
                    READ_MODEL.start_next_runtime_run()
                    ui.notify(f"Restarted {run.run_id}", type="positive")
                except (RuntimeError, OSError) as exc:
                    ui.notify(str(exc), type="negative")
            ui.button("Restart", icon="restart_alt", on_click=restart).props("outline no-caps")

    if run.progress.total_roots:
        ui.linear_progress(value=run.progress.fraction_complete).props("rounded stripe").classes("w-full")
    with ui.row().classes("w-full gap-4 text-xs muted"):
        ui.label(f"Heartbeat: {run.heartbeat_at_utc or 'No telemetry heartbeat yet'}")
        ui.label(f"Attempt: {run.attempt}")
        ui.label(f"Latest sequence: {run.latest_telemetry_sequence if run.latest_telemetry_sequence is not None else '—'}")
    if run.message:
        with ui.row().classes("status-strip status-warning w-full items-center gap-2"):
            ui.icon("info")
            ui.label(run.message)

    with ui.grid(columns=2).classes("w-full gap-5"):
        with ui.card().classes("panel-card w-full"):
            with ui.row().classes("w-full items-center"):
                ui.label("Live GridWorld").classes("section-title")
                ui.space()
                _status_badge("READ-ONLY LIVE", color="blue-7")
            view = telemetry.gridworld
            if view is not None:
                ui.label(
                    f"{view.strategy_name} · {view.branch} · {view.phase} · episode {view.episode_index} · step {view.step}"
                ).classes("muted text-xs")
            ui.html(gridworld_html(view)).classes("w-full")
            if view is not None:
                with ui.row().classes("w-full gap-3 text-xs flex-wrap"):
                    ui.label(f"Intended: {view.intended_action or '—'}")
                    ui.label(f"Executed: {view.executed_action or '—'}")
                    ui.label(
                        f"Episode return: {view.cumulative_episode_return if view.cumulative_episode_return is not None else '—'}"
                    )
                if view.delivered_observation is not None and view.delivered_observation != view.position:
                    ui.label("◇ Delivered observation differs from evaluator-visible true position.").classes("text-amber-800 text-xs")
        with ui.card().classes("panel-card w-full"):
            ui.label("Live episode returns").classes("section-title")
            ui.label("Operational/provisional telemetry only; final evidence still comes from finalized analysis.").classes("muted text-xs")
            ui.echart(
                live_series_options(
                    telemetry.return_series,
                    title="Episode return comparison",
                    y_axis_label="Episode return",
                )
            ).classes("w-full h-[440px]")

    with ui.card().classes("panel-card w-full"):
        ui.label("Recent runtime events").classes("section-title")
        if not telemetry.recent_events:
            ui.label("No telemetry events yet.").classes("muted")
        else:
            for event in reversed(telemetry.recent_events):
                event_name = str(event.get("event") or "event")
                with ui.row().classes("w-full items-center gap-3 py-1 border-b border-slate-100"):
                    ui.icon("timeline", size="16px").classes("text-slate-400")
                    ui.label(f"#{event.get('sequence', '—')} · {event_name}").classes("font-medium text-xs")
                    ui.label(
                        f"{event.get('agent_id', '—')} · {event.get('phase', '—')} · ep {event.get('episode_index', '—')}"
                    ).classes("muted text-xs")
                    ui.space()
                    if event_name == "gridworld_step":
                        ui.label(f"step {event.get('step', '—')} · r={event.get('reward', '—')}").classes("muted text-xs")


@ui.page("/runs", title=f"{APP_TITLE} · Runs")
def runs_page() -> None:
    with page_shell(
        "Runs and live experiment workspace",
        "RuntimeService is the single source of live lifecycle, progress, controls and GridWorld telemetry. Historical trajectories are never synthesized when trace data is absent.",
        eyebrow="Runs",
    ):
        selected: dict[str, str | None] = {"run_id": None}

        @ui.refreshable
        def run_workspace() -> None:
            runs, error = _safe_runtime_runs()
            if error:
                with ui.row().classes("status-strip status-danger w-full items-center gap-2"):
                    ui.icon("error_outline")
                    ui.label(error)
                return
            active = [
                item
                for item in runs
                if item.status in {RuntimeStatus.RUNNING, RuntimeStatus.QUEUED}
            ]
            restartable = [item for item in runs if item.capabilities.can_restart]
            selectable = active + [item for item in restartable if item not in active]
            if selected["run_id"] is None and selectable:
                selected["run_id"] = selectable[0].run_id

            with ui.tabs().classes("w-full") as tabs:
                live_tab = ui.tab("live", label=f"Live / active ({len(active)})", icon="monitor_heart")
                history_tab = ui.tab("history", label="History", icon="history")
            with ui.tab_panels(tabs, value=live_tab).classes("w-full bg-transparent"):
                with ui.tab_panel(live_tab).classes("px-0"):
                    if not selectable:
                        with ui.card().classes("panel-card w-full"):
                            ui.label("No active or restartable runtime run").classes("section-title")
                            ui.label("Start an approved candidate experiment from New Experiment. Historical finalized runs remain available under History.").classes("muted text-sm")
                            ui.button("New Experiment", icon="add", on_click=lambda: ui.navigate.to("/experiment")).props("flat no-caps")
                    else:
                        ui.select(
                            {item.run_id: f"{item.run_id} · {item.status.value}" for item in selectable},
                            value=selected["run_id"],
                            label="Runtime run",
                            on_change=lambda event: (selected.update(run_id=str(event.value)), run_workspace.refresh()),
                        ).props("outlined dense").classes("w-full max-w-xl")
                        chosen = next((item for item in runs if item.run_id == selected["run_id"]), None)
                        if chosen is not None:
                            _render_live_run(chosen)
                with ui.tab_panel(history_tab).classes("px-0"):
                    if not runs:
                        ui.label("No runtime or historical runs are available.").classes("muted")
                    else:
                        ui.aggrid(
                            {
                                "columnDefs": [
                                    {"headerName": "Run", "field": "run_id", "minWidth": 230, "pinned": "left"},
                                    {"headerName": "Status", "field": "status", "width": 125, "filter": True},
                                    {"headerName": "Progress", "field": "progress", "width": 145},
                                    {"headerName": "Attempt", "field": "attempt", "width": 95},
                                    {"headerName": "Created (UTC)", "field": "started_at_utc", "minWidth": 190},
                                    {"headerName": "Updated (UTC)", "field": "updated_at_utc", "minWidth": 190},
                                ],
                                "rowData": _runtime_table_rows(runs),
                                "defaultColDef": {"sortable": True, "filter": True, "resizable": True},
                                "pagination": True,
                                "paginationPageSize": 20,
                            },
                            modules="community",
                        ).classes("w-full h-[620px]")

        run_workspace()
        ui.timer(1.0, run_workspace.refresh)


@ui.page("/compare", title=f"{APP_TITLE} · Compare")
def compare_page() -> None:
    with page_shell(
        "Compare agent resilience",
        "Stored historical v1.0 evidence is shown with its actual SD. Candidate v1.1 paired 95% CIs will appear only after the scientific freeze/final evidence path produces them.",
        eyebrow="Compare",
    ):
        frame = READ_MODEL.v10_aggregated_summary()
        if frame is None:
            with ui.row().classes("status-strip status-warning w-full items-center gap-2"):
                ui.icon("warning_amber")
                ui.label("The historical aggregated summary artifact is unavailable or unreadable.")
            return

        with ui.row().classes("status-strip w-full items-center gap-2"):
            ui.icon("history")
            ui.label("Currently showing immutable protocol-v1.0 historical finalized evidence. v1.1 candidate/tuning telemetry is not promoted here as final evidence.")
        metrics = [
            metric
            for metric in ("post_change_mean", "cumulative_deficit", "immediate_degradation", "nominal_mean")
            if (metric, "mean") in frame.columns
        ]
        with ui.card().classes("panel-card w-full"):
            with ui.row().classes("w-full items-end gap-4"):
                metric_select = ui.select(
                    {metric: METRIC_LABELS.get(metric, metric) for metric in metrics},
                    value=metrics[0],
                    label="Metric",
                ).props("outlined dense").classes("min-w-72")
                ui.label("Bars = mean; v1.0 error bars = SD, not confidence intervals.").classes("muted text-xs pb-2")
            plot = ui.plotly(_plot_payload(aggregated_metric_figure(frame, metrics[0]))).classes("w-full h-[620px]")

            def change_metric(event: Any) -> None:
                plot.figure = _plot_payload(aggregated_metric_figure(frame, str(event.value)))
                plot.update()

            metric_select.on_value_change(change_metric)

        with ui.card().classes("panel-card w-full"):
            ui.label("Condition × agent overview").classes("section-title")
            ui.plotly(_plot_payload(metric_heatmap_figure(frame, "cumulative_deficit"))).classes("w-full h-[520px]")


@ui.page("/artifacts", title=f"{APP_TITLE} · Artifacts")
def artifacts_page() -> None:
    with page_shell(
        "Evidence and export artifacts",
        "Inspect and download existing thesis-final artifacts. Files are presented as stored evidence; the UI does not silently regenerate or replace them.",
        eyebrow="Artifacts",
    ):
        artifacts = READ_MODEL.thesis_final_artifacts()
        if not artifacts:
            ui.label("No thesis-final artifacts were found.").classes("muted")
            return
        rows = [
            {
                "name": item["name"],
                "type": item["suffix"].lstrip(".").upper() or "FILE",
                "size_kib": round(item["size_bytes"] / 1024, 1),
            }
            for item in artifacts
        ]
        with ui.grid(columns=2).classes("w-full gap-5"):
            with ui.card().classes("panel-card w-full"):
                ui.label("Artifact index").classes("section-title")
                ui.aggrid(
                    {
                        "columnDefs": [
                            {"headerName": "Artifact", "field": "name", "flex": 1},
                            {"headerName": "Type", "field": "type", "width": 100},
                            {"headerName": "Size (KiB)", "field": "size_kib", "width": 120},
                        ],
                        "rowData": rows,
                        "defaultColDef": {"sortable": True, "filter": True, "resizable": True},
                    },
                    modules="community",
                ).classes("w-full h-96")
            with ui.card().classes("panel-card w-full"):
                ui.label("Downloads").classes("section-title")
                ui.label("Downloading does not modify scientific evidence.").classes("muted text-sm")
                with ui.column().classes("w-full gap-2"):
                    for item in artifacts:
                        with ui.row().classes("w-full items-center no-wrap border border-slate-200 rounded-xl p-2"):
                            ui.icon("description").classes("text-primary")
                            ui.label(item["name"]).classes("text-sm")
                            ui.space()
                            ui.button(
                                "Download",
                                icon="download",
                                on_click=lambda path=item["path"]: ui.download.file(str(path)),
                            ).props("flat dense no-caps")


def main() -> None:
    """Start the application in native desktop mode or explicit CI/browser mode."""
    multiprocessing.freeze_support()
    browser_mode = os.environ.get("THESIS_APP_BROWSER_MODE", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    if browser_mode:
        port = int(os.environ.get("THESIS_APP_PORT", "8501"))
        ui.run(
            title=APP_TITLE,
            host="127.0.0.1",
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


if __name__ in {"__main__", "__mp_main__"}:
    main()
