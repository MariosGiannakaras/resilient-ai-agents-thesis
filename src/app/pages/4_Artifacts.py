"""Artifacts page: generate and export thesis-ready material.

Operates on real analysis data from results/summaries/ and completed runs.
Shows what evidence is available and what is needed before artifacts can
be generated.
"""
import json
import sys
from pathlib import Path

import streamlit as st

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root / "src") not in sys.path:
    sys.path.insert(0, str(repo_root / "src"))

from resilient_agents.experiment_manager import ExperimentRegistry

st.set_page_config(page_title="Artifacts", page_icon="📦", layout="wide")

st.title("Thesis Artifacts")

st.markdown("""
Generate figures, tables, CSV/JSON exports, and manifests for the thesis.
Artifacts are produced from validated analysis outputs and frozen evidence.
""")

registry = ExperimentRegistry(repo_root)
runs = registry.list_runs()

# Evidence inventory
st.subheader("Evidence Inventory")

completed = [r for r in runs if r.get("status") == "completed"]
failed = [r for r in runs if r.get("status") == "failed"]

col1, col2, col3 = st.columns(3)
col1.metric("Completed Runs", len(completed))
col2.metric("Failed Runs", len(failed))
col3.metric("Total Indexed", len(runs))

# Partition-based inventory
if completed:
    stages = {}
    for r in completed:
        stage = r.get("stage", "unknown")
        stages.setdefault(stage, []).append(r["run_id"])
    for stage_name, stage_runs in sorted(stages.items()):
        st.markdown(f"**{stage_name}:** {len(stage_runs)} completed runs")

# Analysis summaries
st.subheader("Analysis Summaries")
summaries_dir = repo_root / "results" / "summaries"

if summaries_dir.exists():
    analysis_dirs = sorted(
        [d for d in summaries_dir.iterdir() if d.is_dir()],
        key=lambda d: d.name,
    )
    if analysis_dirs:
        for analysis_dir in analysis_dirs:
            overview_path = analysis_dir / "analysis-overview.json"
            if overview_path.exists():
                try:
                    overview = json.loads(
                        overview_path.read_text(encoding="utf-8")
                    )
                    with st.expander(f"📊 {analysis_dir.name}", expanded=False):
                        st.markdown(
                            f"**Valid units:** "
                            f"{overview.get('valid_unit_count', 'N/A')}"
                        )
                        st.markdown(
                            f"**Sensitivity records:** "
                            f"{overview.get('sensitivity_record_count', 'N/A')}"
                        )

                        # Export buttons
                        overview_json = json.dumps(
                            overview, indent=2, ensure_ascii=False
                        )
                        st.download_button(
                            f"Download {analysis_dir.name} overview (JSON)",
                            overview_json,
                            file_name=f"{analysis_dir.name}-overview.json",
                            mime="application/json",
                        )

                        # Show full analysis files
                        analysis_files = sorted(analysis_dir.iterdir())
                        st.markdown("**Files in this analysis:**")
                        for f in analysis_files:
                            if f.is_file():
                                st.markdown(
                                    f"  - `{f.name}` "
                                    f"({f.stat().st_size:,} bytes)"
                                )
                except (json.JSONDecodeError, OSError) as exc:
                    st.warning(f"Could not load analysis: {exc}")
    else:
        st.info("No analysis summaries have been generated yet.")
else:
    st.info("No analysis directory found at `results/summaries/`.")

# Campaign state
st.subheader("Campaign State")
campaigns_dir = repo_root / "results" / "campaigns"
if campaigns_dir.exists():
    for campaign_dir in sorted(campaigns_dir.iterdir()):
        if campaign_dir.is_dir():
            state_path = campaign_dir / "campaign-state.json"
            if state_path.exists():
                try:
                    state = json.loads(
                        state_path.read_text(encoding="utf-8")
                    )
                    with st.expander(
                        f"🔬 {campaign_dir.name}", expanded=False
                    ):
                        st.markdown(
                            f"**Campaign ID:** "
                            f"{state.get('campaign_id', 'N/A')}"
                        )
                        st.markdown(
                            f"**Protocol:** "
                            f"{state.get('protocol_version', 'N/A')}"
                        )
                        if "tuning" in state:
                            selected = (
                                state["tuning"]
                                .get("selected", {})
                                .get("configuration", {})
                            )
                            if selected:
                                st.markdown("**Selected configuration:**")
                                st.json(selected)
                        if "pilot" in state:
                            pilot = state["pilot"]
                            st.markdown(
                                f"**Pilot runs:** "
                                f"{len(pilot.get('run_ids', []))}"
                            )
                            st.markdown(
                                f"**Valid units:** "
                                f"{pilot.get('valid_unit_count', 'N/A')}"
                            )

                        state_json = json.dumps(
                            state, indent=2, ensure_ascii=False
                        )
                        st.download_button(
                            f"Download {campaign_dir.name} state (JSON)",
                            state_json,
                            file_name=f"{campaign_dir.name}-state.json",
                            mime="application/json",
                        )
                except (json.JSONDecodeError, OSError) as exc:
                    st.warning(f"Could not load campaign state: {exc}")
else:
    st.info("No campaign data found.")

# Frozen evidence
st.divider()
st.subheader("Thesis Evidence Package")
thesis_final = repo_root / "results" / "thesis-final"
if thesis_final.exists() and any(thesis_final.iterdir()):
    st.success("Frozen thesis evidence is available.")
    for item in sorted(thesis_final.iterdir()):
        st.markdown(f"- `{item.name}`")
else:
    st.info(
        "No frozen thesis evidence package yet. "
        "This is generated after T-601 (final evidence freeze) is completed."
    )

# Protocol reference
st.divider()
st.subheader("Protocol Reference")
protocol_path = repo_root / "configs" / "protocols" / "protocol-v1.0.json"
if protocol_path.exists():
    try:
        protocol_data = json.loads(
            protocol_path.read_text(encoding="utf-8")
        )
        st.markdown(
            f"**Protocol version:** "
            f"{protocol_data.get('protocol_version', 'N/A')}"
        )
        st.markdown(
            f"**Status:** {protocol_data.get('status', 'N/A')}"
        )
        scope = protocol_data.get("scientific_scope", {})
        st.markdown(
            f"**Primary question:** "
            f"{scope.get('primary_question', 'N/A')}"
        )
        st.download_button(
            "Download protocol (JSON)",
            json.dumps(protocol_data, indent=2, ensure_ascii=False),
            file_name="protocol-v1.0.json",
            mime="application/json",
        )
    except (json.JSONDecodeError, OSError):
        st.warning("Could not load protocol file.")
else:
    st.info("No frozen protocol found.")
