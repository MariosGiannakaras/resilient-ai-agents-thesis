import sys
from pathlib import Path

import streamlit as st

repo_root = Path(__file__).resolve().parents[2]
if str(repo_root / "src") not in sys.path:
    sys.path.insert(0, str(repo_root / "src"))

from resilient_agents.experiment_manager import ExperimentRegistry, get_resource_snapshot

st.set_page_config(
    page_title="Resilient Agents Dashboard",
    page_icon="🛡️",
    layout="wide",
)

st.title("Resilient AI Agents Dashboard")

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
    
col1, col2, col3 = st.columns(3)
if "hardware" in status:
    cpu = status["hardware"].get("cpu", {})
    ram = status["hardware"].get("ram", {})
    col1.metric("CPU Cores", cpu.get("logical_cores", "N/A"))
    col2.metric("Total RAM", f"{ram.get('total_gb', 0):.1f} GB")
    col3.metric("Available RAM", f"{ram.get('available_gb', 0):.1f} GB")

st.subheader("Recent Runs")
registry = ExperimentRegistry(repo_root)
runs = registry.list_runs()

if runs:
    # Display the 5 most recent runs
    recent = sorted(runs, key=lambda r: r.get("started_at_utc", ""), reverse=True)[:5]
    for r in recent:
        st.write(f"**{r.get('run_id')}** - {r.get('status')} - Protocol: {r.get('protocol_version')}")
else:
    st.info("No completed runs found. Go to 'New Experiment' to start one.")
