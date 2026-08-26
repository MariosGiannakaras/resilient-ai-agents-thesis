import streamlit as st

def show_onboarding():
    """Displays a lightweight skippable onboarding tutorial.
    Uses session state to remember completion."""
    if "onboarding_completed" not in st.session_state:
        st.session_state.onboarding_completed = False

    if not st.session_state.onboarding_completed:
        with st.expander("👋 Welcome to the Resilient Agents Dashboard! (Click to start tutorial)", expanded=True):
            st.markdown("### Getting Started")
            
            step = st.session_state.get("onboarding_step", 0)
            
            steps = [
                {
                    "title": "1. Dashboard",
                    "content": "This main page gives you a snapshot of your system resources and the most recent experiment runs. It's your starting point."
                },
                {
                    "title": "2. New Experiment",
                    "content": "Navigate here to configure and launch a new campaign. You must select an approved protocol. The system validates whether you can launch a final campaign or just a pilot."
                },
                {
                    "title": "3. Runs",
                    "content": "Monitor active experiments and view history. You can inspect logs, see live progress, and review completed or failed run metadata."
                },
                {
                    "title": "4. Compare",
                    "content": "Once you have completed runs, use this tab to compare their performance. The system will warn you if you try to compare incompatible protocols."
                },
                {
                    "title": "5. Artifacts",
                    "content": "Generate and export thesis-ready figures, tables, and JSON manifests. This relies on the validated analysis data."
                }
            ]
            
            st.markdown(f"**{steps[step]['title']}**")
            st.write(steps[step]["content"])
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if step > 0:
                    if st.button("Previous"):
                        st.session_state.onboarding_step = step - 1
                        st.rerun()
            with col2:
                if step < len(steps) - 1:
                    if st.button("Next"):
                        st.session_state.onboarding_step = step + 1
                        st.rerun()
                else:
                    if st.button("Finish"):
                        st.session_state.onboarding_completed = True
                        st.session_state.onboarding_step = 0
                        st.rerun()
            with col3:
                if st.button("Skip Tutorial"):
                    st.session_state.onboarding_completed = True
                    st.rerun()

def onboarding_replay_button():
    """Provides a button in the sidebar to replay the tutorial."""
    if st.sidebar.button("💡 Replay Tutorial"):
        st.session_state.onboarding_completed = False
        st.session_state.onboarding_step = 0
        st.rerun()
