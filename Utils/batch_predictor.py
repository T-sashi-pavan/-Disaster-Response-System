"""
Batch Prediction Module
Process multiple disaster messages from CSV files in bulk
"""

import io
import csv
import pandas as pd
from datetime import datetime


class BatchPredictor:
    """Handle batch predictions from CSV files"""
    
    def __init__(self, model, category_names):
        """
        Initialize batch predictor.
        
        Args:
            model: trained sklearn pipeline
            category_names: list of disaster category names
        """
        self.model = model
        self.category_names = category_names
    
    def validate_csv(self, uploaded_file):
        """
        Validate uploaded CSV file.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            tuple: (is_valid: bool, messages: list, error_message: str)
        """
        try:
            # Read CSV
            df = pd.read_csv(uploaded_file)
            
            # Check for required columns
            required_cols = ['message', 'text', 'content', 'Message', 'Text']
            message_col = None
            
            for col in required_cols:
                if col in df.columns:
                    message_col = col
                    break
            
            if not message_col:
                return False, [], f"CSV must contain a 'message' or 'text' column. Found: {list(df.columns)}"
            
            # Extract messages
            messages = df[message_col].dropna().astype(str).tolist()
            
            if not messages:
                return False, [], "No valid messages found in CSV"
            
            if len(messages) > 10000:
                return False, [], f"Too many messages ({len(messages)}). Maximum is 10,000"
            
            return True, messages, None
            
        except pd.errors.ParserError as e:
            return False, [], f"CSV parsing error: {str(e)}"
        except Exception as e:
            return False, [], f"Error reading file: {str(e)}"
    
    def predict_batch(self, messages, progress_callback=None):
        """
        Get predictions for multiple messages.
        
        Args:
            messages: list of text strings
            progress_callback: function(current, total) for progress tracking
            
        Returns:
            list of prediction records
        """
        results = []
        
        for idx, message in enumerate(messages):
            if progress_callback:
                progress_callback(idx + 1, len(messages))
            
            try:
                # Get prediction
                preds = self.model.predict([message])[0]
                
                # Create prediction dict
                predictions_dict = {
                    cat: int(pred) for cat, pred in zip(self.category_names, preds)
                }
                
                results.append({
                    'message': message,
                    'predictions': predictions_dict,
                    'disaster_count': sum(predictions_dict.values()),
                    'status': 'success'
                })
                
            except Exception as e:
                results.append({
                    'message': message,
                    'error': str(e),
                    'status': 'failed'
                })
        
        return results
    
    def export_results_csv(self, results, include_all_categories=False):
        """
        Export prediction results as CSV.
        
        Args:
            results: list of prediction records from predict_batch
            include_all_categories: if True, include all disaster columns
            
        Returns:
            str in CSV format
        """
        output = io.StringIO()
        
        if not results:
            return None
        
        successful_results = [r for r in results if r['status'] == 'success']
        
        if not successful_results:
            return None
        
        if include_all_categories:
            # Full results with all disaster categories
            fieldnames = ['message', 'disaster_count'] + list(self.category_names)
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in successful_results:
                row = {
                    'message': result['message'][:100],
                    'disaster_count': result['disaster_count']
                }
                row.update(result['predictions'])
                writer.writerow(row)
        else:
            # Summary results
            fieldnames = ['message', 'disaster_count', 'detected_disasters']
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in successful_results:
                detected = [cat for cat, val in result['predictions'].items() if val == 1]
                row = {
                    'message': result['message'][:100],
                    'disaster_count': result['disaster_count'],
                    'detected_disasters': '; '.join(detected) if detected else 'None'
                }
                writer.writerow(row)
        
        return output.getvalue()
    
    def get_batch_summary(self, results):
        """
        Generate summary statistics for batch results.
        
        Args:
            results: list of prediction records
            
        Returns:
            dict with summary stats
        """
        successful = [r for r in results if r['status'] == 'success']
        failed = [r for r in results if r['status'] == 'failed']
        
        if not successful:
            return {
                'total': len(results),
                'successful': 0,
                'failed': len(failed),
                'avg_disaster_count': 0,
                'most_common_disaster': None
            }
        
        # Count each disaster type
        disaster_counts = {}
        total_disaster_count = 0
        
        for result in successful:
            for category, value in result['predictions'].items():
                if value == 1:
                    disaster_counts[category] = disaster_counts.get(category, 0) + 1
            total_disaster_count += result['disaster_count']
        
        avg_disaster_count = total_disaster_count / len(successful) if successful else 0
        most_common = max(disaster_counts.items(), key=lambda x: x[1]) if disaster_counts else (None, 0)
        
        return {
            'total': len(results),
            'successful': len(successful),
            'failed': len(failed),
            'avg_disaster_count': round(avg_disaster_count, 2),
            'most_common_disaster': most_common[0],
            'most_common_count': most_common[1],
            'all_disasters_found': dict(sorted(disaster_counts.items(), key=lambda x: x[1], reverse=True))
        }
