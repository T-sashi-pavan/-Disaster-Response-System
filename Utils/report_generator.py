"""
Report Generation & PDF Export
Generate incident reports from disaster predictions
"""

from datetime import datetime
import io

class ReportGenerator:
    """Generate incident reports from predictions"""
    
    def __init__(self):
        self.report_templates = {
            "earthquake": "Earthquake Response Protocol",
            "flood": "Flood Response Protocol",  
            "storm": "Storm Response Protocol",
            "fire": "Fire Response Protocol",
            "infrastructure_related": "Infrastructure Damage Assessment",
            "medical_help": "Medical Emergency Response",
            "search_and_rescue": "Search & Rescue Operations",
            "shelter": "Shelter & Evacuation Protocol"
        }
    
    def generate_incident_report(self, message_text, predictions, severity_info, recommendations):
        """Generate detailed incident report"""
        
        report = {
            "report_id": f"INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity_level": severity_info.get("severity_level", "UNKNOWN"),
            "severity_score": severity_info.get("severity_score", 0),
            "original_message": message_text,
            "detected_disasters": severity_info.get("affected_categories", []),
            "recommendations": recommendations
        }
        
        return report
    
    def format_text_report(self, report):
        """Format report as readable text"""
        
        text = f"""
╔══════════════════════════════════════════════════╗
║        DISASTER INCIDENT REPORT                  ║
╚══════════════════════════════════════════════════╝

Report ID: {report['report_id']}
Generated: {report['timestamp']}

╔══════════════════════════════════════════════════╗
║        SEVERITY ASSESSMENT                       ║
╚══════════════════════════════════════════════════╝

Priority Level: {report['severity_level']}
Severity Score: {report['severity_score']}/100

╔══════════════════════════════════════════════════╗
║        DETECTED DISASTERS                        ║
╚══════════════════════════════════════════════════╝

{chr(10).join([f"• {d}" for d in report.get('detected_disasters', [])])}

╔══════════════════════════════════════════════════╗
║        ORIGINAL MESSAGE                          ║
╚══════════════════════════════════════════════════╝

"{report['original_message']}"

╔══════════════════════════════════════════════════╗
║        RECOMMENDED ACTIONS                       ║
╚══════════════════════════════════════════════════╝

{self._format_recommendations(report['recommendations'])}

╔══════════════════════════════════════════════════╗
║        END OF REPORT                             ║
╚══════════════════════════════════════════════════╝
"""
        return text
    
    def _format_recommendations(self, recommendations):
        """Format recommendations nicely"""
        if not recommendations:
            return "No specific actions required."
        
        formatted = []
        for idx, rec in enumerate(recommendations[:3], 1):
            action_text = f"""
{idx}. {rec.get('category', 'ACTION').upper()}
   Urgency: {rec.get('urgency', 'NORMAL')}
   Action: {rec.get('action', 'N/A')}
   Timeline: {rec.get('timeline', 'ASAP')}
   Resources: {', '.join(rec.get('resources', []))}
"""
            formatted.append(action_text)
        
        return chr(10).join(formatted)
    
    def export_to_csv_line(self, report):
        """Export single report as CSV line"""
        disasters = "|".join(report.get('detected_disasters', []))
        return f"{report['report_id']},{report['timestamp']},{report['severity_level']},{report['severity_score']},{disasters}"


