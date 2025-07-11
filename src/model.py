import joblib
import numpy as np
import pandas as pd

try:
    model = joblib.load("src/rf_model.pkl")
    scaler = joblib.load("src/scaler.pkl")
    selected_features = joblib.load("src/selected_features.pkl")
except Exception as e:
    raise RuntimeError(f"Failed to load model artefacts: {e}")

def preprocess(features_dict: dict) -> np.ndarray:
    """
    Convert input dict to scaled feature array
    """
    df = pd.DataFrame([features_dict])
    df_selected = df[selected_features]
    df_scaled = scaler.transform(df_selected)
    return df_scaled

def predict_url_class(features: np.ndarray) -> tuple[str, float]:
    """
    Predict class and confidence score from scaled input features
    """
    prediction = model.predict(features)[0]
    proba = model.predict_proba(features)[0]
    confidence = max(proba)

    label = "Phishing" if prediction == 1 else "Legitimate"
    return label, confidence
def get_selected_features():
    return selected_features
