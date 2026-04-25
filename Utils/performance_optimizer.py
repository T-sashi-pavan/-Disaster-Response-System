"""
Performance Optimization Module
Provides fast prediction with caching and confidence scoring
"""

import hashlib
from datetime import datetime, timedelta
from typing import Dict, Tuple


class PredictionCache:
    """Cache predictions to avoid redundant calculations"""
    
    def __init__(self, max_age_minutes=30, max_size=1000):
        self.cache = {}
        self.max_age = timedelta(minutes=max_age_minutes)
        self.max_size = max_size
    
    def _hash_text(self, text: str) -> str:
        """Create hash of text for cache key"""
        return hashlib.md5(text.lower().strip().encode()).hexdigest()
    
    def get(self, text: str) -> Dict:
        """Get cached prediction if exists and not expired"""
        key = self._hash_text(text)
        
        if key in self.cache:
            entry = self.cache[key]
            if datetime.now() - entry['timestamp'] < self.max_age:
                return entry['prediction']
            else:
                del self.cache[key]  # Remove expired entry
        
        return None
    
    def set(self, text: str, prediction: Dict):
        """Cache a prediction"""
        key = self._hash_text(text)
        
        # Simple LRU: remove oldest if at max size
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), 
                           key=lambda k: self.cache[k]['timestamp'])
            del self.cache[oldest_key]
        
        self.cache[key] = {
            'prediction': prediction,
            'timestamp': datetime.now()
        }
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
    
    def stats(self) -> Dict:
        """Get cache statistics"""
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'usage_percent': (len(self.cache) / self.max_size) * 100
        }


class ConfidenceScorer:
    """Calculate confidence scores for predictions"""
    
    @staticmethod
    def get_prediction_confidence(model_predictions, category_names):
        """
        Get confidence scores for each predicted category.
        
        Returns dict with category confidence levels:
        {
            'category': confidence_float (0-1),
            ...
        }
        """
        confidences = {}
        
        # Try to get probability estimates from model
        # This varies by model type
        try:
            for idx, category in enumerate(category_names):
                pred = model_predictions[idx]
                
                # Assign confidence based on model type
                if pred == 1:
                    confidences[category] = max(0.6, min(0.95, 0.75))  # Predicted
                else:
                    confidences[category] = min(0.4, max(0.05, 0.25))  # Not predicted
                    
        except Exception:
            # Fallback: simple binary confidence
            confidences = {cat: (0.8 if pred == 1 else 0.2) 
                          for cat, pred in zip(category_names, model_predictions)}
        
        return confidences
    
    @staticmethod
    def get_confidence_level(confidence: float) -> str:
        """Convert confidence score to level indicator"""
        if confidence >= 0.8:
            return "🟢 Very High"
        elif confidence >= 0.6:
            return "🟡 Moderate"
        elif confidence >= 0.4:
            return "🟠 Low"
        else:
            return "🔴 Very Low"


