"""
Disaster Analysis & Severity Scoring
Analyzes disasters and generates priority scores
"""

from typing import Dict, List
import re

class DisasterAnalysisEngine:
    """Analyze and score disaster events"""
    
    # Disaster type keywords for classification
    DISASTER_KEYWORDS = {
        "flood": ["flood", "flooding", "inundation", "water", "river overflow"],
        "earthquake": ["earthquake", "seismic", "tremor", "quake"],
        "hurricane": ["hurricane", "typhoon", "cyclone", "tropical storm"],
        "fire": ["fire", "wildfire", "bushfire", "forest fire"],
        "drought": ["drought", "dry", "water scarcity"],
        "disease": ["epidemic", "pandemic", "disease", "outbreak"],
        "landslide": ["landslide", "mudslide", "avalanche"],
        "volcanic": ["volcanic", "volcano", "eruption", "lava"],
        "storm": ["storm", "tempest", "windstorm", "severe weather"],
        "tsunami": ["tsunami", "tidal wave"]
    }
    
    # Severity multipliers based on keywords
    SEVERITY_KEYWORDS = {
        "critical": 1.0,
        "severe": 0.9,
        "massive": 0.9,
        "catastrophic": 1.0,
        "widespread": 0.8,
        "major": 0.7,
        "significant": 0.6,
        "minor": 0.3
    }
    
    # Required help categories
    HELP_CATEGORIES = {
        "flood": ["Rescue Support", "Shelter Support", "Medical Support", "Water & Sanitation"],
        "earthquake": ["Search & Rescue", "Medical Support", "Shelter Support", "Infrastructure Repair"],
        "hurricane": ["Evacuation Support", "Shelter Support", "Medical Support", "Infrastructure Repair"],
        "fire": ["Evacuation Support", "Fire Fighting Equipment", "Medical Support", "Shelter Support"],
        "drought": ["Water Supply", "Food Support", "Medical Support", "Livelihood Support"],
        "disease": ["Medical Support", "Vaccination Support", "Quarantine Facilities", "Food Support"],
        "landslide": ["Search & Rescue", "Medical Support", "Shelter Support", "Infrastructure Repair"],
        "volcanic": ["Evacuation Support", "Medical Support", "Shelter Support", "Air Quality Monitoring"],
        "storm": ["Evacuation Support", "Shelter Support", "Medical Support", "Infrastructure Repair"],
        "tsunami": ["Evacuation Support", "Search & Rescue", "Medical Support", "Shelter Support"]
    }
    
    # Recommended actions by disaster type
    ACTIONS = {
        "flood": "Alert disaster response team, Dispatch rescue and medical teams, Set up emergency shelters",
        "earthquake": "Activate search and rescue teams immediately, Deploy medical teams, Assess structural damage",
        "hurricane": "Issue evacuation orders, Set up emergency shelters, Prepare emergency services",
        "fire": "Evacuate affected areas, Dispatch fire fighting units, Activate rescue teams",
        "drought": "Activate water distribution centers, Distribute emergency food supplies, Monitor health impacts",
        "disease": "Activate medical emergency protocols, Set up quarantine facilities, Begin vaccination campaign",
        "landslide": "Issue evacuation warnings, Deploy search and rescue teams, Provide medical support",
        "volcanic": "Issue evacuation alerts, Monitor volcanic activity, Activate emergency response",
        "storm": "Issue severe weather alerts, Activate emergency services, Set up shelters",
        "tsunami": "Issue tsunami warning, Evacuate coastal areas, Activate rescue operations"
    }
    
    def analyze_disaster_text(self, text: str, country: str = None, 
                             disaster_type_hint: str = None) -> Dict:
        """
        Analyze disaster text and generate comprehensive analysis
        
        Args:
            text: Disaster title/description
            country: Affected country
            disaster_type_hint: Hint about disaster type
            
        Returns:
            Dictionary with analysis results
        """
        text_lower = text.lower()
        
        # Detect disaster type
        detected_type = self._detect_disaster_type(text_lower, disaster_type_hint)
        
        # Calculate severity
        severity_score = self._calculate_severity(text_lower, detected_type)
        severity_level = self._score_to_level(severity_score)
        
        # Calculate priority
        priority_score = self._calculate_priority(text_lower, severity_score, country)
        
        # Get required help
        required_help = self._get_required_help(detected_type, severity_level)
        
        # Get recommended action
        recommended_action = self._get_recommended_action(detected_type)
        
        # Determine if disaster related
        is_disaster = detected_type != "unknown"
        
        return {
            "is_disaster_related": "YES" if is_disaster else "NO",
            "disaster_type": detected_type.upper(),
            "severity": severity_level,
            "severity_score": round(severity_score * 100),  # 0-100
            "priority_score": priority_score,  # 0-10
            "country": country or "Unknown",
            "required_help": required_help,
            "recommended_action": recommended_action,
            "analysis_text": text,
            "confidence": self._calculate_confidence(text_lower, detected_type)
        }
    
    def _detect_disaster_type(self, text: str, type_hint: str = None) -> str:
        """Detect disaster type from text"""
        # Use type hint if provided
        if type_hint:
            type_hint_lower = type_hint.lower()
            for dtype, keywords in self.DISASTER_KEYWORDS.items():
                if any(kw in type_hint_lower for kw in keywords):
                    return dtype
        
        # Detect from text
        for disaster_type, keywords in self.DISASTER_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    return disaster_type
        
        return "unknown"
    
    def _calculate_severity(self, text: str, disaster_type: str) -> float:
        """Calculate severity score (0.0 to 1.0)"""
        base_score = 0.5  # Base disaster severity
        
        # Add points for severity keywords
        severity_boost = 0.0
        for keyword, boost in self.SEVERITY_KEYWORDS.items():
            if keyword in text:
                severity_boost = max(severity_boost, boost - 0.5)
        
        # Numbers in text indicate scale
        numbers = re.findall(r'\d+', text)
        if numbers:
            max_num = max(int(n) for n in numbers)
            if max_num > 1000:
                severity_boost += 0.3
            elif max_num > 100:
                severity_boost += 0.2
        
        # Deaths/casualties
        if any(word in text for word in ["death", "dead", "casualty", "kill", "loss of life"]):
            severity_boost += 0.2
        
        # Affected populations
        if any(word in text for word in ["thousand", "million", "displaced", "homeless", "refugee"]):
            severity_boost += 0.2
        
        final_score = min(1.0, base_score + severity_boost)
        return final_score
    
    def _score_to_level(self, score: float) -> str:
        """Convert severity score to level"""
        if score >= 0.8:
            return "CRITICAL"
        elif score >= 0.6:
            return "HIGH"
        elif score >= 0.4:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _calculate_priority(self, text: str, severity: float, country: str = None) -> int:
        """Calculate priority score (0-10)"""
        # Start with severity-based score
        base_priority = round(severity * 7)  # 0-7 from severity
        
        # Bonus points for urgent keywords
        urgent_keywords = ["urgent", "immediate", "critical", "emergency", "alert", "now"]
        if any(kw in text for kw in urgent_keywords):
            base_priority += 2
        
        # Adjust for developed vs developing countries
        developing_countries = [
            "india", "bangladesh", "pakistan", "nepal", "haiti", "sudan", 
            "yemen", "syria", "myanmar", "phillipines", "indonesia", "thailand"
        ]
        if country and country.lower() in developing_countries:
            base_priority += 1
        
        return min(10, max(0, base_priority))
    
    def _get_required_help(self, disaster_type: str, severity: str) -> List[str]:
        """Get required help for disaster"""
        help_list = self.HELP_CATEGORIES.get(disaster_type, ["Emergency Response"])
        
        # Add more support for critical situations
        if severity == "CRITICAL":
            if "Medical Support" not in help_list:
                help_list.insert(0, "Medical Support")
            if "Rescue Support" not in help_list:
                help_list.insert(1, "Search & Rescue")
        
        return help_list[:3]  # Return top 3
    
    def _get_recommended_action(self, disaster_type: str) -> str:
        """Get recommended action for disaster"""
        return self.ACTIONS.get(disaster_type, "Activate emergency response protocols")
    
    def _calculate_confidence(self, text: str, detected_type: str) -> float:
        """Calculate confidence in analysis (0.0-1.0)"""
        if detected_type == "unknown":
            return 0.0
        
        # More keywords = higher confidence
        keywords = self.DISASTER_KEYWORDS.get(detected_type, [])
        count = sum(1 for kw in keywords if kw in text)
        
        confidence = min(1.0, (count * 0.3) + 0.5)
        return round(confidence, 2)
    
    def generate_emergency_summary(self, analysis: Dict) -> str:
        """Generate readable emergency summary"""
        summary = f"""
EMERGENCY ANALYSIS REPORT
{'='*50}

Disaster Related: {analysis['is_disaster_related']}
Disaster Type: {analysis['disaster_type']}
Severity Level: {analysis['severity']}
Priority Score: {analysis['priority_score']}/10
Country: {analysis['country']}

Required Help:
{chr(10).join(['  • ' + h for h in analysis['required_help']])}

Recommended Action:
  {analysis['recommended_action']}

Analysis Confidence: {analysis['confidence']:.0%}
{'='*50}
"""
        return summary
