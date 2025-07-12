# auth.py
import streamlit as st
import json
import os

SESSION_FILE = "data/session.json"
CREDENTIAL_FILE = "data/credentials.json"

# ---------------------------
# Session Management
# ---------------------------

def _persist_session(email):
    os.makedirs("data", exist_ok=True)
    with open(SESSION_FILE, "w") as f:
        json.dump({
            "logged_in": True,
            "user_email": email
        }, f)

def _load_persisted_session():
    """Load session state from file into Streamlit session."""
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                data = json.load(f)
            if not isinstance(data, dict) or "logged_in" not in data or "user_email" not in data:
                raise ValueError("Malformed session file")
            st.session_state["logged_in"] = data["logged_in"]
            st.session_state["user_email"] = data["user_email"]
        except Exception:
            st.session_state["logged_in"] = False
            st.session_state["user_email"] = None
    else:
        st.session_state["logged_in"] = False
        st.session_state["user_email"] = None

def logout():
    """Log the user out and remove session file."""
    st.session_state["logged_in"] = False
    st.session_state["user_email"] = None
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

# ---------------------------
# User Credential Management
# ---------------------------

def load_users():
    """Load users from credentials file."""
    if os.path.exists(CREDENTIAL_FILE):
        with open(CREDENTIAL_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save updated users to file."""
    with open(CREDENTIAL_FILE, "w") as f:
        json.dump(users, f)

def create_user(email, password):
    """Create a new user."""
    users = load_users()
    if email in users:
        return False
    users[email] = password
    save_users(users)
    return True

def validate_login(email, password):
    """Check user credentials and start session."""
    users = load_users()
    if users.get(email) == password:
        _persist_session(email)
        st.session_state["logged_in"] = True
        st.session_state["user_email"] = email
        return True
    return False

# ---------------------------
# Route Protection
# ---------------------------

def protect_route():
    """Stop access to protected routes if not logged in."""
    if not st.session_state.get("logged_in"):
        st.warning("Please log in to access this page.")
        st.stop()
