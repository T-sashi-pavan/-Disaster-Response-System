"""
Interactive Map Visualization for Disasters
Using Folium and Streamlit to display disaster locations on map
"""

import folium
from folium import plugins
import streamlit as st
from streamlit_folium import st_folium
from typing import Dict, List, Optional
import json

class DisasterMap:
    """Create interactive disaster maps"""
    
    # Color mapping for severity
    SEVERITY_COLORS = {
        "CRITICAL": "#dc2626",  # Red
        "HIGH": "#f59e0b",       # Orange
        "MEDIUM": "#3b82f6",     # Blue
        "LOW": "#10b981"         # Green
    }
    
    # Icon mapping for disaster types
    DISASTER_ICONS = {
        "Earthquake": "⛈️",
        "Flood": "🌊",
        "Fire": "🔥",
        "Cyclone": "🌪️",
        "Storm": "⛈️",
        "Volcano": "🌋",
        "Drought": "🌵",
        "Tsunami": "🌊",
        "Wildfire": "🔥",
        "Landslide": "⛏️"
    }
    
    def __init__(self, center_lat: float = 20, center_lon: float = 0, zoom_start: int = 2):
        """Initialize map"""
        self.center_lat = center_lat
        self.center_lon = center_lon
        self.zoom_start = zoom_start
    
    def create_disaster_map(self, disasters: List[Dict], title: str = "Global Disasters") -> folium.Map:
        """
        Create interactive map with disaster markers
        
        Args:
            disasters: List of disaster dictionaries with lat/lon
            title: Map title
            
        Returns:
            Folium map object
        """
        # Create base map
        disaster_map = folium.Map(
            location=[self.center_lat, self.center_lon],
            zoom_start=self.zoom_start,
            tiles="OpenStreetMap"
        )
        
        # Add title
        title_html = f"""
        <div style="position: fixed; 
                top: 10px; left: 50px; width: 300px; height: 60px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:16px; font-weight: bold; padding: 10px;
                border-radius: 5px; box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">
            {title}
        </div>
        """
        disaster_map.get_root().html.add_child(folium.Element(title_html))
        
        # Add disaster markers
        for disaster in disasters:
            lat = disaster.get("latitude")
            lon = disaster.get("longitude")
            
            # Skip if no coordinates
            if lat is None or lon is None:
                continue
            
            # Get marker color based on severity
            severity = disaster.get("severity", "MEDIUM")
            color = self.SEVERITY_COLORS.get(severity, "#3b82f6")
            
            # Create popup content
            popup_html = self._create_popup(disaster)
            
            # Add marker to map
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=400),
                tooltip=disaster.get("title", "Disaster Event"),
                icon=folium.Icon(
                    color=self._hex_to_color(color),
                    icon="exclamation-triangle",
                    prefix="fa"
                )
            ).add_to(disaster_map)
        
        # Add heatmap layer for density visualization
        if len(disasters) > 1:
            heat_data = []
            for disaster in disasters:
                lat = disaster.get("latitude")
                lon = disaster.get("longitude")
                if lat and lon:
                    # Higher intensity for critical disasters
                    intensity = 1.0 if disaster.get("severity") == "CRITICAL" else 0.5
                    heat_data.append([lat, lon, intensity])
            
            if heat_data:
                plugins.HeatMap(heat_data, name="Disaster Density").add_to(disaster_map)
        
        # Add layer control
        folium.LayerControl().add_to(disaster_map)
        
        # Add fullscreen button
        plugins.Fullscreen(position='topright').add_to(disaster_map)
        
        # Add coordinates display on click
        disaster_map.add_child(folium.LatLngPopup())
        
        return disaster_map
    
    def _create_popup(self, disaster: Dict) -> str:
        """Create HTML popup for marker"""
        severity_color = self.SEVERITY_COLORS.get(disaster.get("severity", "MEDIUM"), "#3b82f6")
        
        html = f"""
        <div style="font-family: Arial; width: 350px;">
            <h3 style="color: {severity_color}; margin-top: 0;">
                {disaster.get('title', 'Disaster Event')}
            </h3>
            
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="font-weight: bold; width: 120px;">Type:</td>
                    <td>{disaster.get('type', 'Unknown')}</td>
                </tr>
                <tr style="background-color: #f0f0f0;">
                    <td style="font-weight: bold;">Country:</td>
                    <td>{disaster.get('country', 'Unknown')}</td>
                </tr>
                <tr>
                    <td style="font-weight: bold;">Severity:</td>
                    <td><span style="background-color: {severity_color}; 
                    color: white; padding: 4px 8px; border-radius: 4px;">
                    {disaster.get('severity', 'Unknown')}</span></td>
                </tr>
                <tr style="background-color: #f0f0f0;">
                    <td style="font-weight: bold;">Date:</td>
                    <td>{disaster.get('date', 'Unknown')}</td>
                </tr>
                <tr>
                    <td style="font-weight: bold;">Status:</td>
                    <td>{disaster.get('status', 'Unknown')}</td>
                </tr>
                <tr style="background-color: #f0f0f0;">
                    <td style="font-weight: bold;">Source:</td>
                    <td>{disaster.get('source', 'Unknown')}</td>
                </tr>
            </table>
            
            <p style="margin-top: 10px; font-size: 12px; color: #666;">
                {disaster.get('description', 'No additional information')}
            </p>
            
            <div style="margin-top: 10px; padding: 8px; background-color: #f0f0f0; 
            border-left: 3px solid {severity_color}; border-radius: 3px;">
                <strong>Coordinates:</strong><br>
                Lat: {disaster.get('latitude', 'N/A'):.4f}<br>
                Lon: {disaster.get('longitude', 'N/A'):.4f}
            </div>
        </div>
        """
        
        return html
    
    def _hex_to_color(self, hex_color: str) -> str:
        """Convert hex color to folium color name"""
        color_map = {
            "#dc2626": "red",
            "#f59e0b": "orange",
            "#3b82f6": "blue",
            "#10b981": "green"
        }
        return color_map.get(hex_color, "blue")
    
    def create_country_focus_map(self, country: str, disasters: List[Dict]) -> folium.Map:
        """
        Create zoomed map for specific country
        
        Args:
            country: Country name
            disasters: List of disasters in that country
            
        Returns:
            Folium map focused on country
        """
        # Country center coordinates (simplified)
        country_centers = {
            "India": (20, 78),
            "Turkey": (39, 35),
            "Mexico": (23, -102),
            "Philippines": (12, 122),
            "Indonesia": (-2, 113),
            "Japan": (36, 138),
            "United States": (40, -95),
            "Chile": (-30, -71),
            "Australia": (-25, 133),
            "Nepal": (28, 84),
            "Thailand": (15, 101),
            "Bangladesh": (24, 90),
            "Pakistan": (30, 70),
            "Italy": (42, 12),
            "Greece": (39, 22),
            "Brazil": (-10, -55),
        }
        
        center = country_centers.get(country, (20, 0))
        
        # Create map
        country_map = folium.Map(
            location=center,
            zoom_start=6,
            tiles="OpenStreetMap"
        )
        
        # Add country title
        title_html = f"""
        <div style="position: fixed; top: 10px; left: 50px; 
        background-color: white; border:2px solid #3b82f6; z-index:9999; 
        font-size:18px; font-weight: bold; padding: 10px 15px;
        border-radius: 5px; box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">
            {country} - {len(disasters)} Active Events
        </div>
        """
        country_map.get_root().html.add_child(folium.Element(title_html))
        
        # Add all disaster markers
        for disaster in disasters:
            lat = disaster.get("latitude")
            lon = disaster.get("longitude")
            
            if lat is None or lon is None:
                continue
            
            severity = disaster.get("severity", "MEDIUM")
            color = self.SEVERITY_COLORS.get(severity, "#3b82f6")
            
            popup_html = self._create_popup(disaster)
            
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=400),
                tooltip=disaster.get("title", "Event"),
                icon=folium.Icon(
                    color=self._hex_to_color(color),
                    icon="exclamation-triangle",
                    prefix="fa"
                )
            ).add_to(country_map)
        
        folium.LayerControl().add_to(country_map)
        plugins.Fullscreen(position='topright').add_to(country_map)
        
        return country_map
    
    def display_map_in_streamlit(self, disaster_map: folium.Map):
        """Display folium map in Streamlit"""
        st_folium(disaster_map, width=1200, height=600)
    
    def create_cluster_map(self, disasters: List[Dict]) -> folium.Map:
        """Create map with clustered markers"""
        cluster_map = folium.Map(
            location=[20, 0],
            zoom_start=2,
            tiles="OpenStreetMap"
        )
        
        # Add marker cluster
        marker_cluster = plugins.MarkerCluster().add_to(cluster_map)
        
        # Add disasters to cluster
        for disaster in disasters:
            lat = disaster.get("latitude")
            lon = disaster.get("longitude")
            
            if lat and lon:
                severity = disaster.get("severity", "MEDIUM")
                color = self.SEVERITY_COLORS.get(severity, "#3b82f6")
                
                popup_html = self._create_popup(disaster)
                
                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(popup_html, max_width=400),
                    tooltip=disaster.get("title", "Event"),
                    icon=folium.Icon(
                        color=self._hex_to_color(color),
                        icon="exclamation-triangle",
                        prefix="fa"
                    )
                ).add_to(marker_cluster)
        
        folium.LayerControl().add_to(cluster_map)
        return cluster_map
