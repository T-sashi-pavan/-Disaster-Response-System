from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import pickle
import sys
import re

# Add root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Utils.disaster_analyzer import DisasterAnalyzer

app = FastAPI(title="DisasterAI Testing API")

# Global variables for model
MODEL_PAYLOAD = None
ANALYZER = DisasterAnalyzer()

def tokenize(text):
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    return text.split()

# Ensure tokenize is in __main__ for pickle
import __main__
__main__.tokenize = tokenize

@app.on_event("startup")
def load_resources():
    global MODEL_PAYLOAD
    model_path = os.path.join(os.path.dirname(__file__), "ModelFiles", "disaster_model.pkl")
    if not os.path.exists(model_path):
        raise RuntimeError(f"Model file not found at {model_path}")
    with open(model_path, "rb") as f:
        MODEL_PAYLOAD = pickle.load(f)

class PredictionRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "online", "model": MODEL_PAYLOAD["best_model"] if MODEL_PAYLOAD else "None"}

@app.post("/predict")
def predict(request: PredictionRequest):
    if not MODEL_PAYLOAD:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    text = request.message
    model = MODEL_PAYLOAD["model"]
    labels = MODEL_PAYLOAD["labels"]
    
    # ML Prediction
    preds_arr = model.predict([text])[0]
    preds = {label: int(p) for label, p in zip(labels, preds_arr)}
    
    # Analyzer logic
    detected = ANALYZER.detect_disaster(preds, text)
    dtype = ANALYZER.get_disaster_type(preds, text) if detected else "None"
    needs = ANALYZER.get_needs(preds, text)
    severity = ANALYZER.get_severity(text)
    priority = ANALYZER.get_priority_score(severity, needs, dtype)
    locations = ANALYZER.extract_location(text)
    
    return {
        "text": text,
        "disaster_detected": detected,
        "disaster_type": dtype,
        "severity": severity["level"],
        "priority_score": priority,
        "needs": needs,
        "locations": [loc[0] for loc in locations] if locations else []
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
