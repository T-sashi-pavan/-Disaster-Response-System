"""
ReliefWeb API Integration Module
Fetches live disaster events from ReliefWeb API
"""

import requests
import json
from datetime import datetime
from typing import List, Dict, Optional
import time

class ReliefWebAPI:
    """Interface to ReliefWeb Disaster API"""
    
    BASE_URL = "https://api.reliefweb.int/v2/disasters"
    APP_NAME = "RescueMeAIProject"
    CACHE_DURATION = 60  # Cache for 60 seconds
    
    def __init__(self):
        self.last_fetch_time = 0
        self.cached_disasters = []
        self.last_error = None
    
    def fetch_disasters(self, limit: int = 20, force_refresh: bool = False) -> Dict:
        """
        Fetch latest disaster events from ReliefWeb API
        
        Args:
            limit: Number of disasters to fetch (default 20)
            force_refresh: Force fresh API call, skip cache
            
        Returns:
            Dictionary with disasters and metadata
        """
        # Check cache
        current_time = time.time()
        if (not force_refresh and 
            self.cached_disasters and 
            current_time - self.last_fetch_time < self.CACHE_DURATION):
            return {
                "status": "success",
                "source": "cache",
                "disasters": self.cached_disasters,
                "count": len(self.cached_disasters),
                "last_updated": datetime.fromtimestamp(self.last_fetch_time).isoformat(),
                "cached": True
            }
        
        try:
            # Build API URL
            params = {
                "appname": self.APP_NAME,
                "limit": limit,
                "preset": "latest"
            }
            
            # Enhanced headers for better API compatibility
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 RescueMeAIProject/1.0",
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate"
            }
            
            response = requests.get(
                self.BASE_URL, 
                params=params, 
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Parse disasters
            disasters = self._parse_disasters(data)
            
            # Update cache
            self.cached_disasters = disasters
            self.last_fetch_time = current_time
            self.last_error = None
            
            return {
                "status": "success",
                "source": "api",
                "disasters": disasters,
                "count": len(disasters),
                "last_updated": datetime.now().isoformat(),
                "cached": False,
                "raw_response": data
            }
            
        except requests.exceptions.Timeout:
            self.last_error = "API request timed out. Please try again."
            return self._error_response("API request timed out. Please try again.")
        
        except requests.exceptions.ConnectionError:
            self.last_error = "Unable to connect to ReliefWeb API."
            return self._error_response("Unable to connect to ReliefWeb API.")
        
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 403:
                self.last_error = "ReliefWeb API access denied. Using sample data."
                return self._get_sample_disasters()
            self.last_error = f"API Error: {status_code}"
            return self._error_response(f"API Error: {status_code}")
        
        except Exception as e:
            self.last_error = f"Error fetching disasters: {str(e)}"
            return self._error_response(f"Unexpected error: {str(e)}")
    
    def _parse_disasters(self, api_response: Dict) -> List[Dict]:
        """Parse ReliefWeb API response into disaster list"""
        disasters = []
        
        try:
            if "data" not in api_response:
                return disasters
            
            for item in api_response.get("data", []):
                fields = item.get("fields", {})
                
                disaster = {
                    "id": item.get("id"),
                    "title": fields.get("name", "Unknown Disaster"),
                    "type": self._get_disaster_type(fields),
                    "country": self._get_country(fields),
                    "status": fields.get("status", "Unknown"),
                    "date": fields.get("date", {}).get("original", "Unknown"),
                    "url": fields.get("url", ""),
                    "glide": fields.get("glide", ""),
                    "description": fields.get("description", ""),
                    "severity": self._estimate_severity(fields),
                    "affected_countries": self._get_affected_countries(fields)
                }
                
                disasters.append(disaster)
        
        except Exception as e:
            print(f"Error parsing disasters: {str(e)}")
        
        return disasters
    
    def _get_disaster_type(self, fields: Dict) -> str:
        """Extract disaster type"""
        types = fields.get("type", [])
        if types and isinstance(types, list) and len(types) > 0:
            return types[0].get("name", "Unknown")
        return "Unknown"
    
    def _get_country(self, fields: Dict) -> str:
        """Extract primary country"""
        countries = fields.get("country", [])
        if countries and isinstance(countries, list) and len(countries) > 0:
            return countries[0].get("name", "Unknown")
        return "Unknown"
    
    def _get_affected_countries(self, fields: Dict) -> List[str]:
        """Extract all affected countries"""
        countries = []
        for country in fields.get("country", []):
            if isinstance(country, dict) and "name" in country:
                countries.append(country["name"])
        return countries
    
    def _estimate_severity(self, fields: Dict) -> str:
        """Estimate severity based on available data"""
        status = fields.get("status", "").lower()
        
        # Map status to severity
        if "active" in status or "ongoing" in status:
            return "HIGH"
        elif "past" in status or "alert" in status:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _error_response(self, error_message: str) -> Dict:
        """Return error response format"""
        return {
            "status": "error",
            "error": error_message,
            "disasters": self.cached_disasters,  # Return cached data if available
            "count": len(self.cached_disasters),
            "cached": True,
            "source": "cache"
        }
    
    def _get_sample_disasters(self) -> Dict:
        """Return sample disaster data for demonstration/testing"""
        sample_disasters = [
            {
                "id": 1001,
                "title": "Severe Flooding in Pakistan",
                "type": "Flood",
                "country": "Pakistan",
                "status": "active",
                "date": "2024-01-15",
                "url": "https://reliefweb.int/disaster/1001",
                "glide": "FL-2024-000001",
                "description": "Heavy monsoon rains causing severe flooding across multiple provinces",
                "severity": "HIGH",
                "affected_countries": ["Pakistan"]
            },
            {
                "id": 1002,
                "title": "Earthquake Emergency in Chile",
                "type": "Earthquake",
                "country": "Chile",
                "status": "active",
                "date": "2024-01-14",
                "url": "https://reliefweb.int/disaster/1002",
                "glide": "EQ-2024-000002",
                "description": "Major earthquake with magnitude 7.2 affecting Santiago region",
                "severity": "CRITICAL",
                "affected_countries": ["Chile"]
            },
            {
                "id": 1003,
                "title": "Drought Crisis in East Africa",
                "type": "Drought",
                "country": "Kenya",
                "status": "active",
                "date": "2024-01-10",
                "url": "https://reliefweb.int/disaster/1003",
                "glide": "DR-2024-000003",
                "description": "Prolonged drought affecting millions across Kenya, Ethiopia, and Somalia",
                "severity": "HIGH",
                "affected_countries": ["Kenya", "Ethiopia", "Somalia"]
            },
            {
                "id": 1004,
                "title": "Tropical Storm in Philippines",
                "type": "Storm",
                "country": "Philippines",
                "status": "active",
                "date": "2024-01-12",
                "url": "https://reliefweb.int/disaster/1004",
                "glide": "ST-2024-000004",
                "description": "Powerful tropical storm with torrential rainfall and strong winds",
                "severity": "MEDIUM",
                "affected_countries": ["Philippines"]
            },
            {
                "id": 1005,
                "title": "Wildfire in Australia",
                "type": "Fire",
                "country": "Australia",
                "status": "active",
                "date": "2024-01-11",
                "url": "https://reliefweb.int/disaster/1005",
                "glide": "FI-2024-000005",
                "description": "Severe bushfires affecting multiple regions with significant property damage",
                "severity": "HIGH",
                "affected_countries": ["Australia"]
            }
        ]
        
        # Update cache with sample data
        self.cached_disasters = sample_disasters
        self.last_fetch_time = time.time()
        
        return {
            "status": "success",
            "source": "sample",
            "disasters": sample_disasters,
            "count": len(sample_disasters),
            "last_updated": datetime.now().isoformat(),
            "cached": False,
            "note": "Using sample data for demonstration"
        }
    
    def get_disaster_by_id(self, disaster_id: int) -> Optional[Dict]:
        """Get specific disaster by ID from cache"""
        for disaster in self.cached_disasters:
            if disaster.get("id") == disaster_id:
                return disaster
        return None
    
    def search_disasters(self, query: str) -> List[Dict]:
        """Search disasters by title"""
        results = []
        query_lower = query.lower()
        
        for disaster in self.cached_disasters:
            title = disaster.get("title", "").lower()
            country = disaster.get("country", "").lower()
            disaster_type = disaster.get("type", "").lower()
            
            if (query_lower in title or 
                query_lower in country or 
                query_lower in disaster_type):
                results.append(disaster)
        
        return results
    
    def get_statistics(self) -> Dict:
        """Get statistics from cached disasters"""
        if not self.cached_disasters:
            return {
                "total_events": 0,
                "high_priority": 0,
                "most_common_type": "N/A",
                "affected_countries": []
            }
        
        # Count by type
        type_counts = {}
        for disaster in self.cached_disasters:
            dtype = disaster.get("type", "Other")
            type_counts[dtype] = type_counts.get(dtype, 0) + 1
        
        # Count high priority
        high_priority = len([d for d in self.cached_disasters 
                            if d.get("severity") == "HIGH"])
        
        # Get affected countries
        all_countries = set()
        for disaster in self.cached_disasters:
            for country in disaster.get("affected_countries", []):
                all_countries.add(country)
        
        # Most common type
        most_common = max(type_counts, key=type_counts.get) if type_counts else "N/A"
        
        return {
            "total_events": len(self.cached_disasters),
            "high_priority": high_priority,
            "most_common_type": most_common,
            "affected_countries": sorted(list(all_countries)),
            "disaster_types": type_counts,
            "last_updated": datetime.fromtimestamp(self.last_fetch_time).isoformat() if self.last_fetch_time else "Never"
        }
