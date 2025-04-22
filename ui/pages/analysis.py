# ... (most code unchanged)
from src.pdf-generator import PDFGenerator

def display_analysis_results(results: Dict[str, Any]):
    st.subheader("Summary Report")
    st.info("This is the concise report for the doctor to review and sign.")
    st.markdown(results["summary_report"])

    # PDF settings from session
    clinic_settings = st.session_state.get("clinic_settings", {})
    pdfgen = PDFGenerator(
        logo_path=None,
        watermark_path=None,
        footer_note=clinic_settings.get("pdf_footer_note"),
        show_signature_block=clinic_settings.get("show_signature_block", True),
        show_patient_id=clinic_settings.get("show_patient_id", False),
    )

    # Save logo/watermark to temp file if needed (Streamlit file_uploader returns BytesIO)
    import tempfile, os
    logo_path = None
    if clinic_settings.get("clinic_logo"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(clinic_settings["clinic_logo"].getbuffer())
            logo_path = tmp.name
    watermark_path = None
    if clinic_settings.get("pdf_watermark"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(clinic_settings["pdf_watermark"].getbuffer())
            watermark_path = tmp.name

    pdfgen.logo_path = logo_path
    pdfgen.watermark_path = watermark_path

    # Clinic info
    clinic_name = clinic_settings.get("clinic_name", "Dental Clinic")
    clinic_email = clinic_settings.get("clinic_email", "")
    clinic_phone = clinic_settings.get("clinic_phone", "")
    clinic_address = clinic_settings.get("clinic_address", "")

    summary_pdf = pdfgen.generate_summary_pdf(
        results["patient_info"], results["summary_report"], 
        clinic_name=clinic_name, clinic_email=clinic_email, clinic_phone=clinic_phone, clinic_address=clinic_address
    )
    detailed_pdf = pdfgen.generate_detailed_pdf(
        results["patient_info"], results["detailed_report"], 
        clinic_name=clinic_name, clinic_email=clinic_email, clinic_phone=clinic_phone, clinic_address=clinic_address
    )

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="Download Summary Report (PDF)",
            data=summary_pdf,
            file_name=f"dental_summary_{results['timestamp'].replace(':', '-').replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
    st.subheader("Detailed Report")
    st.info("This report explains the reasoning behind the analysis in detail.")
    with st.expander("View Detailed Report"):
        st.markdown(results["detailed_report"])
    with col2:
        st.download_button(
            label="Download Detailed Report (PDF)",
            data=detailed_pdf,
            file_name=f"dental_detailed_{results['timestamp'].replace(':', '-').replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
    # Clean up temp files
    if logo_path: os.unlink(logo_path)
    if watermark_path: os.unlink(watermark_path)

    if st.session_state.crm_settings["type"] != "None":
        st.button("Export to CRM", key="export_to_crm")