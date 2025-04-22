import streamlit as st

def render_history_page():
    """
    Show analysis history, leveraging all saved report settings and anonymization.
    """
    st.title("⏳ Analysis History")
    history = st.session_state.get("history", [])
    anonymize = st.session_state.get("data_privacy", {}).get("anonymize", False)
    if not history:
        st.info("No analysis history yet. Previous analyses will appear here.")
        return

    for entry in reversed(history):
        patient_label = entry['patient'] if not anonymize else "Anonymous"
        with st.expander(f"🧑 {patient_label} — {entry['timestamp']}"):
            results = entry["results"]
            st.write("**📄 Summary Report:**")
            st.markdown(results["summary_report"], unsafe_allow_html=True)
            st.write("**📝 Detailed Report:**")
            st.markdown(results["detailed_report"], unsafe_allow_html=True)
            st.write("**👤 Patient Info:**")
            st.json(results["patient_info"])
            st.write("**🤖 AI Raw Analysis:**")
            st.json(results["raw_analysis"])
