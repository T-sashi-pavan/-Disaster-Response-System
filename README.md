# 🚨 DisasterAI — Advanced Disaster Management AI System

An intelligent, ML-powered disaster response support system built with Python and Streamlit. Analyzes emergency messages and outputs structured predictions, voice alerts, and an interactive map.

---

## Features

| Feature | Description |
|---|---|
| 🔍 Disaster Detection | YES/NO classification using ML model |
| 🌍 Disaster Type | Flood / Fire / Earthquake / Cyclone / Accident |
| 🆘 Multi-Label Needs | Medical / Shelter / Food / Rescue |
| ⚠️ Severity Detection | High / Medium / Low (keyword-based) |
| 📊 Priority Score | 1–10 urgency score |
| 📍 Location Extraction | 150+ cities using regex + NLP |
| 📋 AI Recommended Actions | Rule-based emergency action engine |
| 📢 Auto Response Generator | Emergency summary statement |
| 📊 Dashboard | Case counts, type & severity charts |
| 🗺️ Map Integration | Folium interactive map |
| 🔊 Voice Output | gTTS audio alert (auto-plays after prediction) |

---

## Project Structure

```
New_DisasterResponseTweets_2026/
├── Dataset/
│   ├── disaster_messages.csv
│   └── disaster_categories.csv
├── ModelFiles/
│   └── disaster_model.pkl          ← Trained ML model
├── ModelGeneration/
│   ├── ModelGeneration.py          ← Full training script
│   ├── ModelGeneration_Optimized.py
│   └── ModelGeneration_UltraFast.py
├── Reports/
│   └── *.png                       ← Model comparison charts
├── Utils/
│   ├── disaster_analyzer.py        ← Core AI engine (NEW)
│   ├── severity_scorer.py
│   ├── prediction_history.py
│   └── ...
├── WebApp/
│   └── app.py                      ← Main Streamlit application
├── Requirements.txt
└── README.md
```

---

## Setup & Run

### Step 1 — Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### Step 2 — Install Dependencies
```bash
pip install -r Requirements.txt
```

### Step 3 — Download NLTK Data
```bash
python -c "import nltk; nltk.download('wordnet'); nltk.download('punkt')"
```

### Step 4 — Run the App
```bash
cd WebApp
streamlit run app.py
```

The app opens at **http://localhost:8501**

### Default Login
Register a new account on the login screen (any username/password).

---

## Train the Model

### Quick Train (Recommended — uses optimized LogisticRegression)
```bash
python quicktrain_model.py
```

### Full Training (All 4 models — slower, picks best)
```bash
cd ModelGeneration
python ModelGeneration.py
```
> Training requires the CSV files in `Dataset/`. Takes 5–15 minutes for full training.

---

## How to Test All Features

### 1. Run the app
```bash
cd WebApp && streamlit run app.py
```

### 2. Register & Login
- Click **Register**, create any account, then **Login**

### 3. Test — Disaster Detection
- Message: `"Heavy rain is expected tomorrow"`
- Expected: **NO** (no disaster)

### 4. Test — Flood Detection
- Message: `"Severe flooding in Mumbai, families trapped, need rescue and food"`
- Expected: YES · Flood · High Severity · Priority 9+

### 5. Test — Earthquake
- Message: `"Earthquake in Kathmandu, buildings collapsed, many injured, need medical help"`
- Expected: YES · Earthquake · High Severity · Medical + Rescue needs

### 6. Test — Cyclone
- Message: `"Cyclone approaching Chennai coast, wind 180 kmph, evacuate immediately"`
- Expected: YES · Cyclone · High Severity · Shelter need

### 7. Test — Fire
- Message: `"Wildfire spreading near Bangalore, people evacuating, road blocked"`
- Expected: YES · Fire · Medium Severity

### 8. Test — Accident
- Message: `"Major road accident on Delhi highway, critical injuries, ambulance needed"`
- Expected: YES · Accident · High Severity · Medical need

### 9. Test — Low Severity / Warning
- Message: `"Flood warning issued for coastal areas, prepare and take precautions"`
- Expected: YES · Flood · Low Severity · Priority 3–4

### 10. Test — Location Extraction
- Message: `"People are trapped in Hyderabad near Tank Bund due to floods"`
- Expected: Location = **Hyderabad** + Folium map shown

### 11. Test — Voice Output
- Any disaster message → Click Analyze → Audio player appears and plays automatically

### 12. Test — Dashboard
- Make 3–5 predictions → Go to **Dashboard**
- Expected: Case count, disaster type chart, severity distribution

### 13. Test — History
- Go to **History** tab after several predictions
- Expected: Color-coded timeline of all predictions

---

## ML Model Details

| Model | Accuracy | Speed |
|---|---|---|
| LogisticRegression (default) | ~73% | ⚡ 10–50ms |
| RandomForest (full train) | ~76% | 🐢 500–2000ms |
| LinearSVM | ~74% | ⚡ Fast |
| SGDClassifier | ~72% | ⚡ Very Fast |

The model is trained on **26,000+** real disaster messages (Figure Eight / Appen dataset) with **36 multi-label categories**.

---

## Severity Keyword Reference

| Severity | Keywords |
|---|---|
| 🔴 High | trapped, critical, injured, collapsed, dead, drowning, buried, sos, explosion |
| 🟡 Medium | help needed, road blocked, stranded, evacuate, damage, displaced |
| 🟢 Low | warning, advisory, caution, prepare, forecast, awareness |

---

## Voice Output Note

Voice uses **gTTS** (Google Text-to-Speech). Requires internet access.
If offline, the voice script is displayed as text instead.

To test voice manually:
```python
from gtts import gTTS
import io
tts = gTTS("Disaster detected in Mumbai. Severity High. Dispatch rescue team.", lang='en')
tts.save("test.mp3")
```

---

## Dependencies

- `streamlit` — Web UI
- `scikit-learn` — ML classification
- `nltk` — Text tokenization/lemmatization
- `folium` + `streamlit-folium` — Interactive map
- `gtts` — Google Text-to-Speech
- `pandas`, `numpy` — Data processing
- `tinydb` — Lightweight user database
