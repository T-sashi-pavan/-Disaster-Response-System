"""
disaster_analyzer.py
Core engine for Advanced Disaster Management AI System.
Handles: Detection, Type, Needs, Severity, Priority, Location, Actions, Auto-Response, Voice
"""

import re
import os
import tempfile
import spacy
from fuzzywuzzy import process, fuzz


class DisasterAnalyzer:
    def __init__(self):
        # Load Spacy for NER (Multiple location detection)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception:
            self.nlp = None

        # ── Indian + World Cities (name → (lat, lng)) ─────────────────────────
    CITIES = {
        'mumbai': (19.0760, 72.8777), 'delhi': (28.6139, 77.2090),
        'bangalore': (12.9716, 77.5946), 'bengaluru': (12.9716, 77.5946),
        'hyderabad': (17.3850, 78.4867), 'chennai': (13.0827, 80.2707),
        'kolkata': (22.5726, 88.3639), 'pune': (18.5204, 73.8567),
        'ahmedabad': (23.0225, 72.5714), 'jaipur': (26.9124, 75.7873),
        'surat': (21.1702, 72.8311), 'lucknow': (26.8467, 80.9462),
        'kanpur': (26.4499, 80.3319), 'nagpur': (21.1458, 79.0882),
        'indore': (22.7196, 75.8577), 'thane': (19.2183, 72.9781),
        'bhopal': (23.2599, 77.4126), 'visakhapatnam': (17.6868, 83.2185),
        'vizag': (17.6868, 83.2185), 'patna': (25.5941, 85.1376),
        'vadodara': (22.3072, 73.1812), 'ghaziabad': (28.6692, 77.4538),
        'ludhiana': (30.9010, 75.8573), 'agra': (27.1767, 78.0081),
        'nashik': (19.9975, 73.7898), 'faridabad': (28.4082, 77.3178),
        'meerut': (28.9845, 77.7064), 'rajkot': (22.3039, 70.8022),
        'varanasi': (25.3176, 82.9739), 'srinagar': (34.0837, 74.7973),
        'aurangabad': (19.8762, 75.3433), 'amritsar': (31.6340, 74.8723),
        'allahabad': (25.4358, 81.8463), 'prayagraj': (25.4358, 81.8463),
        'ranchi': (23.3441, 85.3096), 'howrah': (22.5958, 88.2636),
        'coimbatore': (11.0168, 76.9558), 'jabalpur': (23.1815, 79.9864),
        'gwalior': (26.2183, 78.1828), 'vijayawada': (16.5062, 80.6480),
        'jodhpur': (26.2389, 73.0243), 'madurai': (9.9252, 78.1198),
        'raipur': (21.2514, 81.6296), 'kota': (25.2138, 75.8648),
        'chandigarh': (30.7333, 76.7794), 'guwahati': (26.1445, 91.7362),
        'solapur': (17.6805, 75.9064), 'mysuru': (12.2958, 76.6394),
        'mysore': (12.2958, 76.6394), 'tiruchirappalli': (10.7905, 78.7047),
        'bareilly': (28.3670, 79.4304), 'tiruppur': (11.1085, 77.4411),
        'gurgaon': (28.4595, 77.0266), 'gurugram': (28.4595, 77.0266),
        'noida': (28.5355, 77.3910), 'dehradun': (30.3165, 78.0322),
        'shimla': (31.1048, 77.1734), 'jamshedpur': (22.8046, 86.2029),
        'bhubaneswar': (20.2961, 85.8245), 'kochi': (9.9312, 76.2673),
        'cochin': (9.9312, 76.2673), 'mangalore': (12.9141, 74.8560),
        'nellore': (14.4426, 79.9865), 'warangal': (17.9784, 79.5941),
        'gorakhpur': (26.7606, 83.3732), 'bikaner': (28.0229, 73.3119),
        'kolhapur': (16.7050, 74.2433), 'latur': (18.4088, 76.5604),
        'haridwar': (29.9457, 78.1642), 'rishikesh': (30.0869, 78.2676),
        'panaji': (15.4909, 73.8278), 'goa': (15.2993, 74.1240),
        'jammu': (32.7266, 74.8570), 'imphal': (24.8170, 93.9368),
        'shillong': (25.5788, 91.8933), 'gangtok': (27.3389, 88.6065),
        'itanagar': (27.0844, 93.6053), 'aizawl': (23.7307, 92.7173),
        'kohima': (25.6701, 94.1077), 'agartala': (23.8315, 91.2868),
        'puri': (19.8135, 85.8312), 'kedarnath': (30.7346, 79.0669),
        'uttarkashi': (30.7268, 78.4354), 'tehri': (30.3784, 78.4806),
        'kathmandu': (27.7172, 85.3240), 'dhaka': (23.8103, 90.4125),
        'islamabad': (33.6844, 73.0479), 'karachi': (24.8607, 67.0011),
        'colombo': (6.9271, 79.8612), 'new york': (40.7128, -74.0060),
        'london': (51.5074, -0.1278), 'tokyo': (35.6762, 139.6503),
        'paris': (48.8566, 2.3522), 'sydney': (-33.8688, 151.2093),
        'dubai': (25.2048, 55.2708), 'singapore': (1.3521, 103.8198),
        'bangkok': (13.7563, 100.5018),
    }

    # ── Disaster Type Keywords ────────────────────────────────────────────
    DISASTER_KEYWORDS = {
        'Flood':      ['flood', 'flooding', 'inundated', 'waterlogged', 'overflow',
                       'dam burst', 'water level', 'submerged', 'deluge', 'water rising'],
        'Fire':       ['fire', 'blaze', 'burning', 'smoke', 'flames', 'wildfire',
                       'inferno', 'arson', 'burnt', 'firefighter', 'ablaze'],
        'Earthquake': ['earthquake', 'quake', 'tremor', 'seismic', 'aftershock',
                       'magnitude', 'richter', 'epicenter', 'ground shaking', 'shaking'],
        'Cyclone':    ['cyclone', 'storm', 'hurricane', 'typhoon', 'tornado',
                       'gale', 'wind speed', 'landfall', 'tropical storm'],
        'Accident':   ['accident', 'crash', 'collision', 'explosion', 'blast',
                       'collapse', 'landslide', 'stampede', 'derailment'],
    }

    # ML label → disaster type
    LABEL_TO_TYPE = {
        'floods': 'Flood', 'storm': 'Cyclone', 'fire': 'Fire',
        'earthquake': 'Earthquake', 'cold': 'Cyclone',
        'weather_related': 'Cyclone', 'transport': 'Accident',
        'buildings': 'Accident', 'infrastructure_related': 'Accident',
    }

    # ML label → need buckets
    MEDICAL_LABELS  = {'medical_help', 'medical_products', 'hospitals', 'death'}
    SHELTER_LABELS  = {'shelter', 'refugees', 'cold'}
    FOOD_LABELS     = {'food', 'water', 'clothing', 'money'}
    RESCUE_LABELS   = {'search_and_rescue', 'missing_people', 'security', 'military'}

    # Severity keyword lists
    HIGH_KW   = ['trapped', 'critical', 'injured', 'collapsed', 'dead', 'death',
                 'casualty', 'fatal', 'drowning', 'buried', 'missing', 'explosion',
                 'sos', 'mayday', 'dying', 'bodies', 'help us', 'severe', 'panic']
    MEDIUM_KW = ['help needed', 'road blocked', 'damage', 'stranded', 'evacuate',
                 'rescue needed', 'shelter needed', 'displaced', 'need help',
                 'danger', 'affected', 'power cut', 'blocked', 'unsafe']
    LOW_KW    = ['warning', 'awareness', 'alert', 'watch', 'advisory', 'precaution',
                 'possible', 'expected', 'prepare', 'caution', 'forecast']

    # Recommended actions lookup
    ACTIONS = {
        'Medical': {
            'High':   ['🚑 Dispatch ambulance immediately',
                       '🏥 Alert nearest hospitals on emergency standby',
                       '💊 Deploy mobile medical response unit'],
            'Medium': ['🏥 Notify medical facilities in the area',
                       '💊 Send first-aid team'],
            'Low':    ['📋 Monitor health situation', '💊 Prepare first-aid kits'],
        },
        'Rescue': {
            'High':   ['🚁 Deploy helicopter rescue team immediately',
                       '🚒 Dispatch NDRF/SDRF rescue squad',
                       '🔦 Activate full-scale search operations'],
            'Medium': ['🚒 Send local rescue team', '🔦 Coordinate search parties'],
            'Low':    ['📡 Alert rescue teams on standby'],
        },
        'Shelter': {
            'High':   ['🏠 Open emergency shelters immediately',
                       '🚌 Arrange mass evacuation transport'],
            'Medium': ['🏠 Prepare relief camps', '🚌 Organize evacuation routes'],
            'Low':    ['📋 Identify shelter locations nearby'],
        },
        'Food': {
            'High':   ['🍱 Deploy emergency food distribution NOW',
                       '🚚 Dispatch water tankers immediately'],
            'Medium': ['🍱 Coordinate food relief with NGOs',
                       '🚚 Arrange clean water supply'],
            'Low':    ['📦 Stock relief supplies', '🍱 Notify NGOs for support'],
        },
    }

    # ── Public API ────────────────────────────────────────────────────────

    def detect_disaster(self, predictions: dict, text: str = "") -> bool:
        """Returns True if message is disaster-related."""
        tl = text.lower()
        # Check ML Predictions first
        if predictions.get('related', 0) == 1:
            return True

        # Fuzzy Check for Disaster Type Keywords
        for dtype, kws in self.DISASTER_KEYWORDS.items():
            for kw in kws:
                if fuzz.partial_ratio(kw, tl) > 90:
                    return True

        # Fuzzy Check for High Severity Keywords if ML missed it
        if any(fuzz.partial_ratio(kw, tl) > 90 for kw in self.HIGH_KW):
            return True

        # Check key labels
        key_labels = (self.MEDICAL_LABELS | self.SHELTER_LABELS |
                      self.FOOD_LABELS | self.RESCUE_LABELS |
                      {'floods', 'fire', 'earthquake', 'storm', 'death',
                       'missing_people', 'security', 'transport', 'buildings'})
        return any(predictions.get(l, 0) == 1 for l in key_labels)

    def get_disaster_type(self, predictions: dict, text: str) -> str:
        """Determine disaster type: ML labels first, then fuzzy keyword matching."""
        # 1. ML prediction priority
        for label, dtype in self.LABEL_TO_TYPE.items():
            if predictions.get(label, 0) == 1:
                return dtype

        # 2. Fuzzy Keyword matching (handles misspellings like 'eartquake')
        tl = text.lower()
        type_scores = {}
        for dtype, kws in self.DISASTER_KEYWORDS.items():
            # Find the best fuzzy match for any keyword in this category
            best_match_score = 0
            for kw in kws:
                score = fuzz.partial_ratio(kw, tl)
                if score > best_match_score:
                    best_match_score = score
            type_scores[dtype] = best_match_score

        best_type = max(type_scores, key=type_scores.get)
        if type_scores[best_type] > 80:  # Threshold for fuzzy match
            return best_type

        return 'General Emergency'

    def get_needs(self, predictions: dict, text: str = '') -> list:
        """Map ML predictions → [Medical, Shelter, Food, Rescue]."""
        tl = text.lower()
        needs = []
        med_kw  = ['medical', 'doctor', 'hospital', 'injured', 'hurt', 'medicine', 'wound']
        shel_kw = ['shelter', 'homeless', 'evacuate', 'displaced', 'house', 'roof']
        food_kw = ['food', 'water', 'hungry', 'starving', 'drink', 'eat', 'thirsty']
        resc_kw = ['rescue', 'trapped', 'missing', 'search', 'stranded', 'buried']

        if any(predictions.get(l, 0) == 1 for l in self.MEDICAL_LABELS) or \
                any(kw in tl for kw in med_kw):
            needs.append('Medical')
        if any(predictions.get(l, 0) == 1 for l in self.SHELTER_LABELS) or \
                any(kw in tl for kw in shel_kw):
            needs.append('Shelter')
        if any(predictions.get(l, 0) == 1 for l in self.FOOD_LABELS) or \
                any(kw in tl for kw in food_kw):
            needs.append('Food')
        if any(predictions.get(l, 0) == 1 for l in self.RESCUE_LABELS) or \
                any(kw in tl for kw in resc_kw):
            needs.append('Rescue')
        return needs

    def get_severity(self, text: str) -> dict:
        """Keyword-based severity → {level, score, matched_keywords}."""
        tl = text.lower()
        high_hits   = [kw for kw in self.HIGH_KW   if kw in tl]
        medium_hits = [kw for kw in self.MEDIUM_KW if kw in tl]
        low_hits    = [kw for kw in self.LOW_KW    if kw in tl]

        if high_hits:
            level = 'High'
            score = min(85 + len(high_hits) * 3, 100)
        elif medium_hits:
            level = 'Medium'
            score = min(45 + len(medium_hits) * 5, 80)
        elif low_hits:
            level = 'Low'
            score = min(15 + len(low_hits) * 5, 40)
        else:
            level = 'Low'
            score = 10

        return {
            'level': level,
            'score': score,
            'matched': high_hits + medium_hits + low_hits,
        }

    def get_priority_score(self, severity: dict, needs: list, disaster_type: str) -> int:
        """Compute priority 1–10."""
        base  = {'High': 7, 'Medium': 4, 'Low': 2}.get(severity['level'], 2)
        needs_bonus = min(len(needs) * 0.75, 2.0)
        type_bonus  = {'Earthquake': 1.5, 'Flood': 1.2, 'Cyclone': 1.2,
                       'Fire': 1.0, 'Accident': 0.8}.get(disaster_type, 0.5)
        return min(int(round(base + needs_bonus + type_bonus)), 10)

    def extract_location(self, text: str) -> list:
        """Returns list of (display_name, lat, lng)."""
        found_locations = []
        tl = text.lower()

        # 1. Spacy NER (Find all entities)
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ in ["GPE", "LOC", "FAC"]:
                    name = ent.text
                    nl = name.lower()
                    # Check if we have exact coords
                    if nl in self.CITIES:
                        found_locations.append((name, self.CITIES[nl][0], self.CITIES[nl][1]))
                    else:
                        # Try fuzzy match with our city list
                        best_city, score = process.extractOne(nl, self.CITIES.keys())
                        if score > 90:
                            found_locations.append((best_city.title(), self.CITIES[best_city][0], self.CITIES[best_city][1]))
                        else:
                            found_locations.append((name, None, None))

        # 2. Fallback to Regex for specific "in <Place>" patterns if Spacy missed it
        if not found_locations:
            matches = re.finditer(
                r'\b(?:in|at|near|from|around)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)?)',
                text, re.IGNORECASE
            )
            for m in matches:
                place = m.group(1)
                pl = place.lower()
                if pl in self.CITIES:
                    found_locations.append((place, self.CITIES[pl][0], self.CITIES[pl][1]))
                else:
                    found_locations.append((place, None, None))

        # 3. Always check our core city list even without Spacy/Regex
        for city, coords in self.CITIES.items():
            if r'\b' + city + r'\b' in tl:
                if not any(city.lower() == loc[0].lower() for loc in found_locations):
                    found_locations.append((city.title(), coords[0], coords[1]))

        # Remove duplicates
        seen = set()
        unique_locs = []
        for loc in found_locations:
            if loc[0].lower() not in seen:
                unique_locs.append(loc)
                seen.add(loc[0].lower())

        return unique_locs if unique_locs else None

    def get_recommended_actions(self, needs: list, severity: dict, disaster_type: str) -> list:
        """Generate action list from needs × severity."""
        actions = []
        sev = severity['level']
        for need in needs:
            acts = self.ACTIONS.get(need, {}).get(sev, [])
            actions.extend(acts)
        # General actions based on disaster type
        general = {
            'Flood':      '🌊 Issue flood evacuation orders',
            'Fire':       '🔥 Contain fire perimeter immediately',
            'Earthquake': '🏗️ Inspect structural damage of buildings',
            'Cyclone':    '🌀 Secure coastlines and evacuate low-lying areas',
            'Accident':   '🚧 Secure the scene and control traffic',
        }
        if disaster_type in general:
            actions.append(general[disaster_type])
        if not actions:
            actions.append('📡 Monitor situation and remain on standby')
        return list(dict.fromkeys(actions))  # deduplicate preserving order

    def get_auto_response(self, detected: bool, dtype: str,
                          severity: dict, location, needs: list) -> str:
        """Generate a formatted emergency response summary."""
        if not detected:
            return "✅ No emergency detected. Message appears to be non-disaster related."

        loc_str = f" in {location[0]}" if location else ""
        needs_str = ', '.join(needs) if needs else 'general assistance'
        sev = severity['level'].upper()

        templates = {
            'High':   f"🚨 CRITICAL EMERGENCY detected{loc_str}! "
                      f"Situation involves {dtype.lower()} with {sev} severity. "
                      f"Immediate {needs_str} support required. "
                      f"Deploy all available emergency resources NOW.",
            'Medium': f"⚠️ Emergency alert{loc_str}: {dtype} event with MEDIUM severity detected. "
                      f"Resources required: {needs_str}. "
                      f"Coordinate response teams and prepare relief operations.",
            'Low':    f"ℹ️ Low-level alert{loc_str}: {dtype} advisory issued. "
                      f"Monitor situation and prepare {needs_str} resources as precaution.",
        }
        return templates.get(severity['level'],
                             f"Emergency detected{loc_str}. Immediate assistance required.")

    def get_voice_text(self, detected: bool, dtype: str, severity: dict,
                       priority: int, location, needs: list, actions: list) -> str:
        """Plain text for TTS (no emojis)."""
        if not detected:
            return "No disaster detected. The message appears to be non-emergency."
        loc_str = f"in {location[0]}" if location else "location unknown"
        needs_str = ', '.join(needs) if needs else 'general help'
        acts_str  = '. '.join(a.split(' ', 1)[-1] for a in actions[:3])
        return (
            f"Disaster detected. Type: {dtype}. Location: {loc_str}. "
            f"Severity: {severity['level']}. Priority score: {priority} out of 10. "
            f"Required help: {needs_str}. "
            f"Recommended actions: {acts_str}."
        )

    def generate_voice_audio(self, voice_text: str):
        """Generate MP3 bytes using gTTS. Returns bytes or None on failure."""
        try:
            from gtts import gTTS
            import io
            tts = gTTS(text=voice_text, lang='en', slow=False)
            buf = io.BytesIO()
            tts.write_to_fp(buf)
            buf.seek(0)
            return buf.read()
        except Exception:
            return None
