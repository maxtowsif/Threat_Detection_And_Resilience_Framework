# app.py
import streamlit as st
import auth
import model
import features
import json
import os
from datetime import datetime

# Initialize Streamlit session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None

auth._load_persisted_session()

# -------------------------------------
# PAGE ROUTING (Login vs Dashboard)
# -------------------------------------
if not st.session_state.logged_in:
    # ----------------------------
    # LOGIN PAGE
    # ----------------------------
    st.set_page_config(page_title="Login | Threat Detection", page_icon="🔐")
    st.title("🔐 Login to Threat Detection System")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns([1, 2])
    if col1.button("Login"):
        if auth.validate_login(email, password):
            st.experimental_rerun()
        else:
            st.error("Invalid email or password.")

    if col2.button("Logout"):
        auth.logout()
        st.info("You have been logged out.")

    # ---- Registration Section
    with st.expander("🔑 Create a New Account"):
        new_email = st.text_input("New Email")
        new_password = st.text_input("New Password", type="password")
        if st.button("Create Account"):
            if new_email and new_password:
                if auth.create_user(new_email, new_password):
                    st.success("Account created successfully. You can now log in.")
                else:
                    st.warning("User already exists.")
            else:
                st.warning("Please fill in both fields.")

else:
    # ----------------------------
    # DASHBOARD PAGE
    # ----------------------------
    st.set_page_config(page_title="Dashboard | Threat Detection", page_icon="🛡️")
    st.title("🛡️ Threat Detection & Resilience Dashboard")
    st.success(f"Logged in as {st.session_state.user_email}")

    st.button("Logout", on_click=auth.logout)

    # ---- Threat Detection
    url_input = st.text_input("Paste a website URL below:")
    if st.button("Check Legitimacy"):
        if url_input:
            try:
                extracted_features = features.extract_features(url_input)
                scaled_features = model.preprocess(extracted_features)
                label, confidence = model.predict_url_class(scaled_features)

                st.success(f"✅ Prediction: {label}")
                st.info(f"Model Confidence: {confidence * 100:.2f}%")

                # Save to prediction history
                history_path = "data/history_user.json"
                history = []
                if os.path.exists(history_path):
                    with open(history_path, "r") as f:
                        history = json.load(f)

                history.append({
                    "timestamp": str(datetime.now()),
                    "url": url_input,
                    "prediction": label,
                    "confidence": round(confidence * 100, 2)
                })

                with open(history_path, "w") as f:
                    json.dump(history, f, indent=2)

            except Exception as e:
                st.error("Prediction error:")
                st.exception(e)
        else:
            st.warning("Please enter a URL.")

    # ---- History Viewer
    st.markdown("### 📜 Prediction History")
    history_path = "data/history_user.json"
    if os.path.exists(history_path):
        with open(history_path, "r") as f:
            history = json.load(f)
        for entry in reversed(history[-5:]):
            st.write(f"{entry['timestamp']} — [{entry['url']}] — **{entry['prediction']}** ({entry['confidence']}%)")
    else:
        st.info("No predictions yet.")
