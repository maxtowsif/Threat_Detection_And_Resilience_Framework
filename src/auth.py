import streamlit as st
import auth  # Make sure auth.py is in /src and has no circular references

# Load session
auth._load_persisted_session()

# ---------------------------------
# LOGIN SYSTEM
# ---------------------------------

st.set_page_config(page_title="Threat Detection Login", page_icon="🛡️")
st.title("🛡️ Threat Detection & Resilience Framework")

# ---- Login Form ----
email = st.text_input("Email")
password = st.text_input("Password", type="password")

col1, col2 = st.columns([1, 2])
if col1.button("Login"):
    if auth.validate_login(email, password):
        st.success(f"Welcome, {email}!")
    else:
        st.error("Invalid email or password.")

if col2.button("Logout"):
    auth.logout()
    st.info("You have been logged out.")

# ---- Registration Form ----
with st.expander("🔑 Create a New Account"):
    new_email = st.text_input("New Email")
    new_password = st.text_input("New Password", type="password")
    if st.button("Create Account"):
        if new_email and new_password:
            if auth.create_user(new_email, new_password):
                st.success("Account created successfully. You may now log in.")
            else:
                st.warning("User already exists.")
        else:
            st.warning("Please enter both email and password.")

# ---------------------------------
# PROTECTED CONTENT
# ---------------------------------
if st.session_state.get("logged_in"):
    st.markdown("---")
    st.subheader("✅ Secure Dashboard")
    st.success("You are logged in and can use the system.")

    # PLACE YOUR DASHBOARD / SYSTEM BELOW
    st.info("⚙️ Main threat detection system would load here.")

else:
    st.warning("Log in to access protected features.")
