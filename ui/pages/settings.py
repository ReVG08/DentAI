import streamlit as st

def render_settings_page():
    st.title("Settings")
    st.subheader("CRM Integration")
    crm_type = st.selectbox("CRM System", ["None", "DentalCRM", "Other"], index=0)
    st.session_state.crm_settings["type"] = crm_type

    if crm_type != "None":
        st.text_input("CRM API Endpoint", key="crm_api_endpoint")
        st.text_input("CRM Username", key="crm_username")
        st.text_input("CRM Password", key="crm_password", type="password")
        auto_export = st.checkbox("Automatically export reports to CRM", key="crm_auto_export")
        st.session_state.crm_settings["auto_export"] = auto_export

    st.subheader("Other Settings")
    st.write("No additional settings yet.")