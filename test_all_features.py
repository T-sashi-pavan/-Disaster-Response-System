"""
test_all_features.py
====================
Tests ALL features of the Disaster Management AI system
WITHOUT needing Streamlit running. Run from project root.

Usage:
    python test_all_features.py
"""

import sys, os, re, json, pickle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Must define tokenize in __main__ BEFORE loading pickle ───────────────────
try:
    from nltk.stem import WordNetLemmatizer as _WNL
    _lem = _WNL()
    def tokenize(text):
        text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
        try:
            return [_lem.lemmatize(t) for t in text.split() if t]
        except Exception:
            return text.split()
except Exception:
    def tokenize(text):
        return re.sub(r"[^a-zA-Z0-9]", " ", text.lower()).split()

sys.modules["__main__"].tokenize = tokenize

PASS = "PASS"
FAIL = "FAIL"
results = []

def check(name, condition, got="", expected=""):
    status = PASS if condition else FAIL
    results.append((status, name, str(got), str(expected)))
    mark = "[PASS]" if condition else "[FAIL]"
    print(f"  {mark}  {name}")
    if not condition:
        print(f"         Got:      {got}")
        print(f"         Expected: {expected}")

print("\n" + "="*60)
print("  DisasterAI — Full Feature Test Suite")
print("="*60)

# ─────────────────────────────────────────────────────────────
# 1. NLTK Import
# ─────────────────────────────────────────────────────────────
print("\n[1] NLTK & Dependencies")
try:
    import nltk
    from nltk.stem import WordNetLemmatizer
    lem = WordNetLemmatizer()
    result = lem.lemmatize("running")
    check("NLTK imports OK",         True)
    check("WordNetLemmatizer works", result in ["running", "run"], result, "run/running")
except Exception as e:
    check("NLTK imports OK", False, str(e), "no error")

# ─────────────────────────────────────────────────────────────
# 2. Model Loading
# ─────────────────────────────────────────────────────────────
print("\n[2] ML Model Loading")
MODEL_PATH = os.path.join("ModelFiles", "disaster_model.pkl")
try:
    with open(MODEL_PATH, "rb") as f:
        payload = pickle.load(f)
    model          = payload["model"]
    CATEGORY_NAMES = payload["labels"]
    BEST_MODEL     = payload.get("best_model", "Unknown")
    check("Model file loads",          True)
    check("Labels list present",       len(CATEGORY_NAMES) > 0, len(CATEGORY_NAMES), ">0")
    check("Best model name present",   BEST_MODEL != "", BEST_MODEL, "non-empty string")
    check("Pipeline has tfidf step",   "tfidf" in model.named_steps, list(model.named_steps.keys()), "tfidf")
    check("Pipeline has clf step",     "clf"   in model.named_steps, list(model.named_steps.keys()), "clf")
except Exception as e:
    check("Model file loads", False, str(e), "no error")
    print("  [ABORT] Cannot continue without model.")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────
# 3. Disaster Analyzer Module
# ─────────────────────────────────────────────────────────────
print("\n[3] DisasterAnalyzer Module")
try:
    from Utils.disaster_analyzer import DisasterAnalyzer
    a = DisasterAnalyzer()
    check("DisasterAnalyzer imports OK", True)
except Exception as e:
    check("DisasterAnalyzer imports OK", False, str(e))
    sys.exit(1)

# ─────────────────────────────────────────────────────────────
# 4. Feature 1: Disaster Detection
# ─────────────────────────────────────────────────────────────
print("\n[4] Feature 1 — Disaster Detection")
msg_disaster  = "Severe flooding in Mumbai, people trapped and critically injured"
msg_safe      = "The weather is nice today, going for a walk in the park"

preds_dis  = {l: int(v) for l, v in zip(CATEGORY_NAMES, model.predict([msg_disaster])[0])}
preds_safe = {l: int(v) for l, v in zip(CATEGORY_NAMES, model.predict([msg_safe])[0])}

det_dis  = a.detect_disaster(preds_dis)
det_safe = a.detect_disaster(preds_safe)

