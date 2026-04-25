"""
Text Statistics Module
Analyze text in real-time: word count, sentiment, reading time, keywords
"""

import re
from collections import Counter


# Key disaster-related keywords that might trigger predictions
DISASTER_KEYWORDS = {
    'death': ['death', 'died', 'kill', 'fatal', 'deceased', 'casualty'],
    'medical': ['medical', 'hospital', 'injured', 'wound', 'doctor', 'patient', 'disease', 'illness'],
    'water': ['water', 'flood', 'drown', 'wet', 'rain', 'storm'],
    'food': ['food', 'hunger', 'starv', 'eat', 'meal', 'hungry'],
    'shelter': ['shelter', 'home', 'house', 'roof', 'building', 'homeless'],
    'security': ['security', 'safe', 'danger', 'violence', 'attack', 'war', 'conflict'],
    'rescue': ['rescue', 'help', 'emergency', 'save', 'aid', 'assist'],
    'infrastructure': ['road', 'bridge', 'electric', 'power', 'transport', 'building'],
    'money': ['money', 'fund', 'donation', 'financial', 'cost', 'expense'],
    'child': ['child', 'children', 'kid', 'baby', 'infant', 'minor']
}


class TextAnalyzer:
    """Analyze disaster-related text in real-time"""
    
    @staticmethod
    def basic_stats(text):
        """
        Calculate basic text statistics.
        
        Args:
            text: str - Input text
            
        Returns:
            dict with stats
        """
        words = text.split()
        sentences = text.split('.')
        characters = len(text)
        
        return {
            'character_count': characters,
            'word_count': len(words),
            'sentence_count': len([s for s in sentences if s.strip()]),
            'avg_word_length': round(characters / len(words), 2) if words else 0
        }
    
    @staticmethod
    def reading_time(text):
        """
        Estimate reading time in minutes.
        
        Args:
            text: str
            
        Returns:
            float - Minutes (assuming ~200 words per minute)
        """
        word_count = len(text.split())
        reading_speed = 200  # words per minute
        minutes = max(0.1, word_count / reading_speed)
        return round(minutes, 2)
    
    @staticmethod
    def text_quality(text):
        """
        Assess text quality and provide feedback.
        
        Args:
            text: str
            
        Returns:
            dict with quality assessment
        """
        stats = TextAnalyzer.basic_stats(text)
        word_count = stats['word_count']
        
        feedback = []
        quality_score = 100
        
        # Check length
        if word_count < 3:
            feedback.append("⚠️ Message too short for accurate classification")
            quality_score -= 40
        elif word_count < 10:
            feedback.append("ℹ️ Consider adding more context")
            quality_score -= 15
        
        # Check for common patterns
        if text.isupper():
            feedback.append("⚠️ All caps makes it harder to classify accurately")
            quality_score -= 10
        
        if text.count('!!!') > 2 or text.count('...') > 2:
            feedback.append("ℹ️ Multiple punctuation marks may reduce accuracy")
            quality_score -= 5
        
        quality_score = max(0, quality_score)
        
        if quality_score >= 80:
            level = "✅ Excellent"
        elif quality_score >= 60:
            level = "ℹ️ Good"
        elif quality_score >= 40:
            level = "⚠️ Fair"
        else:
            level = "❌ Poor"
        
        return {
            'quality_score': quality_score,
            'quality_level': level,
            'feedback': feedback if feedback else ["✅ Text looks good for classification"]
        }
    
    @staticmethod
    def find_disaster_keywords(text):
        """
        Find disaster-related keywords in text.
        
        Args:
            text: str
            
        Returns:
            dict with found keywords by category
        """
        text_lower = text.lower()
        found_keywords = {}
        
        for category, keywords in DISASTER_KEYWORDS.items():
            found = []
            for keyword in keywords:
                # Use word boundaries for more accurate matching
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, text_lower):
                    found.append(keyword)
            
            if found:
                found_keywords[category] = found
        
        return found_keywords
    
    @staticmethod
    def simple_sentiment(text):
        """
        Simple sentiment analysis based on keywords.
        
        Args:
            text: str
            
        Returns:
            dict with sentiment assessment
        """
        text_lower = text.lower()
        
        positive_words = ['help', 'relief', 'rescue', 'safe', 'good', 'thanks', 'aid', 'support']
        negative_words = ['death', 'die', 'injured', 'pain', 'suffering', 'crisis', 'emergency', 'danger']
        
        positive_count = sum(text_lower.count(word) for word in positive_words)
        negative_count = sum(text_lower.count(word) for word in negative_words)
        
        if negative_count > positive_count:
            sentiment = "🔴 Negative (Critical/Urgent)"
            polarity = "negative"
        elif positive_count > negative_count:
            sentiment = "🟢 Positive (Resolution/Help)"
            polarity = "positive"
        else:
            sentiment = "🟡 Neutral"
            polarity = "neutral"
        
        return {
            'sentiment': sentiment,
            'polarity': polarity,
            'positive_score': positive_count,
            'negative_score': negative_count
        }
    
    @staticmethod
    def language_complexity(text):
        """
        Assess language complexity.
        
        Args:
            text: str
            
        Returns:
            str - Simple/Moderate/Complex assessment
        """
        words = text.split()
        
        # Count complex words (longer than 8 characters)
        complex_words = sum(1 for word in words if len(word) > 8)
        complexity_ratio = complex_words / len(words) if words else 0
        
        if complexity_ratio < 0.1:
            return "📝 Simple (Easy to understand)"
        elif complexity_ratio < 0.25:
            return "📝 Moderate (Clearly written)"
        else:
            return "📝 Complex (May affect classification)"
    
    @staticmethod
    def get_full_analysis(text):
        """
        Get complete text analysis.
        
        Args:
            text: str
            
        Returns:
            dict with all analysis results
        """
        return {
            'basic_stats': TextAnalyzer.basic_stats(text),
            'reading_time': TextAnalyzer.reading_time(text),
            'quality': TextAnalyzer.text_quality(text),
            'keywords': TextAnalyzer.find_disaster_keywords(text),
            'sentiment': TextAnalyzer.simple_sentiment(text),
            'language': TextAnalyzer.language_complexity(text)
        }
