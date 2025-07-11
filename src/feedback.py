# feedback.py
import streamlit as st
import json
import os
from datetime import datetime

def _get_feedback_file():
    user = st.session_state.get("user_email", "anonymous").split("@")[0]
    return f"data/feedback_{user}.json"

def _load_feedback():
    file = _get_feedback_file()
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return []

def _save_feedback(feedback_list):
    file = _get_feedback_file()
    os.makedirs("data", exist_ok=True)
    with open(file, "w") as f:
        json.dump(feedback_list, f, indent=2)

def collect_feedback(url: str, predicted_label: str, confidence: float):
    key_prefix = url.replace("https://", "").replace("http://", "").replace("/", "_")

    # Initialise session feedback cache
    if f"{key_prefix}_choice" not in st.session_state:
        st.session_state[f"{key_prefix}_choice"] = "👍 Correct"
    if f"{key_prefix}_comment" not in st.session_state:
        st.session_state[f"{key_prefix}_comment"] = ""

    with st.expander("💡 Give Feedback", expanded=True):
        choice = st.radio(
            "How would you rate this prediction?",
            ["👍 Correct", "👎 Incorrect"],
            key=f"{key_prefix}_choice"
        )
        comment = st.text_area(
            "Additional comments (optional):",
            key=f"{key_prefix}_comment"
        )

        if st.button("Submit Feedback 📨", key=f"{key_prefix}_submit"):
            feedback_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "url": url,
                "predicted_label": predicted_label,
                "confidence": f"{confidence:.2%}",
                "user_feedback": choice,
                "user_comment": comment.strip()
            }

            feedback_log = _load_feedback()
            feedback_log.append(feedback_entry)
            _save_feedback(feedback_log)

            st.success("✅ Feedback submitted!")

def display_feedback_log():
    feedback_log = _load_feedback()
    if feedback_log:
        st.markdown("### 🗂️ Your Submitted Feedback")
        st.dataframe(feedback_log, use_container_width=True)
    else:
        st.info("No feedback submitted yet.")