check("Disaster detected for emergency msg",  det_dis  == True,  det_dis,  True)
check("No disaster for non-emergency msg",    det_safe == False, det_safe, False)

# ─────────────────────────────────────────────────────────────
# 5. Feature 2: Disaster Type
# ─────────────────────────────────────────────────────────────
print("\n[5] Feature 2 — Disaster Type Classification")
test_types = [
    ("Severe flood in Hyderabad, water rising fast, people displaced",       "Flood"),
    ("Wildfire burning near Bangalore, flames spreading rapidly",             "Fire"),
    ("Magnitude 7 earthquake hit Nepal, buildings collapsed",                 "Earthquake"),
    ("Cyclone landfall near Chennai coast, wind speed 180 kmph",             "Cyclone"),
    ("Major train derailment and road accident near Delhi, multiple collision", "Accident"),
]
for msg, expected in test_types:
    preds = {l: int(v) for l, v in zip(CATEGORY_NAMES, model.predict([msg])[0])}
    got   = a.get_disaster_type(preds, msg)
    check(f"Type: {expected}", got == expected, got, expected)

# ─────────────────────────────────────────────────────────────
# 6. Feature 3: Multi-Label Needs
# ─────────────────────────────────────────────────────────────
print("\n[6] Feature 3 — Multi-Label Needs Detection")
msg_needs = "Earthquake victims need medical help, food, water and rescue from collapsed buildings"
preds_n   = {l: int(v) for l, v in zip(CATEGORY_NAMES, model.predict([msg_needs])[0])}
needs     = a.get_needs(preds_n, msg_needs)

check("Needs list is a list",    isinstance(needs, list),   type(needs), list)
check("Medical need detected",   "Medical" in needs,        needs, "contains Medical")
check("Food need detected",      "Food"    in needs,        needs, "contains Food")
check("Rescue need detected",    "Rescue"  in needs,        needs, "contains Rescue")

# ─────────────────────────────────────────────────────────────
# 7. Feature 4: Severity Detection
# ─────────────────────────────────────────────────────────────
print("\n[7] Feature 4 — Severity Detection")
sev_tests = [
    ("people are trapped and critically injured, bodies found",           "High"),
    ("help needed, road blocked, people stranded and displaced",          "Medium"),
    ("flood warning issued, prepare and take precautions",               "Low"),
]
for msg, expected in sev_tests:
    sev = a.get_severity(msg)
    check(f"Severity: {expected}", sev["level"] == expected, sev["level"], expected)
    check(f"Score > 0 for {expected}", sev["score"] > 0, sev["score"], ">0")

# ─────────────────────────────────────────────────────────────
# 8. Feature 5: Priority Score
# ─────────────────────────────────────────────────────────────
print("\n[8] Feature 5 — Priority Score (1-10)")
sev_high   = {"level": "High",   "score": 90}
sev_medium = {"level": "Medium", "score": 55}
sev_low    = {"level": "Low",    "score": 15}

p_high   = a.get_priority_score(sev_high,   ["Medical","Rescue"], "Earthquake")
p_medium = a.get_priority_score(sev_medium, ["Shelter"],          "Flood")
p_low    = a.get_priority_score(sev_low,    [],                   "General Emergency")

check("High priority >= 8",    p_high   >= 8,  p_high,   ">=8")
check("Medium priority 4-7",   4 <= p_medium <= 7, p_medium, "4-7")
check("Low priority <= 4",     p_low    <= 4,  p_low,    "<=4")
check("Score within 1-10",     1 <= p_high <= 10, p_high, "1-10")

# ─────────────────────────────────────────────────────────────
# 9. Feature 6: Location Extraction
# ─────────────────────────────────────────────────────────────
print("\n[9] Feature 6 — Location Extraction")
loc_tests = [
    ("Severe flooding in Hyderabad near Tank Bund",  "Hyderabad"),
    ("Earthquake in Mumbai, buildings collapsed",     "Mumbai"),
    ("Cyclone warning for Chennai coastal area",      "Chennai"),
    ("Fire broke out in Delhi residential area",      "Delhi"),
]
for msg, expected in loc_tests:
    loc = a.extract_location(msg)
    found = loc[0].lower() if loc else ""
    check(f"Location: {expected}", expected.lower() in found, loc, expected)

