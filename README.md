# Threat_Detection_And_Resilience_Framework
🚀 Threat Detection and Resilience Framework

Enhancing Cybersecurity Readiness Through AI-Augmented Threat Detection and Resilience
📋 Overview

This project implements an AI-powered threat detection and resilience framework combining supervised machine learning and interactive web capabilities. It is designed to:

    Detect phishing URLs and simulate attacks

    Log predictions for transparency

    Provide explainable feature importance

    Support compliance alignment (GDPR, ISO 27001, NIST CSF, MITRE ATT&CK)

    Enable real-time experimentation via a Streamlit web interface

✅ Live Demo: Streamlit Deployment

✅ GitHub Repository: View Code
🧠 Core Features

    AI Model: LightGBM classifier trained on a phishing dataset (>80 features), achieving ~97% accuracy

    Explainability: Feature importance visualizations via Boruta

    Fairness Evaluation: Statistical parity difference and equal opportunity metrics

    Prediction Logging: JSON-based logs to record user predictions (supports auditability)

    Interactive UI: Streamlit app for submitting URLs and viewing results

    Compliance Mapping:

        GDPR: No personal data stored, all logs synthetic

        ISO 27001: Event logging, incident assessment, evidence tracking

        NIST CSF: Identify, Detect, Respond capabilities

        MITRE ATT&CK: Phishing mapped to credential access tactics

🛠️ Project Structure

repo/
├── app.py                # Main Streamlit app
├── model.py              # LightGBM model load and prediction
├── dataset_phishing.csv  # Original dataset
├── dataset_phishing_clean.csv  # Cleaned dataset
├── scaler.pkl            # Scaler for feature normalization
├── selected_features.pkl # Selected feature list
├── rf_model.pkl          # Trained model
├── feedback_user.json    # User feedback logs
├── history_user.json     # Prediction history
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker deployment configuration
├── README.md             # This documentation
└── /static               # Any static files (e.g., images)

⚡ Quick Start

1️⃣ Install Requirements

pip install -r requirements.txt

2️⃣ Launch Locally

streamlit run app.py

3️⃣ Docker Deployment
Build and run the container:

docker build -t threat-detector .
docker run -p 8501:8501 threat-detector

🎯 Objectives

This system delivers on the following academic objectives:
Objective	Implementation Example
Enhance cybersecurity readiness	Simulated phishing URL detection with >95% accuracy
Use AI-augmented methods	LightGBM model with explainability and fairness metrics
Develop an integrated resilience framework	Modular architecture combining ML, explainability, and compliance alignment
Evaluate performance and ethical considerations	ROC, confusion matrix, statistical fairness, GDPR compliance
🧪 How It Works

    User submits a URL.

    The app extracts relevant features.

    The model predicts if the URL is phishing.

    Prediction is stored in history_user.json.

    Feature importance and metrics are displayed.

    Optionally, users submit feedback on prediction accuracy.

