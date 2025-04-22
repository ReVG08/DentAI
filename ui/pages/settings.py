import streamlit as st

def render_settings_page():
    st.title("Settings")

    # --- Clinic & PDF Settings ---
    st.subheader("Clinic & PDF Report Settings")
    if "clinic_settings" not in st.session_state:
        st.session_state.clinic_settings = {
            "clinic_name": "",
            "clinic_logo": None,
            "clinic_email": "",
            "clinic_phone": "",
            "clinic_address": "",
            "pdf_footer_note": "",
            "pdf_watermark": None,
            "show_signature_block": True,
            "show_patient_id": False,
            "default_report_type": "Summary",
        }
    clinic_name = st.text_input("Clinic Name", value=st.session_state.clinic_settings.get("clinic_name", ""))
    clinic_logo = st.file_uploader("Clinic Logo (for PDF)", type=["jpg", "jpeg", "png"], key="clinic_logo")
    clinic_email = st.text_input("Clinic Email", value=st.session_state.clinic_settings.get("clinic_email", ""))
    clinic_phone = st.text_input("Clinic Phone Number", value=st.session_state.clinic_settings.get("clinic_phone", ""))
    clinic_address = st.text_area("Clinic Address", value=st.session_state.clinic_settings.get("clinic_address", ""))
    pdf_footer_note = st.text_area("PDF Footer Note / Custom Disclaimer",
                                   value=st.session_state.clinic_settings.get("pdf_footer_note", ""),
                                   help="This note will appear in the footer of all generated PDFs.")
    pdf_watermark = st.file_uploader("Custom Watermark for PDFs (optional)", type=["jpg", "jpeg", "png"], key="pdf_watermark")
    show_signature_block = st.checkbox("Include Doctor Signature Block in Report", value=st.session_state.clinic_settings.get("show_signature_block", True))
    show_patient_id = st.checkbox("Show Patient ID on Reports", value=st.session_state.clinic_settings.get("show_patient_id", False))
    default_report_type = st.selectbox("Default Report Type", ["Summary", "Detailed"], index=["Summary", "Detailed"].index(st.session_state.clinic_settings.get("default_report_type", "Summary")))

    # Save uploaded files and settings
    if clinic_logo is not None:
        st.session_state.clinic_settings["clinic_logo"] = clinic_logo
    if pdf_watermark is not None:
        st.session_state.clinic_settings["pdf_watermark"] = pdf_watermark
    st.session_state.clinic_settings["clinic_name"] = clinic_name
    st.session_state.clinic_settings["clinic_email"] = clinic_email
    st.session_state.clinic_settings["clinic_phone"] = clinic_phone
    st.session_state.clinic_settings["clinic_address"] = clinic_address
    st.session_state.clinic_settings["pdf_footer_note"] = pdf_footer_note
    st.session_state.clinic_settings["show_signature_block"] = show_signature_block
    st.session_state.clinic_settings["show_patient_id"] = show_patient_id
    st.session_state.clinic_settings["default_report_type"] = default_report_type

    st.divider()

    # --- CRM Integration ---
    st.subheader("CRM Integration")
    crm_type = st.selectbox("CRM System", ["None", "DentalCRM", "Other"], index=["None", "DentalCRM", "Other"].index(st.session_state.crm_settings.get("type", "None")))
    st.session_state.crm_settings["type"] = crm_type
    if crm_type != "None":
        st.text_input("CRM API Endpoint", key="crm_api_endpoint")
        st.text_input("CRM Username", key="crm_username")
        st.text_input("CRM Password", key="crm_password", type="password")
        auto_export = st.checkbox("Automatically export reports to CRM", key="crm_auto_export")
        st.session_state.crm_settings["auto_export"] = auto_export

    st.divider()

    # --- General Application Settings ---
    st.subheader("General Application Settings")
    debug_mode = st.checkbox("Enable Debug Mode", value=st.session_state.get("debug_mode", False))
    st.session_state["debug_mode"] = debug_mode

    default_language = st.selectbox("Default Language", ["English", "Spanish", "French", "German"], key="default_language")
    st.session_state["default_language"] = default_language

    keep_history = st.checkbox("Keep Analysis History", value=st.session_state.get("keep_history", True))
    st.session_state["keep_history"] = keep_history

    max_history_items = st.number_input("Max History Items to Store", min_value=1, max_value=100, value=st.session_state.get("max_history_items", 20), help="Limits the number of past analyses retained in the session.")
    st.session_state["max_history_items"] = max_history_items

    st.divider()

    # --- Security & Privacy ---
    st.subheader("Security & Privacy")
    auto_delete_days = st.number_input("Auto-Delete Analysis Data After (days)", min_value=0, max_value=365, value=st.session_state.get("auto_delete_days", 0), help="Set to 0 to disable auto-delete.")
    st.session_state["auto_delete_days"] = auto_delete_days

    encrypt_local_storage = st.checkbox("Encrypt Local Storage", value=st.session_state.get("encrypt_local_storage", False))
    st.session_state["encrypt_local_storage"] = encrypt_local_storage

    st.divider()

    # --- Team & Audit ---
    st.subheader("Team & Audit Log (coming soon)")
    st.info("User management and audit log features are coming soon.")

    st.divider()

    st.subheader("Other Settings")
    st.write("Suggest new features in the repository!")
