# app.py
import streamlit as st
from streamlit_modal import Modal
import auth
import session_utils as sess
import features
import model
import dashboard
import logger
import feedback
import numpy as np

# Page Config
st.set_page_config(
    page_title="Enhancing Cybersecurity Readiness Through Ai-augmented Threat Detection And Resilience Framework",
    page_icon="🔒",
    layout="wide"
)

# Load persisted session
auth._load_persisted_session()
if not st.session_state.get("logged_in", False):
    auth.login()
    st.stop()

auth.protect_route()
sess.init_ui_settings()
sess.load_session_preferences()
sess.apply_theme()

# -------------------------------
# TOP HEADER – USER + CONTROLS
# -------------------------------
with st.container():
    col1, col2 = st.columns([5, 1])
    with col1:
        user_type = "Admin" if "admin" in st.session_state["user_email"] else "User"
        st.markdown(f"### 👋 Welcome, {user_type}")
    with col2:
        with st.expander("⚙️ Settings", expanded=False):
            font_col1, font_col2 = st.columns(2)
            with font_col1:
                if st.button("A+ Font"):
                    sess.set_font_size("large")
            with font_col2:
                if st.button("A- Font"):
                    sess.set_font_size("small")

            st.markdown(" ")
            if st.button("👤 Profile"):
                st.session_state["open_profile_modal"] = True

# -------------------------------------
# MODAL POPUP – Profile Info (Popup)
# -------------------------------------
modal = Modal(key="profile_modal", title="👤 Profile Information", padding=20, max_width=500)
if st.session_state.get("open_profile_modal", False):
    with modal.container():
        st.write("### Logged in as:")
        st.info(f"**{st.session_state.get('user_email', 'Guest')}**")
    st.session_state["open_profile_modal"] = False

# -------------------------------
# SIDEBAR – ABOUT + LOGOUT
# -------------------------------
with st.sidebar:
    st.image(
        "https://www.rmmagazine.com/images/default-source/magazineimages/2021/07-08/rm7-8-21_find_cybersecurity.jpg?sfvrsn=59dc887f_6",
        width=150
    )
    st.markdown("### MSc Project 2025")
    st.markdown("""
        **MSc Project 2025**  
        *ENHANCING CYBERSECURITY READINESS THROUGH AI-AUGMENTED THREAT DETECTION AND RESILIENCE FRAMEWORK*  
        Model: `RandomForestClassifier`  
        Author: **Towsif**
    """)
    st.markdown("---")
    if st.button("Logout"):
        auth.logout()
    st.caption("Disclaimer: For research & educational use only.")

# -------------------------------
# MAIN – URL INPUT & PREDICTION
# -------------------------------
st.title("🔍 Phishing Website URL Detection Tool")

url_input = st.text_input("Paste a website URL below:", placeholder="https://example.com", key="url_box")
predict_btn = st.button("Check Legitimacy 🚀")

if predict_btn:
    if not url_input.strip():
        st.warning("⚠️ Please enter a valid URL.")
        st.stop()

    try:
        # Extract raw features
        raw_features = features.extract_basic_features(url_input.strip())
        selected_feature_names = model.get_selected_features()
        selected_features = [raw_features.get(f, 0) for f in selected_feature_names]
        X_input = np.array(selected_features).reshape(1, -1)
        X_scaled = model.get_scaler().transform(X_input)
        model_rf = model.get_model()

        pred_label = model_rf.predict(X_scaled)[0]
        probas = model_rf.predict_proba(X_scaled)[0]
        confidence = float(probas[pred_label])  # ✅ FIXED: pick confidence from predicted class

        label_text = "Phishing" if pred_label == 1 else "Legitimate"

        st.session_state["last_prediction"] = {
            "url": url_input.strip(),
            "label": label_text,
            "confidence": confidence,
            "features": raw_features
        }

        logger.log_prediction(url_input.strip(), label_text, confidence)

    except Exception as e:
        st.error(f"⚠️ Something went wrong during prediction.\n\n**Details:** {str(e)}")

# -------------------------------
# RESULTS – Persist After Feedback
# -------------------------------
if "last_prediction" in st.session_state:
    pred = st.session_state["last_prediction"]
    label_text = pred["label"]
    confidence = pred["confidence"]

    st.markdown("---")
    # ✅ FIXED: Reverse order based on label_text
    if label_text == "Phishing":
        st.error(f"❌ **Phishing Website Detected!**\n\nConfidence: {confidence:.2%}")
        dashboard.show_prediction_distribution([1 - confidence, confidence])  # [legit, phish]
    else:
        st.success(f"✅ **Legitimate Website**\n\nConfidence: {confidence:.2%}")
        dashboard.show_prediction_distribution([confidence, 1 - confidence])  # [legit, phish]


    st.markdown("---")
    st.subheader("🔑 Feature Snapshot")
    sel = model.get_selected_features()
    filtered = {k: v for k, v in pred["features"].items() if k in sel}
    st.json(filtered, expanded=False)

    st.markdown("---")
    feedback.collect_feedback(pred["url"], label_text, confidence)

# -------------------------------
# FEEDBACK HISTORY
# -------------------------------
st.markdown("---")
logger.show_history()
feedback.display_feedback_log()
