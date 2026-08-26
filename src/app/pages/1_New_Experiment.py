"""New Experiment page: configure and launch experiment campaigns.

Protocol/stage eligibility is validated explicitly:
- Only frozen protocols can launch final campaigns.
- Final-stage execution is blocked unless the T-511 lifecycle gate is satisfied.
- Development/smoke validation uses non-final partitions through the same core.
"""
import json
import sys
from pathlib import Path
import subprocess

import streamlit as st

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root / "src") not in sys.path:
    sys.path.insert(0, str(repo_root / "src"))

from resilient_agents.pilot_protocol import load_pilot_protocol

st.set_page_config(page_title="New Experiment", page_icon="🧪")

st.title("Configure New Experiment")

st.markdown("""
Select a validated protocol to configure and launch an experiment campaign.
""")

protocols_dir = repo_root / "configs" / "protocols"
protocol_files = sorted(protocols_dir.glob("*.json"))

if not protocol_files:
    st.error("No protocol configurations found in `configs/protocols/`.")
    st.stop()

selected_protocol = st.selectbox(
    "Protocol Version",
    options=protocol_files,
    format_func=lambda p: p.name,
)

if selected_protocol:
    try:
        protocol = load_pilot_protocol(selected_protocol)
        payload = json.loads(selected_protocol.read_text(encoding="utf-8"))
    except Exception as e:
        st.error(f"Failed to load protocol: {e}")
        st.stop()

    protocol_status = payload.get("status", "unknown")
    protocol_version = payload.get("protocol_version", "Unknown")

    st.success(f"Protocol **{protocol_version}** loaded. Status: `{protocol_status}`")

    st.subheader("Pre-run Review")

    col1, col2 = st.columns(2)
    with col1:
        agents = [a.get("agent_id", "?") for a in payload.get("agent_regimes", [])]
        st.markdown(f"**Agents:** {', '.join(agents)}")
        layouts = payload.get("layouts", [])
        layout_ids = [l.get("layout_id", "?") for l in layouts]
        st.markdown(f"**Layouts:** {', '.join(layout_ids)}")

    with col2:
        st.markdown(f"**Conditions:** {len(payload.get('conditions', []))}")
        eval_seeds = payload.get("evaluation", {}).get("root_seeds", [])
        st.markdown(f"**Root Seeds:** {len(eval_seeds)}")

    # Partitions summary
    partitions = payload.get("partitions", {})
    st.markdown("**Partitions:**")
    for stage_name, layout_list in partitions.items():
        count = len(layout_list) if isinstance(layout_list, list) else 0
        st.markdown(f"  - {stage_name}: {count} layout(s)")

    # Eligibility checks
    st.divider()

    is_frozen = protocol_status == "frozen"
    has_final_partition = bool(partitions.get("final"))

    # Check if T-511 gate is satisfied by inspecting TASKS.md
    tasks_path = repo_root / "docs" / "context" / "TASKS.md"
    t511_complete = False
    if tasks_path.exists():
        tasks_text = tasks_path.read_text(encoding="utf-8")
        import re
        t511_match = re.search(r"- \[x\] `T-511`", tasks_text)
        t511_complete = t511_match is not None

    if not is_frozen:
        st.warning(
            f"Protocol status is `{protocol_status}`. "
            "Only frozen protocols can be used for final campaigns."
        )

    if is_frozen and has_final_partition and not t511_complete:
        st.warning(
            "⚠️ **Final-reserve partition is protected.** "
            "Final experiment execution requires T-511 (application validation) "
            "to be completed first. This lifecycle gate protects the "
            "uncontaminated evaluation partition."
        )
        st.info(
            "💡 You can validate the dashboard/workflow using "
            "development or tuning partitions with the same scientific core."
        )

    if is_frozen and has_final_partition and t511_complete:
        st.success("✅ Protocol is frozen and lifecycle gate T-511 is satisfied.")
        if st.button("🚀 Launch Final Campaign"):
            script_path = repo_root / "scripts" / "run_final_campaign.py"
            cmd = [
                sys.executable,
                str(script_path),
                "--repo-root", str(repo_root),
                "--protocol", str(selected_protocol),
                "--allow-final",
            ]
            if sys.platform == "win32":
                subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen(cmd, start_new_session=True)
            st.info(
                "Campaign launch requested. The campaign is running in a "
                "separate process. Active runs will appear in the Runs tab."
            )
    elif not is_frozen:
        st.info("Configure and validate using this pilot/development protocol.")
    else:
        st.info(
            "Final campaign is locked. Use development/tuning partitions "
            "for workflow validation."
        )
