import streamlit as st
from typing import Dict, Any, List
from PIL import Image
from datetime import datetime

def anonymize_patient_info(patient_info: Dict[str, Any]) -> Dict[str, Any]:
    """Return anonymized patient info if enabled."""
    privacy = st.session_state.get("data_privacy", {})
    if privacy.get("anonymize", False):
        return {
            "name": "Anonymous",
            "age": patient_info.get("age"),
            "gender": patient_info.get("gender"),
            "complaint": patient_info.get("complaint"),
            "medical_history": patient_info.get("medical_history")
        }
    return patient_info

def render_analysis_page():
    """
    Render the analysis page, tying in settings for AI, report customization, language, profile, and privacy.
    """
    st.header("🦷 Patient Dental Analysis")

    api_keys = st.session_state.get("api_keys", {})
    if not api_keys.get("openai"):
        st.info("🔑 Please enter your OpenAI API key in the settings to continue.")
        return

    # AI engine settings
    ai_settings = st.session_state.get("ai_settings", {})
    ai_engine = st.session_state.get("ai_engine")
    report_generator = st.session_state.get("report_generator")
    image_processor = st.session_state.get("image_processor")

    # Assume these objects use st.session_state settings on initialization elsewhere (in main app)
    if not ai_engine or not report_generator or not image_processor:
        st.error("❌ Unable to initialize AI components. Please check your API key and settings.")
        return

    with st.form("patient_form", clear_on_submit=False):
        st.subheader("👤 Patient Information")
        col1, col2 = st.columns(2)
        with col1:
            patient_name = st.text_input("Patient Name", key="patient_name")
            patient_age = st.number_input("Age", min_value=0, max_value=120, value=30, step=1, key="patient_age")
            patient_gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="patient_gender")
        with col2:
            patient_complaint = st.text_area("Primary Complaint", key="patient_complaint")
            patient_history = st.text_area("Medical History", key="patient_history")

        st.subheader("🖼️ Dental Images")
        uploaded_files = st.file_uploader(
            "Upload dental X-rays or intraoral images", 
            type=["jpg", "jpeg", "png"], 
            accept_multiple_files=True,
            key="dental_images"
        )
        submitted = st.form_submit_button("Analyze Images")

    images = []
    if uploaded_files:
        st.write(f"**{len(uploaded_files)} image(s) uploaded.**")
        cols = st.columns(min(3, len(uploaded_files)))
        for i, file in enumerate(uploaded_files):
            img = Image.open(file)
            images.append(img)
            cols[i % len(cols)].image(img, caption=f"Image {i+1}", use_column_width=True)

    if submitted:
        if not images:
            st.error("❗ Please upload at least one dental image for analysis.")
            return
        if not patient_name:
            st.error("❗ Please enter patient name.")
            return

        patient_info = {
            "name": patient_name,
            "age": patient_age,
            "gender": patient_gender,
            "complaint": patient_complaint,
            "medical_history": patient_history,
        }
        # Apply anonymization if set
        patient_info_to_use = anonymize_patient_info(patient_info)

        with st.spinner("Processing and analyzing images..."):
            try:
                processed_images = image_processor.process_batch(images)
                # Language and AI settings integration
                lang = st.session_state.get("language", {}).get("lang", "English")
                date_fmt = st.session_state.get("language", {}).get("date_format", "YYYY-MM-DD")
                analysis = ai_engine.analyze_images(
                    processed_images, 
                    patient_info_to_use,
                    model=ai_settings.get("model", "gpt-4"),
                    temperature=ai_settings.get("temperature", 0.4),
                    max_tokens=ai_settings.get("max_tokens", 1024),
                    language=lang
                )
                # Report customization
                report_settings = st.session_state.get("report_customization", {})
                detailed_report = report_generator.generate_detailed_report(
                    analysis, patient_info_to_use, language=lang, date_format=date_fmt,
                    include_sections=report_settings.get("include_sections", []),
                    footer=report_settings.get("footer", "")
                )
                summary_report = report_generator.generate_summary_report(
                    analysis, patient_info_to_use, language=lang, date_format=date_fmt,
                    include_sections=report_settings.get("include_sections", []),
                    footer=report_settings.get("footer", "")
                )

                results = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "patient_info": patient_info_to_use,
                    "raw_analysis": analysis,
                    "detailed_report": detailed_report,
                    "summary_report": summary_report
                }
                st.session_state.current_analysis = results

                # Save to history
                st.session_state.setdefault("history", []).append({
                    "timestamp": results["timestamp"],
                    "patient": patient_info_to_use["name"],
                    "results": results
                })

                st.success("✅ Analysis complete!")
                display_analysis_results(results)
            except Exception as e:
                st.error(f"⚠️ Error during analysis: {str(e)}")

def display_analysis_results(results: Dict[str, Any]):
    """Display AI analysis results and download options, using CRM settings and branding."""
    # Branding
    profile = st.session_state.get("user_profile", {})
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        if "logo" in profile and profile["logo"]:
            st.image(profile["logo"], width=70)
    with col_title:
        st.markdown(f"#### Clinic: {profile.get('name', 'Dental Clinic')}")
        if profile.get("contact", ""):
            st.caption(f"Contact: {profile['contact']}")

    st.subheader("📄 Summary Report")
    st.info("This concise report is for the doctor to review and sign.")
    st.markdown(results["summary_report"], unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="⬇️ Download Summary Report (TXT)",
            data=results["summary_report"].encode(),
            file_name=f"dental_summary_{results['timestamp'].replace(':', '-').replace(' ', '_')}.txt",
            mime="text/plain"
        )

    st.subheader("📝 Detailed Report")
    st.info("Full reasoning and AI explanation.")
    with st.expander("Show Detailed Report"):
        st.markdown(results["detailed_report"], unsafe_allow_html=True)
    with col2:
        st.download_button(
            label="⬇️ Download Detailed Report (TXT)",
            data=results["detailed_report"].encode(),
            file_name=f"dental_detailed_{results['timestamp'].replace(':', '-').replace(' ', '_')}.txt",
            mime="text/plain"
        )

    # CRM export option
    crm_settings = st.session_state.get("crm_settings", {})
    if crm_settings.get("type") and crm_settings["type"] != "None":
        if st.button("🔗 Export to CRM"):
            # Place to add actual CRM export logic
            st.success("Export to CRM triggered! (integration not implemented here)")