class ResourceCalculator:
    """Calculate resource needs based on disaster type"""
    
    # Resource templates for different disaster types
    RESOURCE_TEMPLATES = {
        "earthquake": {
            "search_and_rescue_teams": 5,
            "medical_teams": 3,
            "structural_engineers": 2,
            "heavy_equipment": "8-10 units",
            "volunteers": "50-100",
            "estimated_response_time": "0-1 hour"
        },
        "flood": {
            "rescue_boats": 10,
            "water_pumps": 5,
            "sandbags": "10,000+",
            "medical_teams": 2,
            "temporary_shelters": 3,
            "water_treatment_units": 2,
            "estimated_response_time": "2-4 hours"
        },
        "storm": {
            "emergency_response_units": 4,
            "medical_teams": 2,
            "power_restoration_crews": 6,
            "debris_removal_equipment": "5-8 units",
            "temporary_shelters": 5,
            "estimated_response_time": "1-2 hours"
        },
        "fire": {
            "fire_fighting_units": 8,
            "paramedics": 4,
            "evacuation_teams": 5,
            "water_tankers": 6,
            "emergency_shelters": 3,
            "estimated_response_time": "0-30 minutes"
        },
        "medical_help": {
            "ambulances": 5,
            "medical_teams": 3,
            "hospitals_on_alert": 2,
            "paramedics": 10,
            "blood_units": "20-50 units",
            "estimated_response_time": "5-15 minutes"
        },
        "shelter": {
            "temporary_shelters": 5,
            "food_units": 10,
            "water_distribution": 5,
            "medical_stations": 2,
            "volunteers": "100-200",
            "estimated_response_time": "1-3 hours"
        },
        "search_and_rescue": {
            "rescue_teams": 8,
            "sniffer_dogs": 3,
            "heavy_equipment": "10-15 units",
            "medical_teams": 4,
            "command_centers": 1,
            "estimated_response_time": "0-2 hours"
        }
    }
    
    def calculate_resources(self, predicted_disasters, severity_score):
        """
        Calculate resource needs based on disasters and severity
        
        Args:
            predicted_disasters: List of disaster categories
            severity_score: Severity score (0-100)
        """
        
        # Multiplier based on severity
        if severity_score >= 75:
            multiplier = 1.5  # CRITICAL - mobilize extra resources
        elif severity_score >= 50:
            multiplier = 1.2  # HIGH - increase standard resources
        else:
            multiplier = 1.0  # MEDIUM/LOW - standard resources
        
        combined_resources = {}
        
        for disaster in predicted_disasters:
            disaster_lower = disaster.lower().replace(" ", "_")
            
            if disaster_lower in self.RESOURCE_TEMPLATES:
                template = self.RESOURCE_TEMPLATES[disaster_lower]
                
                for resource, quantity in template.items():
                    if resource == "estimated_response_time":
                        if resource not in combined_resources:
                            combined_resources[resource] = quantity
                        continue
                    
                    if isinstance(quantity, int):
                        # Multiply numeric resources by severity multiplier
                        new_qty = int(quantity * multiplier)
                        if resource in combined_resources:
                            combined_resources[resource] += new_qty
                        else:
                            combined_resources[resource] = new_qty
                    else:
                        # String resources - just add to notes
                        if resource not in combined_resources:
                            combined_resources[resource] = quantity
        
        return {
            "severity_multiplier": multiplier,
            "resources": combined_resources,
            "summary": self._generate_summary(combined_resources),
            "urgency": self._calculate_urgency(severity_score)
        }
    
    def _generate_summary(self, resources):
        """Generate human-readable summary"""
        summary = []
        
        for resource, quantity in resources.items():
            if resource == "estimated_response_time":
                summary.append(f"Expected Response: {quantity}")
            elif isinstance(quantity, int) and quantity > 0:
                summary.append(f"• {quantity} {resource.replace('_', ' ').title()}")
            elif isinstance(quantity, str):
                summary.append(f"• {quantity.replace('_', ' ').title()}")
        
        return summary
    
    def _calculate_urgency(self, severity_score):
        """Calculate urgency level"""
        if severity_score >= 75:
            return "🚨 CRITICAL - IMMEDIATE DEPLOYMENT"
        elif severity_score >= 50:
            return "🔴 HIGH - DEPLOY WITHIN 1 HOUR"
        elif severity_score >= 25:
            return "🟠 MEDIUM - STANDBY & PREPARE"
        else:
            return "🟡 LOW - MONITOR SITUATION"