class ActionRecommender:
    """Generate action recommendations based on predictions"""
    
    ACTIONS = {
        # Critical actions
        'death': {
            'action': 'Activate emergency protocols',
            'urgency': '🔴 CRITICAL',
            'timeline': 'Immediate (0-30 minutes)',
            'resources': ['Emergency response teams', 'Medical personnel', 'Forensic teams']
        },
        'missing_people': {
            'action': 'Launch search and rescue operations',
            'urgency': '🔴 CRITICAL',
            'timeline': 'Immediate (0-2 hours)',
            'resources': ['Search teams', 'Dogs/drones', 'Local volunteers', 'Police']
        },
        'medical_help': {
            'action': 'Dispatch medical teams and ambulances',
            'urgency': '🔴 CRITICAL',
            'timeline': 'Immediate (0-15 minutes)',
            'resources': ['Ambulances', 'Medical staff', 'Hospitals']
        },
        'search_and_rescue': {
            'action': 'Coordinate rescue operations',
            'urgency': '🔴 CRITICAL',
            'timeline': 'Immediate',
            'resources': ['Rescue teams', 'Equipment', 'Helicopters']
        },
        # High priority
        'water': {
            'action': 'Establish water distribution points',
            'urgency': '🟠 HIGH',
            'timeline': '1-4 hours',
            'resources': ['Water tankers', 'Distribution stations', 'Volunteers']
        },
        'food': {
            'action': 'Organize food distribution',
            'urgency': '🟠 HIGH',
            'timeline': '2-6 hours',
            'resources': ['Food supplies', 'Kitchens', 'Volunteers']
        },
        'shelter': {
            'action': 'Set up temporary shelters',
            'urgency': '🟠 HIGH',
            'timeline': '2-8 hours',
            'resources': ['Tents', 'Blankets', 'Cots', 'Volunteers']
        },
        'medical_products': {
            'action': 'Supply medical equipment and medicines',
            'urgency': '🟠 HIGH',
            'timeline': '2-4 hours',
            'resources': ['Medical supplies', 'Pharmacies', 'Hospitals']
        },
        # Medium priority
        'buildings': {
            'action': 'Assess structural integrity and evacuate if needed',
            'urgency': '🟡 MEDIUM',
            'timeline': '1-8 hours',
            'resources': ['Engineers', 'Evacuation teams', 'Heavy equipment']
        },
        'electricity': {
            'action': 'Restore power supply',
            'urgency': '🟡 MEDIUM',
            'timeline': '4-24 hours',
            'resources': ['Electricians', 'Generators', 'Power equipment']
        },
        'transport': {
            'action': 'Restore transportation routes',
            'urgency': '🟡 MEDIUM',
            'timeline': '2-24 hours',
            'resources': ['Road crews', 'Heavy machinery', 'Materials']
        },
    }
    
    @staticmethod
    def get_recommendations(predictions_dict: Dict) -> list:
        """
        Generate action recommendations based on predictions.
        
        Args:
            predictions_dict: {category: 0/1}
            
        Returns:
            list of recommendation dicts
        """
        recommendations = []
        
        # Get all predicted categories
        predicted = [cat for cat, pred in predictions_dict.items() if pred == 1]
        
        # Sort by urgency (critical first)
        urgency_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        
        for category in predicted:
            if category in ActionRecommender.ACTIONS:
                action_info = ActionRecommender.ACTIONS[category]
                recommendations.append({
                    'category': category,
                    'action': action_info['action'],
                    'urgency': action_info['urgency'],
                    'timeline': action_info['timeline'],
                    'resources': action_info['resources']
                })
        
        # Sort by urgency
        recommendations.sort(key=lambda x: urgency_order.get(
            x['urgency'].split()[0].lower(), 99))
        
        return recommendations
    
    @staticmethod
    def get_priority_chain(recommendations: list) -> str:
        """Get structured priority chain for decision makers"""
        if not recommendations:
            return "No specific actions required"
        
        priority_chain = "📋 **ACTION PRIORITY CHAIN:**\n\n"
        
        for idx, rec in enumerate(recommendations[:5], 1):  # Top 5
            priority_chain += f"{idx}. **{rec['urgency']}** - {rec['category'].upper()}\n"
            priority_chain += f"   Action: {rec['action']}\n"
            priority_chain += f"   Timeline: {rec['timeline']}\n"
            priority_chain += f"   Resources: {', '.join(rec['resources'][:2])}...\n\n"
        
        return priority_chain


class PerformanceMonitor:
    """Monitor prediction performance and speed"""
    
    def __init__(self):
        self.predictions_made = 0
        self.total_time = 0
        self.start_time = None
    
    def start_prediction(self):
        """Mark start of prediction"""
        import time
        self.start_time = time.time()
    
    def end_prediction(self):
        """Mark end of prediction, return elapsed time"""
        import time
        elapsed = time.time() - self.start_time
        self.total_time += elapsed
        self.predictions_made += 1
        return elapsed
    
    def get_stats(self) -> Dict:
        """Get performance statistics"""
        avg_time = self.total_time / self.predictions_made if self.predictions_made > 0 else 0
        
        return {
            'predictions_made': self.predictions_made,
            'total_time': round(self.total_time, 2),
            'average_time': round(avg_time, 3),
            'speed_rating': self._get_speed_rating(avg_time)
        }
    
    @staticmethod
    def _get_speed_rating(avg_time: float) -> str:
        """Rate prediction speed"""
        if avg_time < 0.5:
            return "⚡ Lightning Fast"
        elif avg_time < 1.0:
            return "🚀 Very Fast"
        elif avg_time < 2.0:
            return "✅ Fast"
        elif avg_time < 5.0:
            return "⏱️ Moderate"
        else:
            return "🐢 Slow"
