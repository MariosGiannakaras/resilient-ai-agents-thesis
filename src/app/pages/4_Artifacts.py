import sys
from pathlib import Path

import streamlit as st

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root / "src") not in sys.path:
    sys.path.insert(0, str(repo_root / "src"))

st.set_page_config(page_title="Artifacts", page_icon="📦", layout="wide")

st.title("Generate Artifacts")

st.markdown("""
Generate and export figures, tables, CSV/JSON exports, and manifests for the thesis.
""")

st.info("Artifact generation requires completed evaluation matrices.")
