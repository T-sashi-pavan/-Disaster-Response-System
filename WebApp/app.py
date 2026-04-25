import os, sys, re, pickle, time
import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from Utils.disaster_analyzer import DisasterAnalyzer
from Utils.reliefweb_api import ReliefWebAPI
from Utils.disaster_analysis_engine import DisasterAnalysisEngine
from Utils.voice_output import VoiceOutput
from Utils.disaster_data_aggregator import DisasterDataAggregator
from Utils.helpline_database import DisasterHelplineDatabase
from Utils.disaster_map import DisasterMap

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DisasterAI — Emergency Response System",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Premium CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
*{font-family:'Inter',sans-serif;}
.stApp{background:linear-gradient(135deg,#0a0e1a 0%,#0d1b2e 50%,#0a1628 100%);color:#e2e8f0;}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#060d1a 0%,#0d1b2e 100%)!important;border-right:1px solid #1e3a5f;}
section[data-testid="stSidebar"] *{color:#cbd5e1!important;}
.stTextArea textarea{background:#0d1b2e!important;color:#e2e8f0!important;border:1px solid #1e3a5f!important;border-radius:12px!important;}
.stButton>button{background:linear-gradient(135deg,#dc2626,#b91c1c)!important;color:#fff!important;border:none!important;border-radius:12px!important;font-weight:700!important;padding:0.6rem 2rem!important;font-size:1rem!important;transition:all .3s!important;}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 8px 25px rgba(220,38,38,.4)!important;}
.card{background:linear-gradient(135deg,rgba(13,27,46,.9),rgba(6,13,26,.9));border:1px solid #1e3a5f;border-radius:16px;padding:1.2rem 1.5rem;margin-bottom:1rem;}
.card-red{border-color:#dc2626;background:linear-gradient(135deg,rgba(220,38,38,.15),rgba(13,27,46,.9));}
.card-yellow{border-color:#f59e0b;background:linear-gradient(135deg,rgba(245,158,11,.15),rgba(13,27,46,.9));}
.card-green{border-color:#10b981;background:linear-gradient(135deg,rgba(16,185,129,.15),rgba(13,27,46,.9));}
.card-blue{border-color:#3b82f6;background:linear-gradient(135deg,rgba(59,130,246,.15),rgba(13,27,46,.9));}
.badge{display:inline-block;padding:.3rem .9rem;border-radius:20px;font-weight:700;font-size:.85rem;margin:.2rem;}
.badge-red{background:rgba(220,38,38,.2);color:#fca5a5;border:1px solid #dc2626;}
.badge-green{background:rgba(16,185,129,.2);color:#6ee7b7;border:1px solid #10b981;}
.badge-yellow{background:rgba(245,158,11,.2);color:#fde68a;border:1px solid #f59e0b;}
.badge-blue{background:rgba(59,130,246,.2);color:#93c5fd;border:1px solid #3b82f6;}
.badge-purple{background:rgba(139,92,246,.2);color:#c4b5fd;border:1px solid #8b5cf6;}
.metric-card{background:rgba(13,27,46,.8);border:1px solid #1e3a5f;border-radius:12px;padding:1rem;text-align:center;}
.metric-val{font-size:2rem;font-weight:900;color:#f8fafc;}
.metric-lbl{font-size:.8rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.1em;}
.section-title{font-size:1.1rem;font-weight:700;color:#93c5fd;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.8rem;padding-bottom:.4rem;border-bottom:1px solid #1e3a5f;}
.action-item{background:rgba(13,27,46,.6);border-left:3px solid #3b82f6;border-radius:0 8px 8px 0;padding:.6rem 1rem;margin:.4rem 0;color:#e2e8f0;}
.auto-response{background:rgba(220,38,38,.1);border:1px solid #dc2626;border-radius:12px;padding:1.2rem;color:#fca5a5;font-style:italic;font-size:1.05rem;}
.priority-bar{height:12px;border-radius:6px;background:linear-gradient(90deg,#10b981,#f59e0b,#dc2626);margin:.5rem 0;}
h1{color:#f8fafc!important;} h2{color:#cbd5e1!important;} h3{color:#94a3b8!important;}
</style>
""", unsafe_allow_html=True)

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE, "..", "ModelFiles", "disaster_model.pkl")
USER_DB    = os.path.join(BASE, "users_db.json")

# ── Load Model ────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading AI model...")
def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

def tokenize(text):
    from nltk.stem import WordNetLemmatizer
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    lem = WordNetLemmatizer()
    try:
        return [lem.lemmatize(t) for t in text.split() if t]
    except Exception:
        return text.split()

sys.modules["__main__"].tokenize = tokenize
payload        = load_model()
model          = payload["model"]
CATEGORY_NAMES = payload["labels"]
BEST_MODEL     = payload.get("best_model", "ML Model")
analyzer       = DisasterAnalyzer()

# ── Session State ─────────────────────────────────────────────────────────────
for key, val in {
    "logged_in": False, "username": "",
    "history": [], "case_count": 0, "high_priority_count": 0,
    "last_disasters": [], "last_update_time": "", "selected_disaster": None, "show_analysis": False,
    "current_disasters": [], "fetch_mode": "all", "force_refresh": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Auth helpers ──────────────────────────────────────────────────────────────
import json

def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB) as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=2)

def auth_login(u, p):
    return any(x["username"] == u and x["password"] == p for x in load_users())

def auth_register(u, p, m, a):
    users = load_users()
    if any(x["username"] == u for x in users):
        return False
    users.append({"username": u, "password": p, "mobile": m, "address": a})
    save_users(users)
    return True

# ── Auth UI ───────────────────────────────────────────────────────────────────
def auth_ui():
    col = st.columns([1, 2, 1])[1]
    with col:
        st.markdown("""
        <div style='text-align:center;padding:2rem 0 1rem'>
          <div style='font-size:3rem'>🚨</div>
          <h1 style='font-size:2rem;font-weight:900;color:#f8fafc;'>DisasterAI</h1>
          <p style='color:#64748b;'>Advanced Emergency Response System</p>
        </div>""", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        with tab1:
            u = st.text_input("Username", key="li_u")
            p = st.text_input("Password", type="password", key="li_p")
            if st.button("Login", use_container_width=True):
                if auth_login(u, p):
                    st.session_state.logged_in = True
                    st.session_state.username  = u
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        with tab2:
            u2 = st.text_input("Username", key="rg_u")
            p2 = st.text_input("Password", type="password", key="rg_p")
            m2 = st.text_input("Mobile", key="rg_m")
            a2 = st.text_input("Address", key="rg_a")
            if st.button("Register", use_container_width=True):
                if auth_register(u2, p2, m2, a2):
                    st.success("✅ Registered! Please login.")
                else:
                    st.warning("Username already exists")

# ── Predict ───────────────────────────────────────────────────────────────────
def predict_ui():
    st.markdown("## 🚨 Disaster Intelligence Analysis")
    st.markdown(f"<div style='color:#64748b;font-size:.9rem'>Model: <b style='color:#3b82f6'>{BEST_MODEL}</b> · Enter a message below to analyze</div>", unsafe_allow_html=True)
    
    # ────────────────────────────────────────────────────────────────
    # BREAKING NEWS SECTION (TOP)
    # ────────────────────────────────────────────────────────────────
    
    st.markdown("<div class='section-title'>⚡ Breaking News Headlines</div>", unsafe_allow_html=True)
    
    try:
        if "data_aggregator" not in st.session_state:
            st.session_state.data_aggregator = DisasterDataAggregator()
        
        aggregator = st.session_state.data_aggregator
        news_result = aggregator.fetch_breaking_news(force_refresh=False)
        
        if news_result["status"] == "success":
            news_items = news_result.get("disasters", [])[:5]
            
            if news_items:
                news_cols = st.columns(min(len(news_items), 3))
                for idx, news in enumerate(news_items):
                    with news_cols[idx % 3]:
                        severity_color = {
                            "CRITICAL": "#dc2626",
                            "HIGH": "#f59e0b",
                            "MEDIUM": "#3b82f6",
                            "LOW": "#10b981"
                        }.get(news.get("severity", "MEDIUM"), "#3b82f6")
                        
                        st.markdown(f"""<div style='background:{severity_color}22; 
                        border-left:4px solid {severity_color}; 
                        padding:12px; border-radius:6px; margin:8px 0'>
                            <div style='color:{severity_color};font-weight:bold;font-size:0.9rem'>
                                {news.get('source', 'News')}
                            </div>
                            <div style='font-size:0.85rem;margin:6px 0'>
                                {news.get('title', 'Breaking news')[:80]}...
                            </div>
                            <div style='font-size:0.75rem;color:#94a3b8'>
                                {news.get('date', 'Just now')}
                            </div>
                        </div>""", unsafe_allow_html=True)
                        
                        if st.button("Analyze This News", key=f"news_btn_{idx}", use_container_width=True):
                            st.session_state.selected_disaster = news
                            st.session_state.show_analysis = True
            else:
                st.info("No breaking news available at the moment")
        else:
            st.info("News feed unavailable (using standard analysis)")
    
    except Exception as e:
        st.info("Breaking news not available - proceed with standard analysis")

    # ────────────────────────────────────────────────────────────────
    # MESSAGE INPUT SECTION
    # ────────────────────────────────────────────────────────────────

    text = st.text_area("📨 Enter disaster message:", height=130,
                        placeholder="e.g. Heavy flooding in Hyderabad, people are trapped and need rescue...")
    col_btn, col_ex = st.columns([1, 3])
    with col_btn:
        predict_clicked = st.button("🔍 Analyze Message", use_container_width=True)
    with col_ex:
        example = st.selectbox("Or pick an example:", [
            "— select —",
            "Severe flooding in Mumbai, families trapped, need rescue and food",
            "Massive earthquake hit Kathmandu, buildings collapsed, many injured",
            "Wildfire spreading rapidly near Bangalore, people evacuating",
            "Cyclone landfall near Chennai coast, wind speed 180 kmph",
            "Road accident on Delhi highway, critical injuries, ambulance needed",
        ])
        if example != "— select —":
            text = example

    if not predict_clicked:
        return
    if not text.strip():
        st.warning("⚠️ Please enter a message first.")
        return

    with st.spinner("🤖 AI analyzing..."):
        t0   = time.time()
        preds_arr = model.predict([text])[0]
        preds = {label: int(p) for label, p in zip(CATEGORY_NAMES, preds_arr)}
        elapsed = time.time() - t0

        detected      = analyzer.detect_disaster(preds)
        dtype         = analyzer.get_disaster_type(preds, text) if detected else "None"
        needs         = analyzer.get_needs(preds, text)
        severity      = analyzer.get_severity(text)
        priority      = analyzer.get_priority_score(severity, needs, dtype)
        location      = analyzer.extract_location(text)
        actions       = analyzer.get_recommended_actions(needs, severity, dtype)
        auto_response = analyzer.get_auto_response(detected, dtype, severity, location, needs)
        voice_text    = analyzer.get_voice_text(detected, dtype, severity, priority, location, needs, actions)

    # Update session history
    st.session_state.case_count += 1
    if priority >= 7:
        st.session_state.high_priority_count += 1
    st.session_state.history.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "message": text[:60] + "..." if len(text) > 60 else text,
        "disaster": "YES" if detected else "NO",
        "type": dtype,
        "severity": severity["level"],
        "priority": priority,
        "needs": ", ".join(needs) if needs else "—",
        "location": location[0] if location else "Unknown",
    })

    # ── Results ───────────────────────────────────────────────────────────
    sev_color = {"High": "red", "Medium": "yellow", "Low": "green"}.get(severity["level"], "blue")
    dis_color = "red" if detected else "green"

    st.markdown(f"<div style='text-align:right;color:#64748b;font-size:.8rem'>⚡ Analyzed in {elapsed:.2f}s</div>", unsafe_allow_html=True)

    # Row 1: Status + Type + Severity + Priority
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        label = "✅ YES — DISASTER" if detected else "✅ NO — SAFE"
        bg = "#dc2626" if detected else "#10b981"
        st.markdown(f"""<div class='metric-card' style='border-color:{bg}'>
            <div class='metric-lbl'>Disaster Detected</div>
            <div style='font-size:1.3rem;font-weight:900;color:{bg};margin:.3rem 0'>{"YES ⚠️" if detected else "NO ✅"}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        type_icons = {"Flood":"🌊","Fire":"🔥","Earthquake":"🏚️","Cyclone":"🌀","Accident":"🚧","General Emergency":"⚠️"}
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-lbl'>Disaster Type</div>
            <div class='metric-val' style='font-size:1.2rem'>{type_icons.get(dtype,'⚠️')} {dtype}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        sev_colors = {"High":"#dc2626","Medium":"#f59e0b","Low":"#10b981"}
        sc = sev_colors.get(severity["level"],"#64748b")
        st.markdown(f"""<div class='metric-card' style='border-color:{sc}'>
            <div class='metric-lbl'>Severity</div>
            <div class='metric-val' style='color:{sc}'>{severity["level"].upper()}</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        pbar = int(priority / 10 * 100)
        st.markdown(f"""<div class='metric-card' style='border-color:#8b5cf6'>
            <div class='metric-lbl'>Priority Score</div>
            <div class='metric-val' style='color:#c4b5fd'>{priority}/10</div>
            <div style='background:#1e293b;border-radius:6px;height:8px;margin-top:.4rem'>
              <div style='background:linear-gradient(90deg,#10b981,#f59e0b,#dc2626);width:{pbar}%;height:8px;border-radius:6px'></div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


    # Row 2: Location + Needs
    c_loc, c_needs = st.columns([1, 1])
    with c_loc:
        st.markdown("<div class='section-title'>📍 Location</div>", unsafe_allow_html=True)
        if location:
            st.markdown(f"<div class='badge badge-blue'>📍 {location[0]}</div>", unsafe_allow_html=True)
            if location[1]:
                st.markdown(f"<small style='color:#64748b'>Lat: {location[1]:.4f}, Lng: {location[2]:.4f}</small>", unsafe_allow_html=True)
                try:
                    import folium
                    from streamlit_folium import st_folium
                    m = folium.Map(location=[location[1], location[2]], zoom_start=11)
                    folium.Marker(
                        [location[1], location[2]],
                        popup=f"<b>{location[0]}</b><br>Severity: {severity['level']}<br>Type: {dtype}",
                        tooltip=location[0],
                        icon=folium.Icon(color="red" if detected else "green", icon="exclamation-sign"),
                    ).add_to(m)
                    st_folium(m, width=400, height=260)
                except ImportError:
                    st.info("Install streamlit-folium for map view")
        else:
            st.markdown("<div class='badge badge-yellow'>📍 Location not found</div>", unsafe_allow_html=True)
    with c_needs:
        st.markdown("<div class='section-title'>🆘 Required Help</div>", unsafe_allow_html=True)
        need_icons = {"Medical":"🏥","Shelter":"🏠","Food":"🍱","Rescue":"🚁"}
        need_badge = {"Medical":"badge-red","Shelter":"badge-yellow","Food":"badge-blue","Rescue":"badge-purple"}
        if needs:
            for n in needs:
                nb = need_badge.get(n, "badge-blue")
                ni = need_icons.get(n, "✅")
                st.markdown(f"<span class='badge {nb}'>{ni} {n}</span>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='badge badge-green'>✅ No specific needs detected</div>", unsafe_allow_html=True)
        if severity.get("matched"):
            st.markdown(f"<br><small style='color:#64748b'>Keywords: {', '.join(severity['matched'][:5])}</small>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 3: Actions + Auto Response
    c_act, c_resp = st.columns([1, 1])
    with c_act:
        st.markdown("<div class='section-title'>📋 Recommended Actions</div>", unsafe_allow_html=True)
        for i, act in enumerate(actions, 1):
            st.markdown(f"<div class='action-item'><b style='color:#93c5fd'>{i}.</b> {act}</div>", unsafe_allow_html=True)
    with c_resp:
        st.markdown("<div class='section-title'>📢 Auto Emergency Response</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='auto-response'>{auto_response}</div>", unsafe_allow_html=True)

    # Row 4: Voice output
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🔊 Voice Alert Output</div>", unsafe_allow_html=True)
    audio_bytes = analyzer.generate_voice_audio(voice_text)
    if audio_bytes:
        st.audio(audio_bytes, format="audio/mp3")
    else:
        st.info("⚠️ Voice output unavailable — install gTTS: `pip install gtts`")
        with st.expander("📄 Voice script"):
            st.write(voice_text)

    # Severity details expander
    with st.expander("🔬 Raw ML Predictions (All Categories)"):
        det = [{"Category": l, "Predicted": "✅ YES" if v == 1 else "❌ NO"}
               for l, v in preds.items()]
        st.dataframe(pd.DataFrame(det), use_container_width=True)

# ── Dashboard ─────────────────────────────────────────────────────────────────
def dashboard_ui():
    st.markdown("## 📊 Emergency Dashboard")
    history = st.session_state.history

    c1, c2, c3, c4 = st.columns(4)
    total    = st.session_state.case_count
    high_pri = st.session_state.high_priority_count
    disaster_yes = sum(1 for h in history if h["disaster"] == "YES")
    avg_prio = round(sum(h["priority"] for h in history) / len(history), 1) if history else 0

    for col, val, lbl, color in [
        (c1, total,       "Total Cases",        "#3b82f6"),
        (c2, high_pri,    "High Priority",      "#dc2626"),
        (c3, disaster_yes,"Disasters Detected", "#f59e0b"),
        (c4, avg_prio,    "Avg Priority",       "#8b5cf6"),
    ]:
        with col:
            col.markdown(f"""<div class='metric-card' style='border-color:{color}'>
                <div class='metric-lbl'>{lbl}</div>
                <div class='metric-val' style='color:{color}'>{val}</div>
            </div>""", unsafe_allow_html=True)

    if not history:
        st.info("📭 No predictions yet. Go to Predict to get started!")
        return

    st.markdown("<br>", unsafe_allow_html=True)
    df = pd.DataFrame(history)

    c_left, c_right = st.columns(2)
    with c_left:
        st.markdown("<div class='section-title'>🌍 Disaster Type Distribution</div>", unsafe_allow_html=True)
        type_counts = df["type"].value_counts().reset_index()
        type_counts.columns = ["Type", "Count"]
        st.bar_chart(type_counts.set_index("Type"), use_container_width=True)
    with c_right:
        st.markdown("<div class='section-title'>⚠️ Severity Distribution</div>", unsafe_allow_html=True)
        sev_counts = df["severity"].value_counts().reset_index()
        sev_counts.columns = ["Severity", "Count"]
        st.bar_chart(sev_counts.set_index("Severity"), use_container_width=True)

    st.markdown("<div class='section-title'>📋 Recent Cases</div>", unsafe_allow_html=True)
    st.dataframe(df.tail(20)[::-1], use_container_width=True)

    csv = df.to_csv(index=False).encode()
    st.download_button("📥 Export All Cases (CSV)", csv, "disaster_cases.csv", "text/csv")

# ── History ───────────────────────────────────────────────────────────────────
def history_ui():
    st.markdown("## 📜 Prediction History")
    if not st.session_state.history:
        st.info("📭 No predictions yet.")
        return
    df = pd.DataFrame(st.session_state.history[::-1])
    for _, row in df.iterrows():
        sev_c = {"High":"card-red","Medium":"card-yellow","Low":"card-green"}.get(row["severity"],"card")
        st.markdown(f"""<div class='card {sev_c}'>
            <b>{row['time']}</b> &nbsp;|&nbsp;
            <span class='badge badge-{"red" if row["disaster"]=="YES" else "green"}'>{row["disaster"]}</span>&nbsp;
            <span class='badge badge-blue'>{row["type"]}</span>&nbsp;
            <span class='badge badge-purple'>Priority {row["priority"]}/10</span>&nbsp;
            <span class='badge badge-yellow'>{row["severity"]}</span>
            <br><small style='color:#94a3b8'>{row["message"]}</small>
        </div>""", unsafe_allow_html=True)

# ── Help ──────────────────────────────────────────────────────────────────────
def help_ui():
    st.markdown("## ❓ Help & Documentation")
    st.markdown("""
    ### How to Use
    1. Go to **Predict** in the sidebar
    2. Type or paste a disaster message
    3. Click **Analyze Message**
    4. Results appear instantly with voice output

    ### Feature Guide
    | Feature | Description |
    |---|---|
    | Disaster Detection | YES/NO based on ML + keywords |
    | Disaster Type | Flood / Fire / Earthquake / Cyclone / Accident |
    | Severity | High / Medium / Low based on keywords |
    | Priority Score | 1–10 urgency score |
    | Needs | Medical / Shelter / Food / Rescue |
    | Location | Extracted from text (150+ cities) |
    | Actions | AI-generated response recommendations |
    | Auto Response | Emergency summary statement |
    | Map | Folium map if location is found |
    | Voice | Audio alert via gTTS |

    ### Sample Test Messages
    - `"Severe flooding in Mumbai, families are trapped, urgent rescue needed"`
    - `"Earthquake in Kathmandu, buildings collapsed, people injured, need medical help"`
    - `"Cyclone approaching Chennai coast, wind speed 180 kmph"`
    - `"Fire broke out in a building in Delhi, people trapped on 5th floor"`
    - `"Warning: Heavy rainfall expected in Hyderabad area, prepare"`
    """)

# ── Live Disasters ────────────────────────────────────────────────────────────
def live_disasters_ui():
    """Display live global disaster events from multiple sources (GDACS, USGS, EONET, News)"""
    st.markdown("## Global Real-Time Disaster Intelligence Center")
    
    # Initialize all components
    if "data_aggregator" not in st.session_state:
        st.session_state.data_aggregator = DisasterDataAggregator()
    if "helpline_db" not in st.session_state:
        st.session_state.helpline_db = DisasterHelplineDatabase()
    if "disaster_analyzer" not in st.session_state:
        st.session_state.disaster_analyzer = DisasterAnalysisEngine()
    if "disaster_map" not in st.session_state:
        st.session_state.disaster_map = DisasterMap()
    if "voice_output" not in st.session_state:
        try:
            st.session_state.voice_output = VoiceOutput()
        except:
            st.session_state.voice_output = None
    
    aggregator = st.session_state.data_aggregator
    helpline_db = st.session_state.helpline_db
    analyzer = st.session_state.disaster_analyzer
    disaster_map = st.session_state.disaster_map
    voice = st.session_state.voice_output
    
    # ────────────────────────────────────────────────────────────────
    # DATA SOURCE SELECTION & CONTROLS
    # ────────────────────────────────────────────────────────────────
    
    st.markdown("<div class='section-title'>Data Source & Fetch Options</div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("All Sources", key="btn_all", use_container_width=True):
            st.session_state.fetch_mode = "all"
    
    with col2:
        if st.button("GDACS Only", key="btn_gdacs", use_container_width=True):
            st.session_state.fetch_mode = "gdacs"
    
    with col3:
        if st.button("USGS Earthquakes", key="btn_usgs", use_container_width=True):
            st.session_state.fetch_mode = "usgs"
    
    with col4:
        if st.button("NASA EONET", key="btn_eonet", use_container_width=True):
            st.session_state.fetch_mode = "eonet"
    
    with col5:
        if st.button("Breaking News", key="btn_news", use_container_width=True):
            st.session_state.fetch_mode = "news"
    
    fetch_mode = st.session_state.get("fetch_mode", "all")
    
    col_refresh, col_auto = st.columns([2, 3])
    with col_refresh:
        if st.button("Refresh Data", key="refresh_btn", use_container_width=True):
            st.session_state.force_refresh = True
    with col_auto:
        st.markdown("<div style='text-align:center;color:#94a3b8;padding:0.4rem'>Data updates every 5 minutes (cached)</div>", unsafe_allow_html=True)
    
    # ────────────────────────────────────────────────────────────────
    # FETCH DISASTERS
    # ────────────────────────────────────────────────────────────────
    
    force_refresh = st.session_state.get("force_refresh", False)
    
    with st.spinner("Fetching from real-time disaster sources..."):
        if fetch_mode == "all":
            result = aggregator.fetch_all_sources(force_refresh)
        elif fetch_mode == "gdacs":
            result = aggregator.fetch_gdacs_disasters(force_refresh)
        elif fetch_mode == "usgs":
            result = aggregator.fetch_usgs_earthquakes(force_refresh)
        elif fetch_mode == "eonet":
            result = aggregator.fetch_eonet_events(force_refresh)
        elif fetch_mode == "news":
            result = aggregator.fetch_breaking_news(force_refresh)
        else:
            result = aggregator.fetch_all_sources(force_refresh)
        
        if result["status"] == "success":
            disasters = result.get("disasters", [])
            st.session_state.current_disasters = disasters
            st.session_state.fetch_mode = fetch_mode
            st.session_state.force_refresh = False
            st.success(f"Updated: {len(disasters)} events from {len(result.get('sources', []))} sources")
        else:
            st.error("Failed to fetch disaster data")
            disasters = st.session_state.get("current_disasters", [])
    
    if not disasters:
        st.warning("No disaster data available")
        return
    
    # ────────────────────────────────────────────────────────────────
    # REAL-TIME METRICS & STATISTICS
    # ────────────────────────────────────────────────────────────────
    
    stats = aggregator.get_statistics()
    
    st.markdown("<div class='section-title'>Real-Time Intelligence Dashboard</div>", unsafe_allow_html=True)
    
    metric_cols = st.columns(6)
    
    with metric_cols[0]:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-val'>{stats['total_events']}</div>
            <div class='metric-lbl'>Total Events</div>
        </div>""", unsafe_allow_html=True)
    
    with metric_cols[1]:
        st.markdown(f"""<div class='metric-card' style='border-color:#dc2626'>
            <div class='metric-val' style='color:#dc2626'>{stats['critical']}</div>
            <div class='metric-lbl'>Critical</div>
        </div>""", unsafe_allow_html=True)
    
    with metric_cols[2]:
        st.markdown(f"""<div class='metric-card' style='border-color:#f59e0b'>
            <div class='metric-val' style='color:#f59e0b'>{stats['high']}</div>
            <div class='metric-lbl'>High</div>
        </div>""", unsafe_allow_html=True)
    
    with metric_cols[3]:
        st.markdown(f"""<div class='metric-card' style='border-color:#3b82f6'>
            <div class='metric-val' style='color:#3b82f6'>{stats['medium']}</div>
            <div class='metric-lbl'>Medium</div>
        </div>""", unsafe_allow_html=True)
    
    with metric_cols[4]:
        st.markdown(f"""<div class='metric-card' style='border-color:#10b981'>
            <div class='metric-val' style='color:#10b981'>{stats['low']}</div>
            <div class='metric-lbl'>Low</div>
        </div>""", unsafe_allow_html=True)
    
    with metric_cols[5]:
        unique_countries = len(set(d.get("country", "Unknown") for d in disasters))
        st.markdown(f"""<div class='metric-card' style='border-color:#8b5cf6'>
            <div class='metric-val' style='color:#c4b5fd'>{unique_countries}</div>
            <div class='metric-lbl'>Countries</div>
        </div>""", unsafe_allow_html=True)
    
    # ────────────────────────────────────────────────────────────────
    # TABS FOR DIFFERENT VIEWS
    # ────────────────────────────────────────────────────────────────
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Overview Cards",
        "Global Map",
        "Breaking News",
        "Statistics",
        "Filters & Search"
    ])
    
    # ────── TAB 1: OVERVIEW CARDS ──────
    with tab1:
        st.markdown("**Active Disaster Events with Analysis**")
        
        # Filter and sort
        col_sort, col_limit = st.columns(2)
        with col_sort:
            sort_by = st.radio("Sort by:", ["Severity", "Date", "Country"], horizontal=True)
        with col_limit:
            show_count = st.slider("Show events:", 1, min(20, len(disasters)), 10)
        
        # Sort disasters
        if sort_by == "Severity":
            severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
            sorted_disasters = sorted(disasters, 
                                    key=lambda x: severity_order.get(x.get("severity", "LOW"), 4))
        elif sort_by == "Date":
            sorted_disasters = sorted(disasters, key=lambda x: x.get("date", ""), reverse=True)
        else:
            sorted_disasters = sorted(disasters, key=lambda x: x.get("country", ""))
        
        # Display cards
        for idx, disaster in enumerate(sorted_disasters[:show_count]):
            severity_color = {
                "CRITICAL": "card-red",
                "HIGH": "card-yellow",
                "MEDIUM": "card-blue",
                "LOW": "card-green"
            }.get(disaster.get("severity", "MEDIUM"), "card")
            
            col_card, col_btns = st.columns([4, 1])
            
            with col_card:
                st.markdown(f"""<div class='card {severity_color}'>
                    <b>{disaster.get('title', 'Unknown')}</b><br>
                    <small>Country: <b>{disaster.get('country', 'Unknown')}</b> | Type: {disaster.get('type', 'Unknown')}</small><br>
                    <small>Date: {disaster.get('date', 'Unknown')} | Status: {disaster.get('status', 'Unknown')}</small><br>
                    <span class='badge badge-yellow'>Severity: {disaster.get('severity', 'Unknown')}</span>
                    <span class='badge badge-blue'>Source: {disaster.get('source', 'Unknown')}</span>
                </div>""", unsafe_allow_html=True)
            
            with col_btns:
                if st.button("Analyze", key=f"analyze_{idx}", use_container_width=True):
                    st.session_state.selected_disaster = disaster
                    st.session_state.show_analysis = True
        
        # ────── ANALYSIS RESULTS ──────
        if st.session_state.get("show_analysis") and "selected_disaster" in st.session_state:
            disaster = st.session_state.selected_disaster
            
            st.markdown("<div class='section-title'>Detailed Analysis & Emergency Response</div>", unsafe_allow_html=True)
            
            # Analyze
            analysis_text = f"{disaster.get('title', '')} in {disaster.get('country', '')}"
            analysis = analyzer.analyze_disaster_text(
                text=analysis_text,
                country=disaster.get('country'),
                disaster_type_hint=disaster.get('type')
            )
            
            # 3-column layout
            an_col1, an_col2, an_col3 = st.columns(3)
            
            with an_col1:
                st.markdown(f"""<div class='card card-red'>
                    <b>AI Analysis</b><br><br>
                    Type: {analysis['disaster_type']}<br>
                    Severity: {analysis['severity']}<br>
                    Priority: {analysis['priority_score']}/10<br>
                    Confidence: {analysis['confidence']:.0%}
                </div>""", unsafe_allow_html=True)
            
            with an_col2:
                st.markdown(f"""<div class='card card-blue'>
                    <b>Required Response</b><br><br>
                    {chr(10).join([f'• {h}' for h in analysis.get('required_help', [])])}
                </div>""", unsafe_allow_html=True)
            
            with an_col3:
                st.markdown(f"""<div class='card card-green'>
                    <b>Helpline Info</b><br><br>
                    {disaster.get('country', 'Unknown')}
                </div>""", unsafe_allow_html=True)
            
            st.markdown(f"**Recommended Action:** {analysis['recommended_action']}")
            
            # Show helpline for country
            helpline = helpline_db.get_helpline_for_country(disaster.get('country', ''))
            if helpline["status"] == "success":
                st.markdown("<div class='section-title'>Emergency Helpline</div>", unsafe_allow_html=True)
                col_em, col_dis, col_fire = st.columns(3)
                with col_em:
                    st.markdown(f"<div class='badge badge-red'>**Emergency:** {helpline['emergency']}</div>", unsafe_allow_html=True)
                with col_dis:
                    st.markdown(f"<div class='badge badge-yellow'>**Disaster Mgmt:** {helpline['disaster_management']}</div>", unsafe_allow_html=True)
                with col_fire:
                    st.markdown(f"<div class='badge badge-blue'>**Ambulance:** {helpline['contacts']['ambulance']}</div>", unsafe_allow_html=True)
                
                # Show organizations
                if helpline.get("organizations"):
                    st.markdown("**Local Organizations:**")
                    for org in helpline["organizations"][:3]:
                        st.markdown(f"- {org['name']}: {org['phone']}")
            
            # Voice alert
            if voice:
                if st.button("Play Voice Alert", key="voice_alert_btn"):
                    voice.speak_disaster_alert({
                        "title": disaster.get('title'),
                        "country": disaster.get('country'),
                        "disaster_type": analysis['disaster_type'],
                        "severity": analysis['severity'],
                        "priority_score": analysis['priority_score'],
                        "required_help": analysis['required_help'],
                        "recommended_action": analysis['recommended_action']
                    })
                    st.success("Voice alert playing...")
            
            if st.button("Close Analysis"):
                st.session_state.show_analysis = False
                st.rerun()
    
    # ────── TAB 2: GLOBAL MAP ──────
    with tab2:
        st.markdown("**Interactive Global Disaster Map**")
        
        try:
            disaster_map_obj = disaster_map.create_disaster_map(disasters, "Global Disasters Map")
            from streamlit_folium import st_folium
            st_folium(disaster_map_obj, width=1200, height=600)
        except Exception as e:
            st.error(f"Map error: {str(e)}")
    
    # ────── TAB 3: BREAKING NEWS ──────
    with tab3:
        st.markdown("**Latest Breaking News & Headlines**")
        
        news_disasters = [d for d in disasters if d.get("source") in ["BBC World", "Reuters", "Al Jazeera"]]
        
        if news_disasters:
            for news in news_disasters[:15]:
                severity_bg = {
                    "CRITICAL": "#dc2626",
                    "HIGH": "#f59e0b",
                    "MEDIUM": "#3b82f6",
                    "LOW": "#10b981"
                }.get(news.get("severity"), "#3b82f6")
                
                st.markdown(f"""<div style='background:{severity_bg}; 
                color:white; padding:12px; border-radius:8px; margin:8px 0'>
                    <b>{news.get('title', 'Breaking News')}</b><br>
                    <small>Source: {news.get('source', 'Unknown')} | {news.get('date', 'Unknown')}</small><br>
                    {news.get('description', '')}
                </div>""", unsafe_allow_html=True)
        else:
            st.info("No breaking news available")
    
    # ────── TAB 4: STATISTICS ──────
    with tab4:
        st.markdown("**Disaster Statistics & Trends**")
        
        # Disaster type distribution
        if stats['by_type']:
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.markdown("**By Disaster Type**")
                type_df = pd.DataFrame(list(stats['by_type'].items()), columns=['Type', 'Count'])
                st.bar_chart(type_df.set_index('Type'))
            
            with col_chart2:
                st.markdown("**By Country (Top 10)**")
                country_df = pd.DataFrame(list(stats['by_country'].items()), columns=['Country', 'Count'])
                country_df = country_df.nlargest(10, 'Count')
                st.bar_chart(country_df.set_index('Country'))
    
    # ────── TAB 5: FILTERS & SEARCH ──────
    with tab5:
        st.markdown("**Advanced Filters & Search**")
        
        col_search, col_type = st.columns(2)
        
        with col_search:
            search_text = st.text_input("Search by title or country:")
        
        with col_type:
            disaster_types = list(set(d.get("type", "Unknown") for d in disasters))
            selected_type = st.multiselect("Filter by type:", disaster_types)
        
        # Apply filters
        filtered = disasters
        
        if search_text:
            filtered = [d for d in filtered if search_text.lower() in 
                       (d.get("title", "").lower() + d.get("country", "").lower())]
        
        if selected_type:
            filtered = [d for d in filtered if d.get("type") in selected_type]
        
        st.markdown(f"**Found {len(filtered)} matching events**")
        
        for disaster in filtered:
            st.markdown(f"- **{disaster.get('title')}** ({disaster.get('country')}) - {disaster.get('type')} - {disaster.get('severity')}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    if not st.session_state.logged_in:
        auth_ui()
        return

    st.sidebar.markdown("""
    <div style='text-align:center;padding:1rem 0'>
      <div style='font-size:2rem'>🚨</div>
      <div style='font-weight:900;font-size:1.1rem;color:#f8fafc'>DisasterAI</div>
      <div style='font-size:.75rem;color:#64748b'>Emergency Response System</div>
    </div>""", unsafe_allow_html=True)

    page = st.sidebar.radio("Navigate", [
        "🔍 Predict", "📊 Dashboard", "Globe Live Events", "📜 History", "❓ Help"
    ])
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"<small style='color:#475569'>👤 {st.session_state.username}</small>", unsafe_allow_html=True)
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if   page == "🔍 Predict":   predict_ui()
    elif page == "📊 Dashboard": dashboard_ui()
    elif page == "Globe Live Events": live_disasters_ui()
    elif page == "📜 History":   history_ui()
    elif page == "❓ Help":      help_ui()

if __name__ == "__main__":
    main()
