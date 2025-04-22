import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

# --- User database (replace with DB in production) ---
if not os.path.exists("users.yaml"):
    with open("users.yaml", "w") as f:
        yaml.dump({"credentials": {"usernames": {}}}, f)

with open("users.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# --- Authenticator setup ---
authenticator = stauth.Authenticate(
    config['credentials'],
    "dental_ai_app",
    "abcdef",  # Cookie key
    cookie_expiry_days=3
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.success(f"Welcome {name}!")
    # User's API key management
    api_key = st.text_input("OpenAI API Key", type="password", value=config['credentials']['usernames'][username].get("api_key", ""))
    if st.button("Save API Key"):
        config['credentials']['usernames'][username]["api_key"] = api_key
        with open("users.yaml", "w") as file:
            yaml.dump(config, file)
        st.success("API key saved!")

    st.write("Your app features go here...")

    authenticator.logout("Logout", "sidebar")

elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")

# Registration (optional, can be disabled)
try:
    if st.button("Register New User"):
        authenticator.register_user("Register", preauthorization=False)
except Exception as e:
    st.error(e)