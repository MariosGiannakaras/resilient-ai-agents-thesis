"""Compare page: select and compare completed experiment runs.

Operates on real core data from ExperimentRegistry and the analysis module.
Shows compatibility warnings and metric comparisons when valid data exists.
"""
import json
import sys
from pathlib import Path

import streamlit as st
import pandas as pd

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root / "src") not in sys.path:
    sys.path.insert(0, str(repo_root / "src"))

from resilient_agents.experiment_manager import ExperimentRegistry

st.set_page_config(page_title="Compare", page_icon="📊", layout="wide")

st.title("Compare Runs")

st.markdown("""
Select completed runs to compare performance, degradation, recovery, and variability
across agents and conditions.
""")

registry = ExperimentRegistry(repo_root)
runs = registry.list_runs()

# Filter to completed runs only
completed_runs = [r for r in runs if r.get("status") == "completed"]

if not completed_runs:
    st.info(
        "No completed runs available for comparison. "
        "Complete experiments in the **New Experiment** tab first, "
        "then return here to compare results.",
        icon="ℹ️"
    )
    st.stop()

# Build a DataFrame for selection
df = pd.DataFrame(completed_runs)
for col in ("run_id", "status", "protocol_version", "stage", "started_at_utc"):
    if col not in df.columns:
        df[col] = "Unknown"

st.subheader("Select Runs to Compare", help="Only completed runs can be compared. Select runs from the same protocol version and stage to ensure scientific validity.")
selected_ids = st.multiselect(
    "Select two or more completed runs",
    options=df["run_id"].tolist(),
    help="Choose runs with the same protocol version for meaningful comparison.",
)

if len(selected_ids) < 2:
    st.info("Select at least two runs to compare.", icon="ℹ️")
    st.stop()

# Compatibility check
selected_df = df[df["run_id"].isin(selected_ids)]
protocols = selected_df["protocol_version"].unique()
stages = selected_df["stage"].unique()

if len(protocols) > 1:
    st.warning(
        f"Selected runs use different protocol versions: {', '.join(protocols)}. "
        "Cross-protocol comparison may not be scientifically meaningful.",
        icon="⚠️"
    )
if len(stages) > 1:
    st.warning(
        f"Selected runs span different stages: {', '.join(stages)}. "
        "Pilot and final evidence should not be mixed for inferential claims.",
        icon="⚠️"
    )

# Display comparison table
st.subheader("Run Summary", help="A high-level overview of the selected runs.")
display_cols = ["run_id", "protocol_version", "stage", "started_at_utc", "finished_at_utc"]
available_cols = [c for c in display_cols if c in selected_df.columns]
st.dataframe(selected_df[available_cols], use_container_width=True)

# Load summaries for selected runs
st.subheader("Run Details", help="Expand each run to view its specific manifest details and aggregate summary metrics.")
for run_id in selected_ids:
    details = registry.get_run(run_id)
    if details:
        with st.expander(f"📋 {run_id}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Status:** {details['manifest'].get('status')}")
                st.markdown(f"**Protocol:** {details['manifest'].get('protocol_version')}")
                st.markdown(f"**Stage:** {details['manifest'].get('stage')}")
            with col2:
                st.markdown(f"**Started:** {details['manifest'].get('started_at_utc', 'N/A')}")
                st.markdown(f"**Finished:** {details['manifest'].get('finished_at_utc', 'N/A')}")

            # Show summary if available
            summary_path = repo_root / "results" / "runs" / run_id / "summary.json"
            if summary_path.exists():
                try:
                    summary = json.loads(summary_path.read_text(encoding="utf-8"))
                    st.json(summary)
                except (json.JSONDecodeError, OSError):
                    st.warning("Could not load run summary.", icon="⚠️")
            else:
                st.info("No summary file available for this run.", icon="ℹ️")

# Link to analysis
st.divider()
st.subheader("Analysis Summaries", help="Aggregated statistical analyses generated from campaigns.")

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
                    with st.expander(f"📈 {analysis_dir.name}"):
                        st.markdown(
                            f"**Valid units:** {overview.get('valid_unit_count', 'N/A')}"
                        )
                        st.markdown(
                            f"**Sensitivity records:** "
                            f"{overview.get('sensitivity_record_count', 'N/A')}"
                        )
                        st.json(overview)
                except (json.JSONDecodeError, OSError):
                    pass
    else:
        st.info("No analysis summaries generated yet.", icon="ℹ️")
else:
    st.info(
        "No analysis summaries found. Run experiments and generate analyses "
        "to see comparisons here.", icon="ℹ️"
    )
