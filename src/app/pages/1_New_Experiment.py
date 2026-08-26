import json
import sys
from pathlib import Path
import subprocess

import streamlit as st

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root / "src") not in sys.path:
    sys.path.insert(0, str(repo_root / "src"))

from resilient_agents.pilot_protocol import load_pilot_protocol

st.set_page_config(page_title="New Experiment", page_icon="??")

st.title("Configure New Experiment")

st.markdown("""
Select a validated protocol to configure and launch an experiment campaign.
""")

protocols_dir = repo_root / "configs" / "protocols"
protocol_files = list(protocols_dir.glob("*.json"))

if not protocol_files:
    st.error("No protocol configurations found.")
    st.stop()

selected_protocol = st.selectbox(
    "Protocol Version",
    options=protocol_files,
    format_func=lambda p: p.name
)

if selected_protocol:
    try:
        protocol = load_pilot_protocol(selected_protocol)
        payload = json.loads(selected_protocol.read_text(encoding="utf-8"))
        st.success(f"Protocol **{payload.get('protocol_version', 'Unknown')}** loaded successfully. Status: {payload.get('status', 'Unknown')}")
        
        st.subheader("Pre-run Review")
        
        col1, col2 = st.columns(2)
        with col1:
            agents = [a.get("agent_id", "Unknown") for a in payload.get('agent_regimes', [])]
            st.markdown(f"**Agents:** {', '.join(agents)}")
            layouts = payload.get('layouts', [])
            layout_ids = [l.get("layout_id", "Unknown") for l in layouts]
            st.markdown(f"**Layouts:** {', '.join(layout_ids) if layout_ids else 'See partitions'}")
        
        with col2:
            st.markdown(f"**Conditions:** {len(payload.get('conditions', []))}")
            st.markdown(f"**Root Seeds:** {len(payload.get('evaluation', {}).get('root_seeds', []))}")
            
        st.warning("Ensure that your target machine has enough resources for batch execution before launching.")
        
        if st.button("Launch Campaign"):
            script_path = repo_root / "scripts" / "run_final_campaign.py"
            # Launch detached so UI doesn't hang
            if sys.platform == "win32":
                subprocess.Popen(
                    [sys.executable, str(script_path), "--repo-root", str(repo_root), "--protocol", str(selected_protocol)],
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                subprocess.Popen(
                    [sys.executable, str(script_path), "--repo-root", str(repo_root), "--protocol", str(selected_protocol)],
                    start_new_session=True
                )
            
            st.info("Campaign launch requested. The campaign is running in the background. Active runs will appear in the Runs tab.")
            
    except Exception as e:
        st.error(f"Failed to load protocol: {e}")
