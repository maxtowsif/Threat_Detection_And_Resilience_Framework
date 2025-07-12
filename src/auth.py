import streamlit as st
import auth  # make sure this is in the same folder or adjust import path

# Load session if available
auth._load_persisted_session()

st.title("🔐 Login to Threat Detection System")

# -----------------------
# LOGIN FORM
# -----------------------
email = st.text_input("Email")
password = st.text_input("Password", type="password")

col1, col2 = st.columns([1, 3])
login_btn = col1.button("Login")
logout_btn = col2.button("Logout")

if login_btn:
    if auth.validate_login(email, password):
        st.success(f"Welcome, {email}")
    else:
        st.error("Invalid credentials.")

if logout_btn:
    auth.logout()
    st.info("You have been logged out.")

# -----------------------
# REGISTER NEW ACCOUNT
# -----------------------
with st.expander("Create a new account"):
    new_email = st.text_input("New Email")
    new_password = st.text_input("New Password", type="password")
    if st.button("Create Account"):
        if new_email and new_password:
            if auth.create_user(new_email, new_password):
                st.success("Account created successfully! Please log in.")
            else:
                st.warning("This user already exists.")
        else:
            st.warning("Please enter both an email and password.")

# -----------------------
# PROTECTED CONTENT
# -----------------------
if st.session_state.get("logged_in"):
    st.markdown("---")
    st.subheader("✅ Protected Dashboard")
    st.info("Only visible to logged-in users.")
    # Place your main app/dashboard components here
    st.write("You can now use the threat detection system.")
else:
    st.warning("Please log in to use the system.")
