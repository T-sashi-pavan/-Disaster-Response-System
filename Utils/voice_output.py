"""
Text-to-Speech Voice Output Module
Reads prediction results aloud using pyttsx3
"""

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

import threading
from typing import Optional

class VoiceOutput:
    """Handle text-to-speech for disaster analysis results"""
    
    def __init__(self, rate: int = 150, volume: float = 0.9):
        """
        Initialize text-to-speech engine
        
        Args:
            rate: Speech rate (words per minute)
            volume: Volume level (0.0 to 1.0)
        """
        self.available = False
        self.engine = None
        
        if not PYTTSX3_AVAILABLE:
            print("Warning: pyttsx3 not installed - voice output disabled")
            return
            
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            self.available = True
        except Exception as e:
            print(f"Warning: Text-to-speech not available: {str(e)}")
            self.available = False
            self.engine = None
    
    def speak(self, text: str, wait: bool = False):
        """
        Speak text using TTS
        
        Args:
            text: Text to speak
            wait: If True, wait for speech to complete
        """
        if not self.available or not self.engine:
            return
        
        try:
            self.engine.say(text)
            if wait:
                self.engine.runAndWait()
            else:
                # Run in background thread
                threading.Thread(target=self.engine.runAndWait, daemon=True).start()
        except Exception as e:
            print(f"Error during speech: {str(e)}")
    
    def speak_async(self, text: str):
        """Speak text asynchronously in background thread"""
        threading.Thread(target=self._speak_in_thread, args=(text,), daemon=True).start()
    
    def _speak_in_thread(self, text: str):
        """Speak in background thread"""
        try:
            if self.available and self.engine:
                self.engine.say(text)
                self.engine.runAndWait()
        except Exception as e:
            print(f"Error in background speech: {str(e)}")
    
    def speak_disaster_alert(self, disaster_info: dict):
        """
        Speak formatted disaster alert
        
        Args:
            disaster_info: Dictionary with disaster details
        """
        alert_text = self._format_disaster_alert(disaster_info)
        self.speak_async(alert_text)
    
    def _format_disaster_alert(self, info: dict) -> str:
        """Format disaster info for voice output"""
        parts = []
        
        # Title
        if "title" in info:
            parts.append(f"Disaster Alert: {info['title']}")
        
        # Location
        if "country" in info:
            parts.append(f"Location: {info['country']}")
        
        # Type
        if "disaster_type" in info:
            parts.append(f"Type: {info['disaster_type']}")
        
        # Severity
        if "severity" in info:
            parts.append(f"Severity: {info['severity']}")
        
        # Priority
        if "priority_score" in info:
            parts.append(f"Priority: {info['priority_score']} out of 10")
        
        # Required help
        if "required_help" in info and info["required_help"]:
            parts.append(f"Required help: {', '.join(info['required_help'][:2])}")
        
        # Recommended action
        if "recommended_action" in info:
            parts.append(f"Action: {info['recommended_action']}")
        
        return ". ".join(parts)
    
    def speak_prediction_result(self, result: dict):
        """
        Speak prediction analysis result
        
        Args:
            result: Prediction result dictionary
        """
        alert_text = self._format_prediction_result(result)
        self.speak_async(alert_text)
    
    def _format_prediction_result(self, result: dict) -> str:
        """Format prediction result for voice output"""
        parts = [
            f"Analysis complete.",
            f"Disaster related: {result.get('is_disaster_related', 'Unknown')}"
        ]
        
        if result.get('disaster_type'):
            parts.append(f"Disaster type: {result['disaster_type']}")
        
        if result.get('severity'):
            parts.append(f"Severity: {result['severity']}")
        
        if result.get('priority_score'):
            parts.append(f"Priority score: {result['priority_score']} out of 10")
        
        if result.get('affected_location'):
            parts.append(f"Location: {result['affected_location']}")
        
        if result.get('needs'):
            parts.append(f"Needs: {', '.join(result['needs'][:2])}")
        
        if result.get('recommended_action'):
            parts.append(f"Action: {result['recommended_action']}")
        
        return ". ".join(parts)
    
    def stop(self):
        """Stop current speech"""
        if self.available and self.engine:
            try:
                self.engine.stop()
            except:
                pass
    
    def shutdown(self):
        """Shutdown TTS engine"""
        if self.available and self.engine:
            try:
                self.engine.stop()
                self.engine._cleanup()
            except:
                pass
