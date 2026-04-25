"""
Alert System for CRITICAL Disasters
Send email/SMS notifications and in-app alerts to responders
"""

import smtplib
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tinydb import TinyDB, Query

class AlertSystem:
    """Manage alerts and notifications for critical disasters"""
    
    def __init__(self, db_path="users_db.json"):
        self.db = TinyDB(db_path)
        self.responders_table = self.db.table("responders")
    
    def register_responder(self, name, email, disaster_types=None, alert_level="HIGH"):
        """
        Register a responder to receive alerts
        
        Args:
            name: Responder name
            email: Email address
            disaster_types: List of disaster types to alert on (None = all)
            alert_level: Minimum alert level (CRITICAL, HIGH, MEDIUM, LOW)
        """
        responder = {
            "name": name,
            "email": email,
            "disaster_types": disaster_types or [],
            "alert_level": alert_level,
            "registered_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "alerts_received": 0,
            "active": True
        }
        
        # Check if already exists
        Responder = Query()
        existing = self.responders_table.search(Responder.email == email)
        if existing:
            self.responders_table.update(responder, Responder.email == email)
        else:
            self.responders_table.insert(responder)
        
        return f"✅ Responder {name} registered for alerts via {email}"
    
    def get_responders_for_alert(self, severity_level, disaster_categories):
        """Get responders who should be alerted"""
        severity_rank = {"CRITICAL": 1, "HIGH": 2, "MEDIUM": 3, "LOW": 4}
        severity_value = severity_rank.get(severity_level, 4)
        
        alert_responders = []
        
        for responder in self.responders_table.all():
            if not responder.get("active"):
                continue
            
            # Check severity threshold
            responder_rank = severity_rank.get(responder.get("alert_level", "HIGH"), 2)
            if severity_value > responder_rank:
                continue  # Not severe enough
            
            # Check disaster type match
            disaster_types = responder.get("disaster_types", [])
            if disaster_types:
                # If responder has specific types, only match those
                if not any(cat in disaster_types for cat in disaster_categories):
                    continue
            
            alert_responders.append(responder)
        
        return alert_responders
    
    def send_email_alert(self, responder_email, severity, disasters, message_text, severity_score):
        """
        Send email alert (mock version - would need SMTP config in production)
        
        Args:
            responder_email: Email address to send to
            severity: Severity level (CRITICAL, HIGH, etc.)
            disasters: List of disaster categories
            message_text: Original message text
            severity_score: Severity score (0-100)
        """
        # In production, configure this with real email service
        # For now, return mock success
        
        email_body = f"""
        🚨 DISASTER ALERT - {severity} Priority
        
        Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        Severity Score: {severity_score}/100
        
        Detected Disasters:
        {', '.join(disasters)}
        
        Message:
        "{message_text}"
        
        Action Required: Please respond to this alert in the Disaster Response System
        
        ---
        This is an automated alert from the Disaster Response Classification System
        """
        
        # Mock: In production, use smtplib
        return {
            "status": "sent",
            "recipient": responder_email,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity": severity,
            "disasters": disasters
        }
    
    def log_alert(self, responder_email, severity, disasters, message_id=None):
        """Log alert for audit trail"""
        alert_log_table = self.db.table("alert_logs")
        
        alert_record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "responder_email": responder_email,
            "severity": severity,
            "disasters": disasters,
            "message_id": message_id,
            "status": "sent"
        }
        
        alert_log_table.insert(alert_record)
    
    def get_all_responders(self):
        """Get all registered responders"""
        return self.responders_table.all()
    
    def deactivate_responder(self, email):
        """Deactivate responder alerts"""
        Responder = Query()
        self.responders_table.update({"active": False}, Responder.email == email)
    
    def get_alert_stats(self):
        """Get alert statistics"""
        alert_logs = self.db.table("alert_logs")
        all_alerts = alert_logs.all()
        
        critical_count = len([a for a in all_alerts if a.get("severity") == "CRITICAL"])
        high_count = len([a for a in all_alerts if a.get("severity") == "HIGH"])
        
        return {
            "total_alerts_sent": len(all_alerts),
            "critical_alerts": critical_count,
            "high_alerts": high_count,
            "total_responders": len(self.get_all_responders()),
            "active_responders": len([r for r in self.get_all_responders() if r.get("active")])
        }
