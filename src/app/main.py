import sys
from pathlib import Path

import streamlit as st

repo_root = Path(__file__).resolve().parents[2]
if str(repo_root / "src") not in sys.path:
    sys.path.insert(0, str(repo_root / "src"))

from resilient_agents.experiment_manager import ExperimentRegistry, get_resource_snapshot
from app.components.onboarding import show_onboarding, onboarding_replay_button

st.set_page_config(
    page_title="Resilient Agents Dashboard",
    page_icon="🔬",
    layout="wide",
)

st.title("Resilient AI Agents Dashboard")

onboarding_replay_button()
show_onboarding()

st.markdown("""
Welcome to the experiment dashboard for the resilient AI agents thesis.

Use the sidebar to navigate to:
- **New Experiment**: Configure and launch valid experiment campaigns.
- **Runs**: Monitor active runs, inspect history, and view details.
- **Compare**: Compare completed runs against each other.
- **Artifacts**: Generate thesis artifacts and figures.
""")

st.subheader("System Status")
with st.spinner("Loading system snapshot..."):
    status = get_resource_snapshot(repo_root)

if status.get("status") == "unavailable":
    st.warning("System inventory is currently unavailable.", icon="⚠️")
else:
    col1, col2, col3 = st.columns(3)
    cpu = status.get("cpu", {})
    memory = status.get("memory", {})
    storage = status.get("storage", {})
    
    col1.metric(
        "CPU Cores", 
        cpu.get("logical_processors", "N/A"),
        help="Number of logical processors available for parallel environment execution."
    )
    
    total_bytes = memory.get("total_bytes", 0)
    col2.metric(
        "Total RAM", 
        f"{total_bytes / (1024**3):.1f} GB" if total_bytes else "N/A",
        help="Total physical memory on the system."
    )
    
    repo_fs = storage.get("repo_filesystem", {})
    free_bytes = repo_fs.get("free_bytes", 0)
    col3.metric(
        "Free Disk", 
        f"{free_bytes / (1024**3):.1f} GB" if free_bytes else "N/A",
        help="Remaining storage space on the partition hosting the thesis repository."
    )

st.subheader("Recent Runs")
registry = ExperimentRegistry(repo_root)
runs = registry.list_runs()

if runs:
    recent = sorted(runs, key=lambda r: r.get("started_at_utc", ""), reverse=True)[:5]
    for r in recent:
        status_val = r.get("status")
        # Semantic statuses
        if status_val == "completed":
            icon = "✅"
            color = "green"
        elif status_val == "failed":
            icon = "❌"
            color = "red"
        elif status_val == "cancelled":
            icon = "🛑"
            color = "orange"
        else:
            icon = "🔄"
            color = "blue"
            
        st.markdown(
            f"{icon} **`{r.get('run_id')}`** — <span style='color:{color}'>{status_val}</span> — "
            f"Protocol: `{r.get('protocol_version')}`",
            unsafe_allow_html=True
        )
else:
    st.info("No completed runs found. Navigate to **New Experiment** to launch your first campaign.", icon="ℹ️")
