"""
Disaster Trends & Feedback Analysis
Analyze patterns from prediction history and user feedback
"""

from tinydb import TinyDB, Query
from datetime import datetime, timedelta
from collections import Counter
import pandas as pd

class TrendsAnalyzer:
    """Analyze disaster trends from prediction history"""
    
    def __init__(self, db_path="users_db.json"):
        self.db = TinyDB(db_path)
        self.history_table = self.db.table("prediction_history")
        self.feedback_table = self.db.table("user_feedback")
    
    def get_most_common_disasters(self, limit=10, days=None):
        """Get most frequently predicted disasters"""
        history = self.history_table.all()
        
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            history = [h for h in history if datetime.strptime(
                h.get("timestamp", ""), "%Y-%m-%d %H:%M:%S"
            ) > cutoff_date]
        
        disaster_counts = Counter()
        for record in history:
            predictions = record.get("predictions", {})
            for disaster, value in predictions.items():
                if value == 1:
                    disaster_counts[disaster] += 1
        
        return dict(disaster_counts.most_common(limit))
    
    def get_disaster_correlation(self, limit=15):
        """Get which disasters commonly occur together"""
        history = self.history_table.all()
        
        disaster_pairs = Counter()
        for record in history:
            predictions = record.get("predictions", {})
            disasters = [d for d, v in predictions.items() if v == 1]
            
            # Count pairs
            for i in range(len(disasters)):
                for j in range(i+1, len(disasters)):
                    pair = tuple(sorted([disasters[i], disasters[j]]))
                    disaster_pairs[pair] += 1
        
        return dict(disaster_pairs.most_common(limit))
    
    def get_severity_distribution(self):
        """Get distribution of severity levels"""
        history = self.history_table.all()
        
        severity_counts = {
            "CRITICAL": len([h for h in history if h.get("severity_level") == "CRITICAL"]),
            "HIGH": len([h for h in history if h.get("severity_level") == "HIGH"]),
            "MEDIUM": len([h for h in history if h.get("severity_level") == "MEDIUM"]),
            "LOW": len([h for h in history if h.get("severity_level") == "LOW"])
        }
        
        return severity_counts
    
    def get_trends_by_timeframe(self, timeframe_days=7):
        """Get trends over specific timeframe"""
        history = self.history_table.all()
        cutoff = datetime.now() - timedelta(days=timeframe_days)
        
        recent = [h for h in history if datetime.strptime(
            h.get("timestamp", ""), "%Y-%m-%d %H:%M:%S"
        ) > cutoff]
        
        disaster_counts = Counter()
        for record in recent:
            predictions = record.get("predictions", {})
            for disaster, value in predictions.items():
                if value == 1:
                    disaster_counts[disaster] += 1
        
        return {
            "timeframe_days": timeframe_days,
            "messages_in_period": len(recent),
            "top_disasters": dict(disaster_counts.most_common(10))
        }


class FeedbackTracker:
    """Track user feedback on prediction accuracy"""
    
    def __init__(self, db_path="users_db.json"):
        self.db = TinyDB(db_path)
        self.feedback_table = self.db.table("user_feedback")
    
    def record_feedback(self, message_id, actual_disasters, predicted_disasters, accuracy_rating, username=None):
        """
        Record user feedback on prediction accuracy
        
        Args:
            message_id: ID of the prediction
            actual_disasters: What user says actually happened
            predicted_disasters: What model predicted
            accuracy_rating: 1-5 scale (1=very wrong, 5=perfect)
            username: User providing feedback
        """
        feedback = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_id": message_id,
            "actual_disasters": actual_disasters,
            "predicted_disasters": predicted_disasters,
            "accuracy_rating": accuracy_rating,
            "username": username or "anonymous",
            "model_confidence": self._calculate_match(predicted_disasters, actual_disasters)
        }
        
        self.feedback_table.insert(feedback)
        return feedback
    
    def _calculate_match(self, predicted, actual):
        """Calculate what % of predictions were correct"""
        if not predicted:
            return 0
        
        correct = len([p for p in predicted if p in actual])
        return correct / len(predicted)
    
    def get_model_improvement_metrics(self):
        """Get stats on model accuracy based on feedback"""
        all_feedback = self.feedback_table.all()
        
        if not all_feedback:
            return {
                "total_feedback": 0,
                "average_rating": 0,
                "model_match_rate": 0,
                "improvement_trend": "No data yet"
            }
        
        ratings = [f.get("accuracy_rating", 3) for f in all_feedback]
        match_rates = [f.get("model_confidence", 0) for f in all_feedback]
        
        return {
            "total_feedback": len(all_feedback),
            "average_rating": sum(ratings) / len(ratings),
            "average_match_rate": sum(match_rates) / len(match_rates),
            "recent_feedback": all_feedback[-5:],  # Last 5
            "accuracy_distribution": {
                "perfect": len([r for r in ratings if r == 5]),
                "good": len([r for r in ratings if r == 4]),
                "ok": len([r for r in ratings if r == 3]),
                "poor": len([r for r in ratings if r == 2]),
                "very_poor": len([r for r in ratings if r == 1])
            }
        }
    
    def get_most_misclassified_disasters(self, limit=10):
        """Get disasters that are most often mispredicted"""
        all_feedback = self.feedback_table.all()
        
        misclassified = Counter()
        for feedback in all_feedback:
            predicted = set(feedback.get("predicted_disasters", []))
            actual = set(feedback.get("actual_disasters", []))
            
            # Disasters that were predicted but shouldn't have been
            false_positives = predicted - actual
            for fp in false_positives:
                misclassified[f"{fp} (false positive)"] += 1
            
            # Disasters that occurred but weren't predicted
            false_negatives = actual - predicted
            for fn in false_negatives:
                misclassified[f"{fn} (false negative)"] += 1
        
        return dict(misclassified.most_common(limit))
    
    def get_user_feedback_contribution(self, username):
        """Get feedback metrics for a specific user"""
        Feedback = Query()
        user_feedback = self.feedback_table.search(Feedback.username == username)
        
        if not user_feedback:
            return {"total_feedback": 0, "avg_rating": 0}
        
        ratings = [f.get("accuracy_rating", 3) for f in user_feedback]
        
        return {
            "total_feedback": len(user_feedback),
            "avg_rating": sum(ratings) / len(ratings),
            "contributions": len(user_feedback)
        }
