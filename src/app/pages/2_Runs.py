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

st.markdown("Monitor active experiments, view historical run metadata, and inspect configurations.")

tab1, tab2 = st.tabs(["History", "Run Detail"])

registry = ExperimentRegistry(repo_root)

with tab1:
    st.subheader("Run History", help="Complete list of all finalized experiment runs.")
    runs = registry.list_runs()
    
    if runs:
        # Convert to DataFrame for easy filtering and display
        df = pd.DataFrame(runs)
        
        # Ensure key columns exist
        for col in ["run_id", "status", "protocol_version", "stage", "started_at_utc"]:
            if col not in df.columns:
                df[col] = "Unknown"
        
        # Add visual status column
        def get_icon(status):
            if status == "completed": return "✅"
            if status == "failed": return "❌"
            if status == "cancelled": return "🛑"
            return "🔄"
            
        df[" "] = df["status"].apply(get_icon)
        
        # Select important columns
        display_df = df[[" ", "run_id", "status", "protocol_version", "stage", "started_at_utc"]]
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No runs found in history. Use the New Experiment tab to launch one.", icon="ℹ️")

with tab2:
    st.subheader("Run Detail", help="Inspect detailed manifest and configuration of a specific run.")
    runs = registry.list_runs()
    if runs:
        run_ids = [r.get("run_id") for r in runs if "run_id" in r]
        selected_run_id = st.selectbox(
            "Select Run", 
            options=run_ids,
            help="Select a run to view its resolved configuration, metadata, and final status."
        )
        
        if selected_run_id:
            details = registry.get_run(selected_run_id)
            if details:
                manifest = details['manifest']
                status_val = manifest.get('status')
                
                # Semantic header
                if status_val == "completed":
                    st.success(f"Run {selected_run_id} completed successfully.", icon="✅")
                elif status_val == "failed":
                    st.error(f"Run {selected_run_id} failed.", icon="❌")
                elif status_val == "cancelled":
                    st.warning(f"Run {selected_run_id} was cancelled.", icon="🛑")
                else:
                    st.info(f"Run {selected_run_id} status: {status_val}")
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Protocol", manifest.get('protocol_version'))
                col2.metric("Stage", manifest.get('stage'))
                col3.metric("Started", manifest.get('started_at_utc', 'N/A').split('T')[0] if 'T' in manifest.get('started_at_utc', '') else 'N/A')
                
                with st.expander("📦 Manifest", expanded=False):
                    st.markdown("Cryptographic checksums and output inventory.")
                    st.json(manifest)
                with st.expander("⚙️ Resolved Configuration", expanded=True):
                    st.markdown("Exact parameters used for execution.")
                    st.json(details['config'])
            else:
                st.warning("Could not load details for this run.", icon="⚠️")
    else:
        st.info("No runs available to inspect.", icon="ℹ️")
