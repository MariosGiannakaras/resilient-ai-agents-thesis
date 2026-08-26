import sys
from pathlib import Path

import streamlit as st

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root / "src") not in sys.path:
    sys.path.insert(0, str(repo_root / "src"))

st.set_page_config(page_title="Compare", page_icon="📊", layout="wide")

st.title("Compare Runs")

st.markdown("""
Select multiple completed runs to compare performance, degradation, recovery, and variability.
""")

st.info("Comparison features will be enabled after sufficient valid evaluation data is collected.")
