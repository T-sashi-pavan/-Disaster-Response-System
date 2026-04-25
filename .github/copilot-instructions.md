# Disaster Response Tweets Classification - Project Guide

## 📋 Project Overview
This is a **disaster response system** that classifies disaster-related tweets/messages into multiple disaster categories using machine learning. The system features:
- Multi-label classification (a message can belong to multiple disaster types)
- Web-based Streamlit interface  
- User authentication with TinyDB
- Model comparison and performance reports

## 🏗️ Architecture

### Key Components
- **ModelGeneration/ModelGeneration.py** - Model training pipeline (4 classifiers: LogisticRegression, LinearSVM, RandomForest, SGDClassifier)
- **WebApp/app.py** - Streamlit web interface with authentication and prediction UI
- **Dataset/** - Training data (disaster_messages.csv, disaster_categories.csv)
- **ModelFiles/disaster_model.pkl** - Serialized trained model payload
- **Reports/** - Generated comparison graphs

### Data Flow
```
Raw Text → Tokenization & Lemmatization → TF-IDF Vectorization → Multi-Output Classifier → Predictions
```

### Disaster Categories
The model predicts one or more of these categories:
- related, request, offer, aid_related, medical_help, medical_products
- search_and_rescue, security, military, child_alone, water, food, shelter
- clothing, money, missing_people, refugees, death, other_aid, infrastructure_related
- transport, buildings, electricity, tools, hospitals, shops, aid_centers, other_infrastructure
- weather_related, floods, storm, fire, earthquake, cold, other_weather

## 🚀 Planned Features (5-Day Roadmap)

### Day 1: Severity Score & Priority System
- Calculate disaster severity based on predicted categories
- Show priority level (Critical, High, Medium, Low)
- Add contextual recommendations

### Day 2: Prediction History & Analytics
- Store prediction history per user
- Dashboard with statistics: trends, most common disasters, prediction frequency
- Export history as CSV/JSON

### Day 3: Batch Processing & CSV Import
- Upload multiple disaster messages at once
- Get predictions for entire batch
- Download results with timestamps and confidence scores

### Day 4: Real-time Text Statistics
- Word count, reading time estimation
- Sentiment analysis  
- Highlight disaster-related keywords detected
- Text quality feedback

### Day 5: Polish & Documentation
- Create API reference guide
- Improve UI/UX consistency
- Add quick reference cards for disaster types

## 🛠️ Development Environment

### Requirements
- Python 3.10.9+
- Dependencies: numpy, pandas, matplotlib, seaborn, nltk, scikit-learn, streamlit, tinydb

### Running the App
```bash
# Activate environment
source env/Scripts/activate  # Windows/Git Bash

# Run training (optional)
python ModelGeneration/ModelGeneration.py

# Run web app
streamlit run WebApp/app.py
```

### Key Database
- `users_db.json` - TinyDB for user credentials and predictions

## ⚠️ Important Notes
- **Paths**: ModelGeneration.py has hardcoded path - update if needed
- **Tokenization**: Must match training in app.py (uses WordNetLemmatizer with fallback)
- **Model Format**: Pickled payload contains {model, labels, best_model}
- **Performance**: RandomForest is the best model (highest micro-F1)

## 📝 Coding Conventions
- Use Streamlit's st.session_state for UI state
- Keep tokenization logic synchronized between training and prediction
- Store user data in users_db.json (TinyDB)
- Use absolute paths with os.path.join for cross-platform compatibility

## 🔗 Quick Links
- Main app: `WebApp/app.py`
- Model training: `ModelGeneration/ModelGeneration.py`
- Training data: `Dataset/`
- User database: `users_db.json`
