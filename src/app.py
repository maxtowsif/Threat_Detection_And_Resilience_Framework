# app.py
import streamlit as st
import auth
import model  # your AI model (rf_model, scaler, etc.)
import features  # for feature extraction
import json
import os
from datetime import datetime

auth._load_persisted_session()

st.set_page_config(page_title="Threat Detection", page_icon="🛡️")
st.title("🛡️ Threat Detection & Resilience Framework")

# ----------------------------
# LOGIN SECTION
# ----------------------------
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

# ----------------------------
# REGISTRATION SECTION
# ----------------------------
with st.expander("🔑 Create New Account"):
    new_email = st.text_input("New Email")
    new_password = st.text_input("New Password", type="password")
    if st.button("Create Account"):
        if new_email and new_password:
            if auth.create_user(new_email, new_password):
                st.success("Account created successfully! You may now log in.")
            else:
                st.warning("User already exists.")
        else:
            st.warning("Please enter both email and password.")

# ----------------------------
# MAIN SYSTEM — THREAT DETECTION (Protected)
# ----------------------------
if st.session_state.get("logged_in"):

    st.markdown("---")
    st.subheader("✅ Secure Dashboard")

    url_input = st.text_input("Paste a website URL below:")
    if st.button("Check Legitimacy"):
        if url_input:
            try:
                extracted_features = features.extract_features(url_input)
                scaled_features = model.preprocess(extracted_features)
                label, confidence = model.predict_url_class(scaled_features)

                st.success(f"✅ Prediction: {label}")
                st.info(f"Model Confidence: {confidence * 100:.2f}%")

                # Save to history
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
                st.error("Something went wrong during prediction.")
                st.exception(e)
        else:
            st.warning("Please enter a URL.")

    # Display prediction history
    st.markdown("### 📜 Prediction History")
    history_path = "data/history_user.json"
    if os.path.exists(history_path):
        with open(history_path, "r") as f:
            history = json.load(f)
        for entry in reversed(history[-5:]):
            st.write(f"{entry['timestamp']} — [{entry['url']}] — **{entry['prediction']}** ({entry['confidence']}%)")
    else:
        st.info("No history yet.")
else:
    st.warning("Log in to access the threat detection system.")