loc_none = a.extract_location("There was a disaster somewhere")
check("Returns None when no location", loc_none is None, loc_none, None)

# ─────────────────────────────────────────────────────────────
# 10. Feature 7: Recommended Actions
# ─────────────────────────────────────────────────────────────
print("\n[10] Feature 7 — AI Recommended Actions")
actions = a.get_recommended_actions(["Medical","Rescue"], sev_high, "Earthquake")
check("Actions list not empty",           len(actions) > 0, len(actions), ">0")
check("Actions are strings",              all(isinstance(x, str) for x in actions), True, True)
check("At least 2 actions returned",      len(actions) >= 2, len(actions), ">=2")
check("General Earthquake action added",  any("inspect" in ac.lower() or "structur" in ac.lower() or "build" in ac.lower() for ac in actions), actions, "earthquake action")
clean_actions = [re.sub(r'[^\x00-\x7F]+', '', ac) for ac in actions[:3]]
print(f"         Actions: {clean_actions}")

# ─────────────────────────────────────────────────────────────
# 11. Feature 8: Auto Response Generator
# ─────────────────────────────────────────────────────────────
print("\n[11] Feature 8 — Auto Response Generator")
loc_hyd = ("Hyderabad", 17.38, 78.48)
resp_high = a.get_auto_response(True,  "Flood", sev_high,   loc_hyd, ["Medical","Rescue"])
resp_safe = a.get_auto_response(False, "None",  sev_low,    None,    [])

check("Response is string",                 isinstance(resp_high, str), type(resp_high), str)
check("High response contains location",    "Hyderabad" in resp_high,  resp_high[:80], "Hyderabad")
check("High response shows urgency",        any(w in resp_high.upper() for w in ["EMERGENCY","CRITICAL","IMMEDIATE"]), resp_high[:80])
check("Safe response indicates no disaster", "No emergency" in resp_safe or "non-disaster" in resp_safe.lower(), resp_safe[:80])
clean_resp = re.sub(r'[^\x00-\x7F]+', '', resp_high)
print(f"         Response: {clean_resp[:100]}...")

# ─────────────────────────────────────────────────────────────
# 12. Feature 9: Dashboard Data (Session State Logic)
# ─────────────────────────────────────────────────────────────
print("\n[12] Feature 9 — Dashboard Data Aggregation")
# Simulate session state counting
history = []
for msg in [msg_disaster, msg_safe, msg_needs]:
    preds  = {l: int(v) for l, v in zip(CATEGORY_NAMES, model.predict([msg])[0])}
    det    = a.detect_disaster(preds)
    dtype  = a.get_disaster_type(preds, msg)
    sev    = a.get_severity(msg)
    needs_ = a.get_needs(preds, msg)
    pri    = a.get_priority_score(sev, needs_, dtype)
    history.append({"disaster": "YES" if det else "NO", "type": dtype,
                    "severity": sev["level"], "priority": pri})

check("History list populated",         len(history) == 3,  len(history), 3)
check("Each entry has disaster field",  all("disaster" in h for h in history), True, True)
check("Each entry has type field",      all("type"     in h for h in history), True, True)
check("Each entry has priority",        all("priority" in h for h in history), True, True)
check("Priority values in 1-10",        all(1 <= h["priority"] <= 10 for h in history), True, True)

# ─────────────────────────────────────────────────────────────
# 13. Feature 10: Map Integration (Coordinates)
# ─────────────────────────────────────────────────────────────
print("\n[13] Feature 10 — Map Integration")
loc_data = [
    ("flooding in Mumbai river area",   "Mumbai",    19.07,  72.87),
    ("earthquake in Delhi near India gate", "Delhi", 28.61,  77.20),
    ("cyclone hit Kolkata coast",       "Kolkata",   22.57,  88.36),
]
for msg, city, exp_lat, exp_lng in loc_data:
    loc = a.extract_location(msg)
    if loc and loc[1]:
        lat_ok = abs(loc[1] - exp_lat) < 1.0
        lng_ok = abs(loc[2] - exp_lng) < 1.0
        check(f"Map coords for {city}",  lat_ok and lng_ok,
              f"({loc[1]:.2f},{loc[2]:.2f})", f"~({exp_lat},{exp_lng})")
    else:
        check(f"Map coords for {city}", False, "None", f"({exp_lat},{exp_lng})")

