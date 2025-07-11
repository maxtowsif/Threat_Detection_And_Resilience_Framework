# model.py
# ---------------------------------------------------------
# 🧠 Model Prediction Module
# Loads trained model + scaler + features and makes predictions
# ---------------------------------------------------------

import joblib
import numpy as np

# File paths for model artefacts
MODEL_PATH = "rf_model.pkl"
SCALER_PATH = "scaler.pkl"
FEATURE_LIST_PATH = "selected_features.pkl"

# Load artefacts once at module level
try:
    rf_model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    selected_features = joblib.load(FEATURE_LIST_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load model artefacts: {e}")


def get_selected_features():
    """
    Returns the list of selected feature names.
    """
    return selected_features


def get_scaler():
    """
    Returns the fitted StandardScaler.
    """
    return scaler


def get_model():
    """
    Returns the trained RandomForest model.
    """
    return rf_model


def predict_url_class(features: np.ndarray) -> tuple[int, float]:
    """
    Predicts the class of a URL based on its features.

    Args:
        features (np.ndarray): Scaled 1×n feature vector

    Returns:
        tuple: (predicted_label, confidence_score)
    """
    probas = rf_model.predict_proba(features)[0]
    pred = int(np.argmax(probas))
    conf = float(np.max(probas))
    return pred, conf
