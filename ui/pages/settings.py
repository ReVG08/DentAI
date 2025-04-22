import streamlit as st

def render_settings_page():
    """
    Renders the multi-tab settings page and saves all values to st.session_state.
    Categories: Profile, Theme, Report, Language, Notifications, Data/Privacy, Integrations, AI.
    """
    st.title("⚙️ Settings")

    st.session_state.setdefault("user_profile", {})
    st.session_state.setdefault("theme", {"mode": "Light"})
    st.session_state.setdefault("report_customization", {})
    st.session_state.setdefault("language", {"lang": "English"})
    st.session_state.setdefault("notifications", {})
    st.session_state.setdefault("data_privacy", {})
    st.session_state.setdefault("crm_settings", {"type": "None"})
    st.session_state.setdefault("api_keys", {})
    st.session_state.setdefault("ai_settings", {})

    tabs = st.tabs([
        "User Profile", "Theme & Appearance", "Report Customization", 
        "Language & Localization", "Notifications", "Data & Privacy", 
        "API & Integrations", "AI Advanced"
    ])
    
    # 1. User Profile Tab
    with tabs[0]:
        st.subheader("👤 User/Clinic Profile")
        profile = st.session_state["user_profile"]
        profile["name"] = st.text_input("Name", profile.get("name", ""))
        profile["email"] = st.text_input("Email", profile.get("email", ""))
        profile["contact"] = st.text_input("Contact Number", profile.get("contact", ""))
        logo = st.file_uploader("Upload Clinic Logo", type=["jpg", "jpeg", "png"], key="clinic_logo")
        if logo:
            st.image(logo, width=100)
            profile["logo"] = logo.getvalue()
        st.session_state["user_profile"] = profile

    # 2. Theme Tab
    with tabs[1]:
        st.subheader("🎨 Theme & Appearance")
        theme = st.session_state["theme"]
        theme["mode"] = st.selectbox("Theme", ["Light", "Dark"], index=["Light", "Dark"].index(theme.get("mode", "Light")))
        theme["primary_color"] = st.color_picker("Primary Color", theme.get("primary_color", "#0066cc"))
        st.session_state["theme"] = theme
        st.info("To apply Streamlit theming, set these colors in .streamlit/config.toml.")

    # 3. Report Customization Tab
    with tabs[2]:
        st.subheader("📝 PDF Report Customization")
        rc = st.session_state["report_customization"]
        rc["footer"] = st.text_input("Custom footer/disclaimer for reports", rc.get("footer", ""))
        rc["include_sections"] = st.multiselect(
            "Sections to include in PDF",
            ["Summary", "Detailed Analysis", "Patient Info", "AI Explanation", "Images"],
            default=rc.get("include_sections", ["Summary", "Detailed Analysis", "Patient Info"])
        )
        st.session_state["report_customization"] = rc

    # 4. Language & Localization Tab
    with tabs[3]:
        st.subheader("🌐 Language & Localization")
        lang = st.session_state["language"]
        lang["lang"] = st.selectbox("Report/UI Language", ["English", "Spanish", "French", "German"], index=["English", "Spanish", "French", "German"].index(lang.get("lang", "English")))
        lang["date_format"] = st.selectbox("Date Format", ["YYYY-MM-DD", "DD/MM/YYYY", "MM/DD/YYYY"], index=0)
        st.session_state["language"] = lang

    # 5. Notifications Tab
    with tabs[4]:
        st.subheader("🔔 Notifications")
        notif = st.session_state["notifications"]
        notif["email_enabled"] = st.checkbox("Enable email notifications", notif.get("email_enabled", False))
        notif["recipients"] = st.text_input("Notification recipients (comma-separated emails)", notif.get("recipients", ""))
        st.session_state["notifications"] = notif

    # 6. Data & Privacy Tab
    with tabs[5]:
        st.subheader("🔒 Data Management & Privacy")
        data = st.session_state["data_privacy"]
        if st.button("Clear analysis history"):
            st.session_state["history"] = []
            st.success("History cleared!")
        data["retention_days"] = st.number_input("Data retention (days)", min_value=1, max_value=3650, value=data.get("retention_days", 365))
        data["anonymize"] = st.checkbox("Anonymize patient data in reports", data.get("anonymize", False))
        st.session_state["data_privacy"] = data

    # 7. API & Integrations Tab
    with tabs[6]:
        st.subheader("🔗 Integrations")
        crm = st.session_state["crm_settings"]
        crm["type"] = st.selectbox("CRM System", ["None", "DentalCRM", "Other"], index=["None", "DentalCRM", "Other"].index(crm.get("type", "None")))
        if crm["type"] != "None":
            crm["api_endpoint"] = st.text_input("CRM API Endpoint", crm.get("api_endpoint", ""))
            crm["username"] = st.text_input("CRM Username", crm.get("username", ""))
            crm["password"] = st.text_input("CRM Password", crm.get("password", ""), type="password")
            crm["auto_export"] = st.checkbox("Automatically export reports to CRM", crm.get("auto_export", False))
        st.session_state["crm_settings"] = crm

        st.markdown("---")
        st.subheader("🔑 API Keys")
        api_keys = st.session_state["api_keys"]
        api_keys["openai"] = st.text_input("OpenAI API Key", api_keys.get("openai", ""), type="password")
        api_keys["other_api"] = st.text_input("Other API Key", api_keys.get("other_api", ""), type="password")
        st.session_state["api_keys"] = api_keys

    # 8. AI Advanced Tab
    with tabs[7]:
        st.subheader("🤖 Advanced AI Settings")
        ai = st.session_state["ai_settings"]
        ai["model"] = st.selectbox("OpenAI Model", ["gpt-4", "gpt-3.5-turbo"], index=["gpt-4", "gpt-3.5-turbo"].index(ai.get("model", "gpt-4")))
        ai["temperature"] = st.slider("AI Temperature (creativity)", 0.0, 1.0, float(ai.get("temperature", 0.4)))
        ai["max_tokens"] = st.number_input("Max Tokens (response length)", min_value=100, max_value=3000, value=int(ai.get("max_tokens", 1024)))
        st.session_state["ai_settings"] = ai

    st.success("Settings saved! They will be used in future analyses and reports.")
