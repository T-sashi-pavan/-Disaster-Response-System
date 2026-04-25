"""
Prediction History Module
Tracks user predictions for analytics and reporting
"""

import json
from datetime import datetime
from tinydb import TinyDB, Query


class PredictionHistory:
    """Manage prediction history for users"""
    
    def __init__(self, db_path="users_db.json"):
        self.db = TinyDB(db_path)
        self.PredictionRecord = Query()
    
    def add_prediction(self, username, message, predictions, severity_level, severity_score):
        """
        Add a new prediction record to history.
        
        Args:
            username: str - User who made the prediction
            message: str - The input message
            predictions: dict - Category predictions {category: 0/1}
            severity_level: str - CRITICAL/HIGH/MEDIUM/LOW
            severity_score: int - 0-100
        """
        record = {
            "username": username,
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "message_length": len(message),
            "predictions": predictions,
            "severity_level": severity_level,
            "severity_score": severity_score,
            "disaster_count": sum(predictions.values())  # How many categories predicted
        }
        
        # Add to a 'predictions' table
        if 'predictions' not in self.db.tables():
            predictions_table = self.db.table('predictions')
        else:
            predictions_table = self.db.table('predictions')
        
        predictions_table.insert(record)
    
    def get_user_predictions(self, username, limit=None):
        """
        Get all predictions for a user.
        
        Args:
            username: str
            limit: int - Maximum number of records to return (most recent first)
            
        Returns:
            list of prediction records
        """
        predictions_table = self.db.table('predictions')
        user_preds = predictions_table.search(
            self.PredictionRecord.username == username
        )
        
        # Sort by timestamp descending (most recent first)
        user_preds.sort(key=lambda x: x['timestamp'], reverse=True)
        
        if limit:
            return user_preds[:limit]
        return user_preds
    
    def get_user_stats(self, username):
        """
        Get analytics for a user.
        
        Returns:
            dict with stats like:
            - total_predictions: int
            - avg_severity: float
            - most_common_disaster: str with count
            - severity_distribution: dict of level: count
        """
        predictions = self.get_user_predictions(username)
        
        if not predictions:
            return {
                "total_predictions": 0,
                "avg_severity": 0,
                "most_common_disaster": None,
                "severity_distribution": {},
                "predictions": []
            }
        
        # Calculate statistics
        total = len(predictions)
        avg_severity = sum(p['severity_score'] for p in predictions) / total
        
        # Count each disaster category
        disaster_counts = {}
        for pred in predictions:
            for category, value in pred['predictions'].items():
                if value == 1:
                    disaster_counts[category] = disaster_counts.get(category, 0) + 1
        
        most_common = max(disaster_counts.items(), key=lambda x: x[1]) if disaster_counts else (None, 0)
        
        # Severity distribution
        severity_dist = {}
        for pred in predictions:
            level = pred['severity_level']
            severity_dist[level] = severity_dist.get(level, 0) + 1
        
        return {
            "total_predictions": total,
            "avg_severity": round(avg_severity, 2),
            "most_common_disaster": most_common[0],
            "most_common_count": most_common[1],
            "severity_distribution": severity_dist,
            "all_disasters_seen": dict(sorted(disaster_counts.items(), key=lambda x: x[1], reverse=True)),
            "predictions": predictions
        }
    
    def clear_user_history(self, username):
        """Delete all predictions for a user (with confirmation)"""
        predictions_table = self.db.table('predictions')
        predictions_table.remove(self.PredictionRecord.username == username)
    
    def export_user_history_csv(self, username):
        """
        Export user predictions as CSV string.
        
        Returns:
            str in CSV format
        """
        import csv
        from io import StringIO
        
        predictions = self.get_user_predictions(username)
        
        if not predictions:
            return None
        
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            'timestamp', 'message', 'severity_level', 'severity_score', 'disaster_count'
        ])
        
        writer.writeheader()
        for pred in predictions:
            writer.writerow({
                'timestamp': pred['timestamp'],
                'message': pred['message'][:100],  # First 100 chars
                'severity_level': pred['severity_level'],
                'severity_score': pred['severity_score'],
                'disaster_count': pred['disaster_count']
            })
        
        return output.getvalue()