try:
    import folium
    m = folium.Map(location=[17.38, 78.48], zoom_start=12)
    folium.Marker([17.38, 78.48], popup="Test").add_to(m)
    check("Folium map creation OK", True)
except ImportError:
    check("Folium installed", False, "ImportError", "folium module")

# ─────────────────────────────────────────────────────────────
# 14. Feature 11: Voice Output (gTTS)
# ─────────────────────────────────────────────────────────────
print("\n[14] Feature 11 — Voice Output (gTTS)")
voice_text = a.get_voice_text(True, "Flood", sev_high, 9, loc_hyd, ["Medical","Rescue"],
                               ["Dispatch ambulance", "Deploy rescue team"])
check("Voice text is string",         isinstance(voice_text, str), type(voice_text), str)
check("Voice text > 20 chars",        len(voice_text) > 20, len(voice_text), ">20")
check("Voice text has disaster type", "Flood" in voice_text, voice_text[:60])
check("Voice text has severity",      "High"  in voice_text, voice_text[:60])
check("Voice text has location",      "Hyderabad" in voice_text, voice_text[:80])
check("Voice text has priority",      "9" in voice_text, voice_text[:80])
clean_voice = re.sub(r'[^\x00-\x7F]+', '', voice_text)
print(f"         Voice: {clean_voice[:100]}...")

try:
    from gtts import gTTS
    import io
    tts = gTTS(text="Disaster detected. Test alert.", lang='en', slow=False)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    audio_bytes = buf.read()
    check("gTTS generates audio bytes",  len(audio_bytes) > 500, len(audio_bytes), ">500 bytes")
except Exception as e:
    check("gTTS audio generation", False, str(e), "audio bytes")

# ─────────────────────────────────────────────────────────────
# 15. Auth System
# ─────────────────────────────────────────────────────────────
print("\n[15] Auth System — Login & Register")
import tempfile, os as _os

# Use a temp file so we don't pollute the real users_db
tmp = tempfile.mktemp(suffix=".json")
with open(tmp, "w") as f:
    json.dump([], f)

def _load(path):
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        table = data.get("_default", data)
        return list(table.values()) if isinstance(table, dict) else []
    return []

def _save(path, users):
    with open(path, "w") as f:
        json.dump(users, f)

def _register(db, u, p):
    users = _load(db)
    if any(x.get("username") == u for x in users):
        return False, "exists"
    users.append({"username": u, "password": p})
    _save(db, users)
    return True, "ok"

def _login(db, u, p):
    return any(x.get("username") == u and x.get("password") == p for x in _load(db))

ok1, _ = _register(tmp, "testuser", "pass123")
ok2, _ = _register(tmp, "testuser", "pass123")   # duplicate
check("Register new user",           ok1 == True,  ok1, True)
check("Reject duplicate username",   ok2 == False, ok2, False)
check("Login with correct creds",    _login(tmp, "testuser", "pass123"),  True,  True)
check("Reject wrong password",       not _login(tmp, "testuser", "wrong"), False, False)
check("Reject non-existent user",    not _login(tmp, "nobody",  "pass"),   False, False)
_os.unlink(tmp)

# ─────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────
print("\n" + "="*60)
passed = sum(1 for r in results if r[0] == PASS)
failed = sum(1 for r in results if r[0] == FAIL)
total  = len(results)
print(f"  RESULTS: {passed}/{total} passed  |  {failed} failed")
print("="*60)

if failed > 0:
    print("\n  Failed tests:")
    for r in results:
        if r[0] == FAIL:
            print(f"    - {r[1]}")

if failed == 0:
    print("\n  All features working correctly!")
print()
