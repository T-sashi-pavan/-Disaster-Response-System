# 🚀 Quick Start Guide - Global Disaster Intelligence System

## ⚡ 5-Minute Setup

### 1. **Activate Environment**
```bash
# Windows (Git Bash or CMD)
source env/Scripts/activate

# Or Windows PowerShell
.\env\Scripts\Activate.ps1
```

### 2. **Start the App**
```bash
streamlit run WebApp/app.py
```

### 3. **Open in Browser**
```
http://localhost:8501
```

---

## 🎯 What's NEW - Feature Overview

### **Tab 1: 🔍 Predict**
**What's New:**
- ⚡ **Breaking News Headlines** section at top
- Shows latest news from BBC, Reuters, Al Jazeera
- "Analyze This News" button for each headline
- Then: Standard message analysis below

**Steps:**
1. See breaking news at top
2. Enter your disaster message
3. Click "🔍 Analyze Message"
4. Get instant AI analysis

---

### **Tab 2: 🌍 Globe Live Events** (COMPLETELY REDESIGNED)
**What's New:**
- 🔴 Multi-source data selector (All/GDACS/USGS/EONET/News)
- 📊 Real-time intelligence dashboard (6 metrics)
- 5 Interactive tabs inside:
  - Overview Cards (sortable, analyzable)
  - Global Map (interactive, clickable)
  - Breaking News (RSS feeds)
  - Statistics (charts)
  - Filters & Search

**Steps:**
1. Click "All Sources" or specific source
2. Click "Refresh Data"
3. See dashboard metrics
4. Navigate tabs to explore
5. Click "Analyze" on any disaster
6. See emergency helplines + voice alert

---

## 📊 Dashboard Walkthrough

### **Real-Time Intelligence Dashboard**
Shows 6 live metrics:
- 📍 Total Events
- 🔴 Critical (Red)
- 🟠 High (Orange)
- 🔵 Medium (Blue)
- 🟢 Low (Green)
- 🗺️ Countries Affected

### **Inside the Map Tab**
- 🗺️ Interactive global map
- 📌 Color-coded disaster markers
- 🎯 Clustered for large datasets
- 🔍 Click markers for details

---

## 🆘 Emergency Helpline Feature

### **When You Analyze a Disaster:**
You'll see emergency helpline for that country showing:
- 📞 Emergency Number (112/911/999)
- 🚨 Disaster Management Hotline
- 🚑 Ambulance Number
- 🚒 Fire Department
- 🚔 Police
- 🏥 Local Organizations (top 3)

### **Supported Countries:**
India, Bangladesh, Pakistan, Philippines, Thailand, Indonesia, Japan, Nepal, Turkey, Syria, Kenya, Ethiopia, USA, Mexico, Chile, Brazil, Italy, Greece, Australia, New Zealand, South Korea, Vietnam, Hong Kong, Sri Lanka (25+)

---

## 🗺️ Global Map Features

### **What You See:**
- 🔴 RED = CRITICAL severity
- 🟠 ORANGE = HIGH severity
- 🔵 BLUE = MEDIUM severity
- 🟢 GREEN = LOW severity

### **Interactions:**
- Zoom in/out with scroll
- Drag to pan
- Click markers for info
- Fullscreen button in corner
- Markers cluster when zoomed out

---

## 📰 Breaking News Integration

### **In Predict Tab (Top Section):**
Shows 3-5 latest news headlines with:
- Source: BBC | Reuters | Al Jazeera
- Headline (preview)
- Timestamp
- Color-coded severity
- "Analyze This News" button

### **In Live Events Tab (Breaking News Tab):**
Shows 15+ latest news items scrollable

---

## 🔄 Data Sources (4 APIs)

### **GDACS** 🔴
- Global Disaster Alert & Coordination System
- Earthquakes, floods, cyclones, volcanoes
- Updated in real-time

### **USGS** 📊
- US Geological Survey Earthquakes
- Significant earthquakes worldwide (M4.5+)
- 24-hour rolling feed

### **NASA EONET** 🛰️
- Earth Observation Network
- Satellite-detected wildfires, floods, volcanoes, storms
- High accuracy

### **Breaking News** 📰
- BBC World RSS
- Reuters Alerts RSS
- Al Jazeera English RSS

---

## ⚙️ Key Settings

### **Cache Duration:**
- 5 minutes per source
- Prevents API overload
- Automatic fallback data if API fails

### **Sorting Options:**
- By Severity (Critical → Low)
- By Date (Newest first)
- By Country (A-Z)

### **Filtering:**
- Search by text (title/country)
- Filter by disaster type
- Real-time results

---

## 🎤 Voice Alert Feature

### **When Activated:**
- Text-to-speech conversion
- Plays in background (non-blocking)
- Announces: Disaster type, severity, location, actions needed

### **Example Alert:**
"Earthquake detected in Nepal. Severity: Critical. Priority: 9 out of 10. Rescue and shelter assistance urgently needed."

---

## 📊 Performance

### **Prediction Speed:**
- Single message: **1-5ms** ⚡
- 100 messages: **1-2 seconds**
- 1000 messages: **15-25 seconds**

### **API Response (with cache):**
- Average: **500-1500ms per source**
- With 5-min cache: **<100ms cached**

