import json
import sys
from pathlib import Path

import streamlit as st
import pandas as pd

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root / "src") not in sys.path:
    sys.path.insert(0, str(repo_root / "src"))

from resilient_agents.experiment_manager import ExperimentRegistry

st.set_page_config(page_title="Runs", page_icon="📋", layout="wide")

st.title("Experiment Runs")

tab1, tab2 = st.tabs(["History", "Run Detail"])

registry = ExperimentRegistry(repo_root)

with tab1:
    st.subheader("Run History")
    runs = registry.list_runs()
    
    if runs:
        # Convert to DataFrame for easy filtering and display
        df = pd.DataFrame(runs)
        
        # Ensure key columns exist
        for col in ["run_id", "status", "protocol_version", "started_at_utc"]:
            if col not in df.columns:
                df[col] = "Unknown"
        
        # Select important columns
        display_df = df[["run_id", "status", "protocol_version", "started_at_utc"]]
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No runs found in history.")

with tab2:
    st.subheader("Run Detail")
    runs = registry.list_runs()
    if runs:
        run_ids = [r.get("run_id") for r in runs if "run_id" in r]
        selected_run_id = st.selectbox("Select Run", options=run_ids)
        
        if selected_run_id:
            details = registry.get_run(selected_run_id)
            if details:
                st.write(f"**Status:** {details['manifest'].get('status')}")
                st.write(f"**Protocol:** {details['manifest'].get('protocol_version')}")
                
                with st.expander("Manifest"):
                    st.json(details['manifest'])
                with st.expander("Configuration"):
                    st.json(details['config'])
            else:
                st.warning("Could not load details for this run.")
    else:
        st.info("No runs available to inspect.")
