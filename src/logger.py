# logger.py
# ---------------------------------------------------------
# 📝 Logs predictions to user-specific JSON files
# ---------------------------------------------------------

import streamlit as st
from datetime import datetime
import os
import json


def _get_log_file():
    user = st.session_state.get("user_email", "anonymous").split("@")[0]
    return f"data/history_{user}.json"


def _load_log():
    file = _get_log_file()
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return []


def _save_log(log):
    file = _get_log_file()
    with open(file, "w") as f:
        json.dump(log, f, indent=2)


def log_prediction(url: str, prediction: str, confidence: float):
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "url": url,
        "prediction": prediction,
        "confidence": f"{confidence:.2%}"
    }
    log = _load_log()
    log.append(entry)
    _save_log(log)


def show_history():
    log = _load_log()
    if log:
        st.markdown("### 🕒 Prediction History")
        st.dataframe(log, use_container_width=True)
    else:
        st.info("No predictions logged yet.")
