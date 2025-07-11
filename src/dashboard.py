# dashboard.py
# ---------------------------------------------------------
# 📈 Dashboard Components for Streamlit App
# Optional: Feature importance & prediction confidence viz
# ---------------------------------------------------------

import matplotlib.pyplot as plt
import streamlit as st
import numpy as np


def show_feature_importance(feature_scores: dict, top_n: int = 10):
    """
    Plots the top-N feature importances.

    Args:
        feature_scores (dict): Feature importance scores as {feature_name: score}
        top_n (int): Number of top features to show
    """
    sorted_feats = sorted(feature_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    labels, scores = zip(*sorted_feats)

    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.barh(labels, scores)
    ax.invert_yaxis()
    ax.set_title("🔍 Top Feature Importances")
    ax.set_xlabel("Importance Score")
    st.pyplot(fig)


def show_prediction_distribution(proba: list[float]):
    """
    Plots a horizontal bar to show predicted class probabilities.

    Args:
        proba (list): [prob_legit, prob_phishing]
    """
    classes = ["Legitimate", "Phishing"]
    colors = ["green", "red"]

    fig, ax = plt.subplots(figsize=(4, 1.2))
    bars = ax.barh(classes, proba, color=colors)
    ax.set_xlim(0, 1)
    ax.set_title("🔬 Model Confidence")
    ax.set_xlabel("Probability")

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.01, bar.get_y() + bar.get_height() / 2,
                f"{width:.2%}", va='center')

    st.pyplot(fig)
