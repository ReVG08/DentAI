import streamlit as st

def render_history_page():
    st.title("Analysis History")
    history = st.session_state.get("history", [])
    if not history:
        st.info("No analysis history yet. Previous analyses will appear here.")
        return

    for entry in reversed(history):
        with st.expander(f"Patient: {entry['patient']} — {entry['timestamp']}"):
            results = entry["results"]
            st.write("**Summary Report:**")
            st.markdown(results["summary_report"])
            st.write("**Detailed Report:**")
            st.markdown(results["detailed_report"])
            st.write("**Patient Info:**")
            st.json(results["patient_info"])
            st.write("**AI Raw Analysis:**")
            st.json(results["raw_analysis"])