# DisasterAI - Quick Start Guide

## Installation

### 1. Install Dependencies
```bash
cd "c:\Desktop\college project\New_DisasterResponseTweets_2026"
pip install -r Requirements.txt
```

### 2. Download NLTK Data (One-time)
```bash
python nltkdownload.py
```

### 3. Train Model (Optional - if disaster_model.pkl missing)
```bash
python quicktrain_model.py
```

## Running the Application

### Start Web Application
```bash
streamlit run WebApp/app.py
```

App opens at: `http://localhost:8501`

### Default Credentials (Demo)
- **Username**: `demo`
- **Password**: `demo123`

Or create new account on signup page.

## Features Overview

| Feature | Location | Description |
|---------|----------|-------------|
| **Predict** | Sidebar → Predict | Single message disaster classification |
| **Dashboard** | Sidebar → Dashboard | Analytics & statistics |
| **Live Events** | Sidebar → Globe Live Events | Real-time global disasters (NEW) |
| **History** | Sidebar → History | Past predictions |
| **Help** | Sidebar → Help | Usage guide & documentation |

## Live Disasters Feature (NEW)

### What It Does
- Fetches 20+ active disasters from ReliefWeb API
- Displays metrics dashboard (total events, high priority, etc.)
- Shows disaster type distribution chart
- Allows click-to-analyze for individual events
- Provides voice alerts (text-to-speech)

### How to Use
1. Click "Globe Live Events" in sidebar
2. Click "Refresh Now" to update list
3. Click "Analyze" on any disaster card
4. View AI-powered analysis results
5. Click "Play Voice Alert" to hear summary

### Technical Stack
- **API**: ReliefWeb (https://api.reliefweb.int/v2/disasters)
- **Analysis**: Custom DisasterAnalysisEngine
- **Voice**: pyttsx3 (text-to-speech)
- **Caching**: 60-second response cache
- **Fallback**: Sample data if API unavailable

## Testing

### Run Comprehensive Tests
```bash
python test_reliefweb_api.py
```

**Expected Output**:
```
✅ PASS | ReliefWeb API
✅ PASS | Disaster Analysis
✅ PASS | Voice Output
✅ PASS | Full Integration

Total: 4/4 test groups passed
```

### Run CURL API Tests
```bash
bash curl_reliefweb_tests.sh
```

## Model Performance

- **Accuracy**: 70% (Naive Bayes for speed)
- **Speed**: 1-5ms per prediction
- **Batch**: 1-2 seconds for 100 messages
- **Training**: ~3 minutes for 26,000 messages

## New Files Added

| File | Type | Purpose |
|------|------|---------|
| `Utils/reliefweb_api.py` | Module | ReliefWeb API integration |
| `Utils/disaster_analysis_engine.py` | Module | AI disaster analysis |
| `Utils/voice_output.py` | Module | Text-to-speech alerts |
| `test_reliefweb_api.py` | Test | Comprehensive test suite |
| `curl_reliefweb_tests.sh` | Test | CURL API tests |
| `LIVE_DISASTERS_FEATURE.md` | Docs | Feature documentation |
| `QUICK_START.md` | Guide | This file |

## Sample Test Messages

```
"Severe flooding in Mumbai, families are trapped, urgent rescue needed"
"Massive earthquake in Nepal, buildings collapsed, injuries reported"
"Wildfire spreading in California, evacuations underway"
"Cyclone approaching Chennai coast with 180 kmph wind speed"
```

## API Endpoints Used

### ReliefWeb API
- Base: `https://api.reliefweb.int/v2/disasters`
- Example: `?appname=RescueMeAIProject&limit=20&preset=latest`

## Troubleshooting

### Port Already in Use
```bash
streamlit run WebApp/app.py --server.port 8502
```

### Model Not Found
```bash
python quicktrain_model.py
```

### Voice Not Working
```bash
pip install pyttsx3
```

### API Access Issues
- App automatically falls back to sample data
- No loss of functionality

## Database

### User Database
- File: `users_db.json`
- Format: JSON (TinyDB)
- Contains: credentials, prediction history, feedback

## Project Structure

```
DisasterResponseTweets/
├── WebApp/
│   └── app.py (Streamlit UI - 560+ lines)
├── ModelFiles/
│   └── disaster_model.pkl (trained model)
├── Utils/
│   ├── reliefweb_api.py (NEW - API integration)
│   ├── disaster_analysis_engine.py (NEW - AI analysis)
│   ├── voice_output.py (NEW - TTS)
│   ├── disaster_analyzer.py (original)
│   └── ... (other utilities)
├── Dataset/
│   ├── disaster_messages.csv
│   └── disaster_categories.csv
├── test_reliefweb_api.py (NEW - tests)
├── curl_reliefweb_tests.sh (NEW - tests)
├── quicktrain_model.py (model training)
├── Requirements.txt (dependencies)
└── README.md
```

## Performance Tips

1. **Enable Auto-Refresh**: Keeps 60-second cache fresh
2. **Batch Processing**: Analyze 100+ messages at once
3. **Use Dashboard**: Pre-computed statistics are fast
4. **Voice Async**: TTS runs in background, doesn't block UI

## Next Steps

1. Train model with your own data (optional)
2. Add custom disaster categories
3. Integrate with alert systems
4. Add email notifications
5. Deploy to cloud (Heroku, AWS, etc.)

## Support

For issues or questions:
1. Check `❓ Help` tab in app
2. Review `LIVE_DISASTERS_FEATURE.md`
3. Run tests: `python test_reliefweb_api.py`
4. Check logs for errors

## Version Info

- **App Version**: 2.0 (Live Disasters Update)
- **Python**: 3.10.9+
- **Streamlit**: Latest
- **Release Date**: 2026-04-25

---

**Ready to use!** Start with:
```bash
streamlit run WebApp/app.py
```
