"""
Disaster Helpline & Emergency Contact Database
Country and region-specific emergency numbers and support contacts
"""

from typing import Dict, List, Optional

class DisasterHelplineDatabase:
    """Manage emergency helplines and disaster support contacts"""
    
    # Comprehensive global emergency helpline database
    HELPLINES = {
        # Asia
        "India": {
            "country_code": "+91",
            "emergency": "112",
            "disaster_management": "1078",
            "earthquake": "1077",
            "fire": "101",
            "ambulance": "102",
            "police": "100",
            "contacts": [
                {"name": "National Disaster Management Authority (NDMA)", "phone": "+91-11-26701700", "website": "ndma.gov.in"},
                {"name": "Ministry of Home Affairs", "phone": "+91-11-23438010", "website": "mha.gov.in"}
            ]
        },
        "Bangladesh": {
            "country_code": "+880",
            "emergency": "999",
            "disaster_management": "1331",
            "fire": "999",
            "ambulance": "999",
            "police": "999",
            "contacts": [
                {"name": "Bangladesh Disaster Management Bureau", "phone": "+880-2-55006051", "website": "bdrcs.org"},
                {"name": "Red Crescent Society Bangladesh", "phone": "+880-2-9134633", "website": "bdrcs.org"}
            ]
        },
        "Pakistan": {
            "country_code": "+92",
            "emergency": "15",
            "disaster_management": "1700",
            "fire": "16",
            "ambulance": "115",
            "police": "15",
            "contacts": [
                {"name": "National Disaster Management Authority (NDMA)", "phone": "+92-51-9242801", "website": "ndma.gov.pk"},
                {"name": "Pakistan Red Crescent Society", "phone": "+92-51-2278981", "website": "prcs.org.pk"}
            ]
        },
        "Philippines": {
            "country_code": "+63",
            "emergency": "911",
            "disaster_management": "1",
            "fire": "160",
            "ambulance": "162",
            "police": "117",
            "contacts": [
                {"name": "National Disaster Risk Reduction & Management Council", "phone": "+63-2-83118222", "website": "ndrrmc.gov.ph"},
                {"name": "Philippine Red Cross", "phone": "+63-2-5255801", "website": "redcross.org.ph"}
            ]
        },
        "Thailand": {
            "country_code": "+66",
            "emergency": "1300",
            "disaster_management": "1300",
            "fire": "199",
            "ambulance": "1669",
            "police": "191",
            "contacts": [
                {"name": "Disaster Prevention & Mitigation Department", "phone": "+66-2-298-8333", "website": "dpm.go.th"},
                {"name": "Thai Red Cross", "phone": "+66-2-555-8051", "website": "redcross.or.th"}
            ]
        },
        "Indonesia": {
            "country_code": "+62",
            "emergency": "112",
            "disaster_management": "119",
            "earthquake": "119",
            "fire": "113",
            "ambulance": "118",
            "police": "110",
            "contacts": [
                {"name": "National Agency for Disaster Management (BNPB)", "phone": "+62-21-7863119", "website": "bnpb.go.id"},
                {"name": "Indonesian Red Cross (PMI)", "phone": "+62-21-7992325", "website": "pmi.or.id"}
            ]
        },
        "Japan": {
            "country_code": "+81",
            "emergency": "110",
            "disaster_management": "0120-221-357",
            "earthquake": "171",
            "fire": "119",
            "ambulance": "119",
            "police": "110",
            "contacts": [
                {"name": "Japan Meteorological Agency (JMA)", "phone": "+81-3-6735-0000", "website": "jma.go.jp"},
                {"name": "Japanese Red Cross", "phone": "+81-3-3437-7081", "website": "jrc.or.jp"}
            ]
        },
        "Nepal": {
            "country_code": "+977",
            "emergency": "100",
            "disaster_management": "1200",
            "fire": "101",
            "ambulance": "102",
            "police": "100",
            "contacts": [
                {"name": "Nepal Disaster Risk Reduction & Management Authority", "phone": "+977-1-4211445", "website": "ndrrma.gov.np"},
                {"name": "Nepal Red Cross Society", "phone": "+977-1-4413638", "website": "nrcs.org"}
            ]
        },
        
        # Middle East
        "Turkey": {
            "country_code": "+90",
            "emergency": "112",
            "disaster_management": "112",
            "earthquake": "184",
            "fire": "110",
            "ambulance": "112",
            "police": "155",
            "contacts": [
                {"name": "Disaster & Emergency Management Presidency (AFAD)", "phone": "+90-312-2032000", "website": "afad.gov.tr"},
                {"name": "Turkish Red Crescent", "phone": "+90-212-5274545", "website": "kizilay.org.tr"}
            ]
        },
        "Syria": {
            "country_code": "+963",
            "emergency": "113",
            "disaster_management": "113",
            "fire": "113",
            "ambulance": "160",
            "police": "112",
            "contacts": [
                {"name": "Syrian Arab Red Crescent", "phone": "+963-11-3318480", "website": "sarc.sy"}
            ]
        },
        
        # Africa
        "Kenya": {
            "country_code": "+254",
            "emergency": "999",
            "disaster_management": "0800-720-000",
            "fire": "999",
            "ambulance": "999",
            "police": "999",
            "contacts": [
                {"name": "Kenyan Red Cross Society", "phone": "+254-20-6999000", "website": "kenyaredcross.org"}
            ]
        },
        "Ethiopia": {
            "country_code": "+251",
            "emergency": "911",
            "disaster_management": "911",
            "fire": "911",
            "ambulance": "911",
            "police": "911",
            "contacts": [
                {"name": "Ethiopian Red Cross", "phone": "+251-11-412-3000", "website": "redcrescent.org.et"}
            ]
        },
        
        # Americas
        "United States": {
            "country_code": "+1",
            "emergency": "911",
            "disaster_management": "1-800-621-3362",
            "fire": "911",
            "ambulance": "911",
            "police": "911",
            "contacts": [
                {"name": "FEMA - Federal Emergency Management Agency", "phone": "1-202-646-2500", "website": "fema.gov"},
                {"name": "American Red Cross", "phone": "1-800-733-2767", "website": "redcross.org"},
                {"name": "USGS Earthquake Hazards", "phone": "1-888-ASK-USGS", "website": "usgs.gov"}
            ]
        },
        "Mexico": {
            "country_code": "+52",
            "emergency": "911",
            "disaster_management": "911",
            "fire": "068",
            "ambulance": "065",
            "police": "911",
            "contacts": [
                {"name": "Mexican Red Cross", "phone": "+52-55-5557-5757", "website": "cruzroja.org.mx"},
                {"name": "Civil Protection", "phone": "1-800-PROTECCION", "website": "proteccioncivil.gob.mx"}
            ]
        },
        "Chile": {
            "country_code": "+56",
            "emergency": "132",
            "disaster_management": "132",
            "earthquake": "130",
            "fire": "132",
            "ambulance": "131",
            "police": "133",
            "contacts": [
                {"name": "Chilean Red Cross", "phone": "+56-2-2690-6000", "website": "cruzroja.cl"}
            ]
        },
        "Brazil": {
            "country_code": "+55",
            "emergency": "192",
            "disaster_management": "199",
            "fire": "193",
            "ambulance": "192",
            "police": "190",
            "contacts": [
                {"name": "Brazilian Red Cross", "phone": "+55-11-3216-6500", "website": "redcross.org.br"}
            ]
        },
        
        # Europe
        "Italy": {
            "country_code": "+39",
            "emergency": "112",
            "disaster_management": "112",
            "fire": "115",
            "ambulance": "118",
            "police": "113",
            "contacts": [
                {"name": "Italian Red Cross", "phone": "+39-06-5510-1", "website": "cri.it"},
                {"name": "Civil Protection Department", "phone": "+39-06-6822-6822", "website": "protezionecivile.gov.it"}
            ]
        },
        "Greece": {
            "country_code": "+30",
            "emergency": "112",
            "disaster_management": "112",
            "fire": "199",
            "ambulance": "166",
            "police": "100",
            "contacts": [
                {"name": "Hellenic Red Cross", "phone": "+30-213-2012700", "website": "redcross.gr"}
            ]
        },
        
        # Oceania
        "Australia": {
            "country_code": "+61",
            "emergency": "000",
            "disaster_management": "1800-226-701",
            "fire": "000",
            "ambulance": "000",
            "police": "000",
            "contacts": [
                {"name": "Australian Red Cross", "phone": "1300-735-090", "website": "redcross.org.au"},
                {"name": "Emergency Management Australia", "phone": "+61-2-6272-7000", "website": "ema.gov.au"}
            ]
        },
        "New Zealand": {
            "country_code": "+64",
            "emergency": "111",
            "disaster_management": "111",
            "fire": "111",
            "ambulance": "111",
            "police": "111",
            "contacts": [
                {"name": "New Zealand Red Cross", "phone": "+64-4-570-0300", "website": "redcross.org.nz"},
                {"name": "National Emergency Management", "phone": "+64-2-4999-600", "website": "beready.nz"}
            ]
        }
    }
    
    # Global humanitarian organizations
    HUMANITARIAN_ORG = {
        "International Red Cross": {
            "phone": "+41-22-730-6001",
            "email": "resource@icrc.org",
            "website": "icrc.org"
        },
        "UNHCR (UN Refugees)": {
            "phone": "+41-22-739-8111",
            "email": "hqinfo@unhcr.org",
            "website": "unhcr.org"
        },
        "UNICEF": {
            "phone": "+1-212-326-7000",
            "website": "unicef.org"
        },
        "WHO (World Health Organization)": {
            "phone": "+41-22-791-2111",
            "website": "who.int"
        },
        "WFP (World Food Programme)": {
            "phone": "+39-06-6513-1",
            "website": "wfp.org"
        }
    }
    
    def get_helpline_for_country(self, country: str) -> Dict:
        """Get emergency helplines for a specific country"""
        country_title = country.title() if country else ""
        
        # Try exact match first
        if country_title in self.HELPLINES:
            return self._format_helpline(country_title, self.HELPLINES[country_title])
        
        # Try case-insensitive search
        for key in self.HELPLINES.keys():
            if key.lower() == country_title.lower():
                return self._format_helpline(key, self.HELPLINES[key])
        
        # Not found
        return {
            "status": "not_found",
            "country": country,
            "message": f"Helpline information for {country} not in database",
            "global_resources": self.HUMANITARIAN_ORG
        }
    
    def _format_helpline(self, country: str, helpline_data: Dict) -> Dict:
        """Format helpline data for display"""
        return {
            "status": "success",
            "country": country,
            "emergency": helpline_data.get("emergency", "Unknown"),
            "disaster_management": helpline_data.get("disaster_management", helpline_data.get("emergency")),
            "contacts": {
                "fire": helpline_data.get("fire", helpline_data.get("emergency")),
                "ambulance": helpline_data.get("ambulance", helpline_data.get("emergency")),
                "police": helpline_data.get("police", helpline_data.get("emergency"))
            },
            "organizations": helpline_data.get("contacts", []),
            "country_code": helpline_data.get("country_code", ""),
            "global_resources": [
                {
                    "name": "International Red Cross",
                    "phone": "+41-22-730-6001",
                    "website": "icrc.org"
                }
            ]
        }
    
    def get_nearest_resources(self, country: str, latitude: float = None, 
                            longitude: float = None) -> Dict:
        """Get nearest emergency resources and helplines"""
        helplines = self.get_helpline_for_country(country)
        
        resources = {
            "country": country,
            "helplines": helplines,
            "international_organizations": self.HUMANITARIAN_ORG,
            "resources": {
                "medical": "Contact local hospitals and ambulance services",
                "shelter": "Contact Red Cross/Red Crescent national society",
                "food": "Contact local government and WFP coordination center",
                "water": "Contact UNICEF and local water authority",
                "search_rescue": "Contact national disaster management authority"
            }
        }
        
        return resources
    
    def get_all_supported_countries(self) -> List[str]:
        """Get list of all supported countries"""
        return sorted(list(self.HELPLINES.keys()))
    
    def search_helpline(self, search_term: str) -> Dict:
        """Search for helpline by country name"""
        search_lower = search_term.lower()
        
        matches = []
        for country in self.HELPLINES.keys():
            if search_lower in country.lower():
                matches.append(self.get_helpline_for_country(country))
        
        return {
            "status": "success" if matches else "not_found",
            "search_term": search_term,
            "matches": matches,
            "count": len(matches)
        }
    
    def get_emergency_summary(self, country: str) -> str:
        """Get text summary of emergency contacts"""
        helpline = self.get_helpline_for_country(country)
        
        if helpline["status"] == "not_found":
            return f"Emergency helpline database not available for {country}. Contact international organizations."
        
        summary = f"""
EMERGENCY CONTACTS FOR {country.upper()}
{'='*50}

Primary Emergency Number: {helpline['emergency']}
Disaster Management: {helpline['disaster_management']}

Emergency Services:
- Fire: {helpline['contacts']['fire']}
- Ambulance: {helpline['ambulance']}
- Police: {helpline['contacts']['police']}

Organizations:
"""
        for org in helpline['organizations'][:3]:
            summary += f"- {org['name']}: {org['phone']}\n"
        
        return summary