---

## 🔧 Troubleshooting

### **App won't start?**
```bash
# Reinstall dependencies
pip install -r Requirements.txt

# Try updating Streamlit
pip install --upgrade streamlit
```

### **Map not showing?**
- Check internet connection
- Clear browser cache
- Try different browser

### **Breaking news not showing?**
- Wait for RSS feed update (usually 1-5 min)
- Click "Refresh Data" button
- Check if news sources are accessible

### **Voice not working?**
- App will show warning but continue
- Try "Play Voice Alert" button
- Check volume is not muted

### **Helpline not showing?**
- Country might not be in database (25+ countries)
- Contact admin to add more countries
- Manual lookup available in Help tab

---

## 📱 Mobile Friendly

- App is responsive on mobile
- Touch-optimized buttons
- Readable on all sizes
- Works on phones, tablets, desktops

### **Recommended Screen Sizes:**
- Desktop: 1920x1080+
- Tablet: 1024x768+
- Phone: 375x667+

---

## 🎯 Use Cases

### **Disaster Response Team:**
1. Go to "Globe Live Events"
2. Check real-time metrics
3. View global map
4. Search specific country/disaster
5. Get helpline info instantly

### **News Organization:**
1. Check "Breaking News" tab
2. See latest disaster news
3. Analyze news headlines
4. Cross-reference with live APIs

### **Research Study:**
1. Use "Batch Processing" for multiple messages
2. Export results to CSV
3. Analyze prediction patterns
4. Generate statistics

### **Emergency Responder:**
1. Enter urgent message
2. Get severity & priority instantly
3. See recommended actions
4. Get local helpline numbers
5. Enable voice alert

---

## 🚀 Advanced Features

### **Session Persistence:**
- Close and reopen tabs without losing data
- Analysis results persist
- Browsing history maintained

### **User History:**
- Every prediction tracked
- Timestamp recorded
- Can be exported to CSV
- Searchable by date/content

### **Batch Processing:**
- Upload CSV with 100s of messages
- Process all at once
- Download results with confidence scores

### **Export Data:**
- CSV export available
- JSON export available
- Includes all metadata
- Timestamped

---

## 💾 Data Storage

### **User Data Stored:**
- `users_db.json` - User credentials, history, feedback
- Local storage only (no cloud)
- TinyDB format (JSON-based)

### **Model Data:**
- `ModelFiles/disaster_model.pkl` - Trained model
- Naive Bayes classifier
- Multi-output capable (multiple categories)

### **Training Data:**
- `Dataset/disaster_messages.csv` - Training messages
- `Dataset/disaster_categories.csv` - Training labels
- 26,386 labeled messages
- 36 disaster categories

---

## 🎓 Learning Path

### **Beginner:**
1. Read this Quick Start
2. Try Predict tab with sample messages
3. View a breaking news headline
4. Check history

### **Intermediate:**
1. Explore "Globe Live Events"
2. View global map
3. Analyze multiple disasters
4. Check helpline info

### **Advanced:**
1. Use Batch Processing
2. Export data and analyze patterns
3. Understand severity scoring
4. Review prediction history analytics

---

## 🔗 External Resources

### **API Documentation:**
- GDACS: https://www.gdacs.org/
- USGS: https://earthquake.usgs.gov/earthquakes/feed/
- NASA EONET: https://eonet.gsfc.nasa.gov/

### **Emergency Services:**
- Red Cross: https://www.ifrc.org/
- UNHCR: https://www.unhcr.org/
- WHO: https://www.who.int/

---

## ❓ FAQ

**Q: How often is data updated?**
A: Every 5 minutes (cached from real sources that update continuously)

**Q: Which countries have helplines?**
A: 25+ countries including India, Japan, USA, Australia, Brazil, etc.

**Q: Can I use this offline?**
A: No, requires internet for APIs and news feeds

**Q: How accurate are predictions?**
A: 70% accuracy for disaster detection (optimized for speed)

**Q: Can I customize severity thresholds?**
A: Advanced users can edit `disaster_analysis_engine.py`

**Q: What if an API is down?**
A: System uses fallback data and continues normally

**Q: How long can I run the app?**
A: Indefinitely (caching prevents API overload)

**Q: Can I add more countries' helplines?**
A: Edit `Utils/helpline_database.py` to add new entries

---

## 🎉 Summary - What Changed

| Feature | Before | After |
|---------|--------|-------|
| Data Sources | 1 (ReliefWeb) | 4 (GDACS, USGS, EONET, News) |
| Breaking News | ❌ None | ✅ BBC, Reuters, Al Jazeera |
| Global Map | ❌ Static | ✅ Interactive, clustered |
| Helplines | ❌ None | ✅ 25+ countries |
| Dashboard | ✅ Basic | ✅ Enhanced (6 metrics) |
| Tabs | 1 tab | ✅ 5 tabs in Live Events |
| Search/Filter | ❌ None | ✅ Full search + filter |
| Voice Alerts | ✅ Yes | ✅ Enhanced |
| Session Persistence | ❌ No | ✅ Yes |
| Performance | ⚡ Fast | ⚡⚡⚡ Faster (1-5ms) |

---

**Ready? Start the app and explore! 🚀**
