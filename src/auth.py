import streamlit as st
import auth  # your auth.py must be in the same folder or adjust path

# Load previous session (if any)
auth._load_persisted_session()

# ----------------------------
# LOGIN SECTION
# ----------------------------
st.title("🔐 User Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if auth.validate_login(email, password):
        st.success(f"Welcome, {email}!")
    else:
        st.error("Invalid credentials.")

if st.button("Logout"):
    auth.logout()
    st.info("You have been logged out.")

# ----------------------------
# REGISTRATION SECTION
# ----------------------------
with st.expander("Create New Account"):
    new_email = st.text_input("New Email")
    new_password = st.text_input("New Password", type="password")
    if st.button("Create Account"):
        if new_email and new_password:
            if auth.create_user(new_email, new_password):
                st.success("Account created successfully! Please log in.")
            else:
                st.warning("User already exists.")
        else:
            st.warning("Both fields are required.")

# ----------------------------
# PROTECTED CONTENT
# ----------------------------
if st.session_state.get("logged_in"):
    st.markdown("---")
    st.subheader("✅ Protected Area")
    st.success("You are logged in and can now use the system.")
else:
    st.warning("Log in to access the system features.")
