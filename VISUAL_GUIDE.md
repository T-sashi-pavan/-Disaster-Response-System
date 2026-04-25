# 👀 Visual Guide - What You'll See When Running the App

## 🎬 App Navigation Overview

When you run `streamlit run WebApp/app.py`, you'll see this layout:

```
╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║  🔐 AUTHENTICATION TAB (First Time)                                   ║
║  ├─ Login Form (or Register)                                          ║
║  ├─ Email/Password input                                              ║
║  └─ After auth → Main Dashboard                                       ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝
```

---

## 📊 Main Dashboard (After Login)

```
╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║  SIDEBAR (Left)                                                       ║
║  ├─ [🔍 Predict]          ← Single message analysis                   ║
║  ├─ [📊 Dashboard]        ← Statistics & analytics                    ║
║  ├─ [🌍 Globe Live Events] ← NEW: 4-source live disasters            ║
║  ├─ [📜 History]          ← Prediction history                        ║
║  ├─ [Batch Processing]    ← CSV upload                               ║
║  ├─ [❓ Help]             ← Documentation                             ║
║  └─ [Logout]              ← Sign out                                   ║
║                                                                        ║
║  MAIN CONTENT AREA (80% width)                                       ║
║  └─ Content changes based on selected tab                            ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝
```

---

## 🔍 TAB 1: PREDICT (Single Message Analysis)

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║  🚨 Disaster Intelligence Analysis                                   ║
║  Model: Naive Bayes · Enter a message below to analyze               ║
║                                                                       ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │ ⚡ Breaking News Headlines                                      │ ║
║  ├─────────────────────────────────────────────────────────────────┤ ║
║  │                                                                 │ ║
║  │  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐   │ ║
║  │  │ BBC World       │  │ Reuters         │  │ Al Jazeera   │   │ ║
║  │  │ Earthquake in   │  │ Floods hit      │  │ Wildfire     │   │ ║
║  │  │ Japan 7.2M      │  │ Bangladesh      │  │ spreads in   │   │ ║
║  │  │ [Analyze News]  │  │ [Analyze News]  │  │ Australia    │   │ ║
║  │  └─────────────────┘  └─────────────────┘  │ [Analyze News]   │ ║
║  │                                            └──────────────┘   │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │ MESSAGE INPUT                                                   │ ║
║  ├─────────────────────────────────────────────────────────────────┤ ║
║  │                                                                 │ ║
║  │ 📨 Enter disaster message:                                     │ ║
║  │ ┌─────────────────────────────────────────────────────────────┐│ ║
║  │ │ Heavy flooding in Mumbai, families trapped, need rescue... ││ ║
║  │ └─────────────────────────────────────────────────────────────┘│ ║
║  │                                                                 │ ║
║  │ [🔍 Analyze Message]    Or pick example: [Earthquake ▼]       │ ║
║  │                                                                 │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
║  (After clicking Analyze...)                                          ║
║                                                                       ║
║  ⚡ Analyzed in 0.003s                                                ║
║                                                                       ║
║  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐ ┌───────┐ ║
║  │ DISASTER       │ │ DISASTER TYPE  │ │ SEVERITY       │ │ PRIOR │ ║
║  │ DETECTED       │ │                │ │                │ │ SCORE │ ║
║  │                │ │ 🌊 Flood       │ │ 🟠 HIGH        │ │ 8/10  │ ║
║  │ YES ⚠️         │ │                │ │                │ │ [████▓│ ║
║  │                │ │                │ │                │ │       │ ║
║  └────────────────┘ └────────────────┘ └────────────────┘ └───────┘ ║
║                                                                       ║
║  📍 Location                        🆘 Required Response             ║
║  ┌────────────────────────────────┐ ┌──────────────────────────────┐ ║
║  │ 📍 Mumbai, India               │ │ • Rescue & Evacuation        │ ║
║  │ Lat: 19.0760, Lng: 72.8777     │ │ • Food & Water              │ ║
║  │                                 │ │ • Shelter                   │ ║
║  └────────────────────────────────┘ │ • Medical Assistance         │ ║
║                                      └──────────────────────────────┘ ║
║                                                                       ║
║  🔧 Recommended Action:                                               ║
║  Immediate emergency evacuation required. Coordinate with local       ║
║  disaster management for rescue operations and relief supplies.       ║
║                                                                       ║
║  [🎤 Play Voice Alert]  [📍 Show Map]  [📞 Helplines]               ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 🌍 TAB 2: GLOBE LIVE EVENTS (NEW - COMPLETELY REDESIGNED)

### **Top Section: Data Source Selection**

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║  Global Real-Time Disaster Intelligence Center                      ║
║                                                                       ║
║  Data Source & Fetch Options                                         ║
║                                                                       ║
║  [All Sources] [GDACS Only] [USGS Only] [NASA EONET] [Breaking News]║
║                                                                       ║
║  [Refresh Data]   Data updates every 5 minutes (cached)             ║
║                                                                       ║
║  Updated: 12 events from 4 sources                                   ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### **Real-Time Intelligence Dashboard**

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║  Real-Time Intelligence Dashboard                                    ║
║                                                                       ║
║  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   ║
║  │ TOTAL    │ │ CRITICAL │ │ HIGH     │ │ MEDIUM   │ │ LOW      │   ║
║  │ EVENTS   │ │          │ │          │ │          │ │          │   ║
║  │          │ │ 🔴       │ │ 🟠       │ │ 🔵       │ │ 🟢       │   ║
║  │    12    │ │    2     │ │    3     │ │    4     │ │    3     │   ║
║  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘   ║
║                                                                       ║
║  ┌──────────────┐                                                     ║
║  │ COUNTRIES    │                                                     ║
║  │ AFFECTED     │                                                     ║
║  │      8       │                                                     ║
║  └──────────────┘                                                     ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### **Tab Selection**

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║  [Overview Cards] [Global Map] [Breaking News] [Statistics] [Filters]║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### **TAB 2.1: Overview Cards (Sortable, Analyzable)**

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║  Active Disaster Events with Analysis                                ║
║                                                                       ║
║  Sort by: ○ Severity  ○ Date  ○ Country    Show: 10 [───────►]     ║
║                                                                       ║
║  ╔════════════════════════════════════════════════════╗              ║
║  ║ EARTHQUAKE IN NEPAL - MAGNITUDE 7.2               [Analyze]      ║
║  ║ Country: Nepal | Type: Earthquake                 ╚═════════════╝║
║  ║ Date: 2024-01-20 | Status: Ongoing                              ║
║  ║ Severity: CRITICAL | Source: USGS                                ║
║  ║ Coordinates: 28.15°N, 84.50°E                                     ║
║  ╚════════════════════════════════════════════════════╗              ║
║  ║ FLOODING IN BANGLADESH - 200K DISPLACED            [Analyze]      ║
║  ║ Country: Bangladesh | Type: Flood                 ╚═════════════╝║
║  ║ Date: 2024-01-20 | Status: Ongoing                              ║
║  ║ Severity: HIGH | Source: GDACS                                    ║
║  ║ Coordinates: 23.68°N, 90.36°E                                     ║
║  ╚════════════════════════════════════════════════════╗              ║
║  ║ WILDFIRE IN CALIFORNIA - 50K ACRES                 [Analyze]      ║
║  ║ Country: USA | Type: Wildfire                     ╚═════════════╝║
║  ║ Date: 2024-01-20 | Status: Active                                ║
║  ║ Severity: HIGH | Source: NASA EONET                              ║
║  ╚════════════════════════════════════════════════════╝              ║
║                                                                       ║
║  ... (more cards scrollable)                                         ║
║                                                                       ║
║  ╔═══════════════════════════════════════════════════════════════╗  ║
║  ║ DETAILED ANALYSIS & EMERGENCY RESPONSE (if analyzed)          ║  ║
║  ╟───────────────────────────────────────────────────────────────╢  ║
║  ║                                                               ║  ║
║  ║  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐           ║  ║
║  ║  │ AI ANALYSIS  │ │ REQUIRED     │ │ HELPLINE     │           ║  ║
║  ║  ├──────────────┤ │ RESPONSE     │ │ INFO         │           ║  ║
║  ║  │ Type:        │ │ ├─ Rescue    │ │ Nepal        │           ║  ║
║  ║  │ Earthquake   │ │ ├─ Shelter   │ │ Emergency:   │           ║  ║
║  ║  │              │ │ ├─ Medical   │ │ +977-1-4200  │           ║  ║
║  ║  │ Severity:    │ │ │            │ │              │           ║  ║
║  ║  │ CRITICAL     │ │ │            │ │ Earthquake   │           ║  ║
║  ║  │              │ │ │            │ │ Hotline:     │           ║  ║
║  ║  │ Priority:    │ │ │            │ │ +977-1-4200  │           ║  ║
║  ║  │ 9/10         │ │ │            │ │              │           ║  ║
║  ║  │              │ │ │            │ │ Red Cross:   │           ║  ║
║  ║  │ Confidence:  │ │ │            │ │ +977-1-4248  │           ║  ║
║  ║  │ 95%          │ │ │            │ │              │           ║  ║
║  ║  └──────────────┘ └──────────────┘ └──────────────┘           ║  ║
║  ║                                                               ║  ║
║  ║  Recommended Action:                                          ║  ║
║  ║  Emergency evacuation required. Deploy rescue teams            ║  ║
║  ║  immediately. Coordinate with disaster management authorities. ║  ║
║  ║                                                               ║  ║
║  ║  [🎤 Play Voice Alert]  [Close Analysis]                     ║  ║
║  ║                                                               ║  ║
║  ╚═══════════════════════════════════════════════════════════════╝  ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### **TAB 2.2: Global Map (Interactive)**

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║  Interactive Global Disaster Map                                     ║
║                                                                       ║
║  ┌──────────────────────────────────────────────────────────┐        ║
║  │                                                          │        ║
║  │        🌍 Folium Map with Disaster Markers              │        ║
║  │                                                          │        ║
║  │    🔴 = CRITICAL (Nepal Earthquake, Bangladesh Flood)   │        ║
║  │    🟠 = HIGH (California Fire, Indonesia Storm)         │        ║
║  │    🔵 = MEDIUM (Various regions)                        │        ║
║  │    🟢 = LOW (Monitoring alerts)                         │        ║
║  │                                                          │        ║
║  │  • Markers cluster when zoomed out                      │        ║
║  │  • Click markers for details                           │        ║
║  │  • Hover for quick info                                │        ║
║  │  • Pan/Zoom with mouse                                 │        ║
║  │  • [🔒 Fullscreen] button in corner                    │        ║
║  │                                                          │        ║
║  └──────────────────────────────────────────────────────────┘        ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### **TAB 2.3: Breaking News**

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║  Latest Breaking News & Headlines                                    ║
║                                                                       ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │ 🔴 BBC WORLD - 2024-01-20 10:30                                │ ║
║  │ Major earthquake strikes off coast of Sumatra, tsunami warnings  │ ║
║  │ issued for Indian Ocean region...                               │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │ 🟠 REUTERS - 2024-01-20 09:15                                  │ ║
║  │ Severe monsoon flooding in Southeast Asia affects 50,000 people  │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │ 🟠 AL JAZEERA - 2024-01-20 08:45                               │ ║
║  │ Wildfires spread across Australia as temperatures soar          │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
║  ... (more headlines scrollable)                                     ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### **TAB 2.4: Statistics**

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║  Disaster Statistics & Trends                                        ║
║                                                                       ║
║  By Disaster Type              By Country (Top 10)                   ║
║  ┌─────────────────────────┐   ┌─────────────────────────┐          ║
║  │                         │   │                         │          ║
║  │  Earthquake ████████ 5  │   │  Nepal       ███████ 4 │          ║
║  │  Flood ███████ 3        │   │  Bangladesh  ████ 2    │          ║
║  │  Fire ████ 2            │   │  Indonesia   ████ 2    │          ║
║  │  Storm ██ 1             │   │  Philippines ██ 1      │          ║
║  │  Landslide ██ 1         │   │  USA         ██ 1      │          ║
║  │                         │   │                         │          ║
║  └─────────────────────────┘   └─────────────────────────┘          ║
║                                                                       ║
║  (Scrollable bar charts)                                              ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### **TAB 2.5: Filters & Search**

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║  Advanced Filters & Search                                           ║
║                                                                       ║
║  Search by title or country:                                         ║
║  ┌────────────────────────────────┐                                  ║
║  │ earthquake nepal               │                                  ║
║  └────────────────────────────────┘                                  ║
║                                                                       ║
║  Filter by type:                                                      ║
║  ☑ Earthquake  ☑ Flood  ☐ Fire  ☐ Storm  ☐ Landslide               ║
║                                                                       ║
║  Found 3 matching events                                              ║
║  • Earthquake in Nepal - CRITICAL - USGS                            ║
║  • Earthquake aftershock - MEDIUM - USGS                            ║
║  • Recent seismic activity - LOW - GDACS                            ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 📊 TAB 3: DASHBOARD (Analytics)

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║  📊 Dashboard                                                         ║
║                                                                       ║
║  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐ ║
║  │ CASES TOTAL  │ │ HIGH PRIORITY│ │ TODAY        │ │ THIS WEEK  │ ║
║  │     145      │ │      23      │ │     12       │ │    87      │ ║
║  └──────────────┘ └──────────────┘ └──────────────┘ └────────────┘ ║
║                                                                       ║
║  Disaster Type Breakdown                                              ║
║  Flood: 45 (31%) | Earthquake: 35 (24%) | Fire: 28 (19%)            ║
║  Storm: 18 (12%) | Other: 19 (13%)                                   ║
║                                                                       ║
║  Severity Distribution                                                ║
║  Critical: 15 | High: 38 | Medium: 58 | Low: 34                    ║
║                                                                       ║
║  Recent Predictions                                                   ║
║  ├─ [10:32] Earthquake Nepal - CRITICAL - Priority 9                ║
║  ├─ [10:15] Flooding Mumbai - HIGH - Priority 7                     ║
║  ├─ [09:58] Fire Alert - MEDIUM - Priority 5                        ║
║  └─ [09:30] Storm Warning - MEDIUM - Priority 4                     ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 📞 Emergency Helpline Example

When you analyze a disaster from Nepal:

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║  Emergency Helpline - Nepal                                           ║
║                                                                       ║
║  🔴 Emergency Number: +977-1-4200                                    ║
║  🚨 Disaster Management: +977-1-4200 ext. 2                          ║
║  🚑 Ambulance: 102                                                    ║
║  🚒 Fire Department: 101                                              ║
║  🚔 Police: 100                                                       ║
║                                                                       ║
║  Local Organizations:                                                 ║
║  • Nepal Red Cross Society: +977-1-4248888                           ║
║  • Disaster Management Authority: +977-1-4270699                    ║
║  • Search & Rescue Team: +977-1-4263636                             ║
║                                                                       ║
║  International Support:                                               ║
║  • International Red Cross: +41-22-730-6001                          ║
║  • UNHCR: +1-202-296-5191                                            ║
║  • UNICEF: +1-212-326-7000                                           ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 🎤 Voice Alert Example

When you click "Play Voice Alert":

**Voice Output (Text-to-Speech):**
```
"Earthquake detected in Nepal. Magnitude: 7.2. Severity: Critical.
Priority score: 9 out of 10. Immediate rescue and shelter assistance
urgently needed. Coordinate with local disaster management authorities.
Emergency number: +977-1-4200. Red Cross contact: +977-1-4248888."
```

---

## 📱 Mobile View

The app is responsive and works on mobile:

```
┌─────────────────────────────┐
│  Disaster Intelligence      │
│  [☰ Menu]                   │
├─────────────────────────────┤
│                             │
│ Breaking News Headlines     │
│ [Swipe →]                   │
│                             │
│ 📨 Enter message:           │
│ ┌─────────────────────────┐ │
│ │ Heavy flooding in...    │ │
│ └─────────────────────────┘ │
│                             │
│ [Analyze] [Load Example]    │
│                             │
├─────────────────────────────┤
│  Results (if analyzed):     │
│                             │
│ ✅ YES - DISASTER           │
│ 🌊 Flood                    │
│ 🟠 HIGH                     │
│ 7/10 Priority               │
│                             │
│ [📍 Map] [📞 Helpline]      │
│                             │
└─────────────────────────────┘
```

---

## 🎯 Key UI Elements You'll See

### **Color Coding**
- 🔴 **RED** = CRITICAL severity
- 🟠 **ORANGE** = HIGH severity  
- 🔵 **BLUE** = MEDIUM severity
- 🟢 **GREEN** = LOW severity

### **Icons**
- 🚨 Emergency/Alert
- 🌊 Flooding
- 🔥 Fire
- 🏚️ Earthquake
- 🌀 Cyclone
- 📍 Location
- 📞 Helpline
- 🗺️ Map
- 📊 Dashboard
- ⚡ Breaking News

### **Interactive Elements**
- Buttons (Analyze, Refresh, Download)
- Sliders (Show X events)
- Radio buttons (Sort by)
- Checkboxes (Filter by type)
- Text inputs (Search)
- Dropdowns (Select example)

---

## ✅ Expected First Run Experience

```
1. Open browser → http://localhost:8501
2. See login/register screen
3. Enter credentials
4. See main dashboard
5. Click "Predict" tab
6. See breaking news headlines at top
7. Enter a message like "Earthquake in Nepal"
8. Get instant analysis in <5ms
9. See disaster type, severity, priority, location
10. Click "Show Helpline" to see emergency numbers
11. Click "Show Map" to see interactive map
12. Try "Globe Live Events" to explore 4 real APIs
13. See interactive map with 12+ disasters
14. Click "Analyze" on any disaster
15. See emergency info and helplines
16. Click "Play Voice Alert" to hear alert
17. Try "Dashboard" to see analytics
18. Export history from "📜 History" tab
```

---

**Ready to explore? Start the app now! 🚀**
