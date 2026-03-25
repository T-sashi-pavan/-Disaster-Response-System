import os
import re
import sys
import pickle
import streamlit as st
import numpy as np
import pandas as pd

from tinydb import TinyDB, Query
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


# ---------------------------------------------------------
# UI Styling
# ---------------------------------------------------------
def set_background():
    st.markdown(
        """
        <style>
        .stApp { background-color: #e8f0fa; }
        section[data-testid="stSidebar"] { background-color: #0b2c4d; }
        section[data-testid="stSidebar"] * { color: white; }
        input, textarea {
            border-radius: 10px !important;
            border: 1px solid #0b2c4d !important;
        }
        button {
            border-radius: 10px !important;
            background-color: #0b2c4d !important;
            color: white !important;
            font-weight: 600;
        }
        .best-model {
            background-color: #28a745;
            color: white;
            padding: 8px 14px;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# CONFIG (UNCHANGED PATHS)
# ---------------------------------------------------------
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ModelFiles", "disaster_model.pkl")
REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Reports")
USER_DB = "users_db.json"


# ---------------------------------------------------------
# Tokenizer (MUST match training)
# ---------------------------------------------------------
def tokenize(text):
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    # Fast tokenization - simple split instead of NLTK
    tokens = text.split()
    lemmatizer = WordNetLemmatizer()
    try:
        return [lemmatizer.lemmatize(tok) for tok in tokens if tok]
    except (LookupError, FileNotFoundError, Exception):
        # If wordnet is not available, return tokens as-is
        return [tok for tok in tokens if tok]

# 🔥 required for pickle
sys.modules["__main__"].tokenize = tokenize


# ---------------------------------------------------------
# Load Model Payload
# ---------------------------------------------------------
@st.cache_resource
def load_payload():
    with open(MODEL_PATH, "rb") as f:
        payload = pickle.load(f)
    
    # Optimize model for single-threat prediction (disable parallelization)
    model = payload["model"]
    
    # Disable n_jobs for faster predictions (avoid threading overhead)
    # Set n_jobs=1 on MultiOutputClassifier and all its estimators
    clf = model.named_steps["clf"]
    if hasattr(clf, 'n_jobs'):
        clf.n_jobs = 1
    
    # Set n_jobs=1 on each RandomForest estimator
    if hasattr(clf, 'estimators_'):
        for est in clf.estimators_:
            if hasattr(est, 'n_jobs'):
                est.n_jobs = 1
    
    return payload

payload = load_payload()

model = payload["model"]
CATEGORY_NAMES = payload["labels"]        # ✅ correct labels
BEST_MODEL = payload["best_model"]        # ✅ RandomForest

vectorizer = model.named_steps["tfidf"]
estimators = model.named_steps["clf"].estimators_


# ---------------------------------------------------------
# Confidence Handling (RandomForest SAFE)
# ---------------------------------------------------------
def get_confidence(estimator, X):
    if hasattr(estimator, "predict_proba"):
        return estimator.predict_proba(X)[0][1]
    elif hasattr(estimator, "decision_function"):
        score = estimator.decision_function(X)[0]
        return 1 / (1 + np.exp(-score))
    return None


# ---------------------------------------------------------
# TinyDB Auth
# ---------------------------------------------------------
db = TinyDB(USER_DB)
User = Query()

def login(username, password):
    return db.search((User.username == username) & (User.password == password))

def register(username, password, mobile, address):
    if db.search(User.username == username):
        return False
    db.insert({
        "username": username,
        "password": password,
        "mobile": mobile,
        "address": address
    })
    return True


# ---------------------------------------------------------
# UI Components
# ---------------------------------------------------------
def best_model_badge():
    st.markdown(
        f'<div class="best-model">🏆 Best Model: {BEST_MODEL}</div>',
        unsafe_allow_html=True
    )


def auth_ui():
    st.title("🚨 Disaster Response System")

    menu = st.radio("Select Option", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if menu == "Login":
        if st.button("Login"):
            if login(username, password):
                st.session_state["logged_in"] = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")
    else:
        mobile = st.text_input("Mobile Number")
        address = st.text_area("Address")
        if st.button("Register"):
            if register(username, password, mobile, address):
                st.success("Registration successful. Please login.")
            else:
                st.warning("User already exists")


# ---------------------------------------------------------
# Prediction UI
# ---------------------------------------------------------
def prediction_ui():
    st.title("📨 Disaster Message Classification")
    best_model_badge()

    text = st.text_area("Enter a disaster-related message:")

    if st.button("Predict"):
        if not text.strip():
            st.warning("Please enter a message")
            return

        with st.spinner("🔄 Analyzing message..."):
            try:
                # Single prediction call - vectorizer is inside the pipeline
                import time
                start = time.time()
                preds = model.predict([text])[0]
                elapsed = time.time() - start
                
                st.subheader("Prediction Results")
                st.info(f"⚡ Processed in {elapsed:.2f} seconds")

                # Display predictions
                for label, pred in zip(CATEGORY_NAMES, preds):
                    if pred == 1:
                        st.success(f"✅ {label}: YES")
                    else:
                        st.info(f"❌ {label}: NO")
                        
            except Exception as e:
                st.error(f"Error during prediction: {str(e)}")


# ---------------------------------------------------------
# Reports UI
# ---------------------------------------------------------
def reports_ui():
    st.title("📊 Model Comparison Reports")

    acc_img = os.path.join(REPORT_DIR, "model_accuracy_comparison.png")
    f1_img = os.path.join(REPORT_DIR, "model_f1_comparison.png")

    if os.path.exists(acc_img):
        st.image(acc_img, caption="Accuracy Comparison", use_container_width=True)
    if os.path.exists(f1_img):
        st.image(f1_img, caption="F1 Score Comparison", use_container_width=True)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------
def main():
    set_background()

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        auth_ui()
    else:
        st.sidebar.title("Navigation")
        choice = st.sidebar.radio("Go to", ["Prediction", "Model Reports", "Logout"])

        if choice == "Prediction":
            prediction_ui()
        elif choice == "Model Reports":
            reports_ui()
        else:
            st.session_state["logged_in"] = False
            st.success("Logged out")
            st.rerun()


if __name__ == "__main__":
    main()
