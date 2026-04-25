"""
Severity Scoring Module for Disaster Classification
Assigns severity levels and priority rankings to disaster predictions
"""

# Severity mapping: which disaster categories indicate critical vs routine needs
SEVERITY_MAPPING = {
    # CRITICAL - Life-threatening situations requiring immediate response
    "critical": {
        "categories": ["death", "missing_people", "medical_help", "search_and_rescue"],
        "color": "🔴",
        "level": "CRITICAL",
        "recommendation": "⚠️ Immediate response required. Emergency services should prioritize."
    },
    
    # HIGH - Urgent needs affecting survival/basic needs
    "high": {
        "categories": ["water", "food", "shelter", "medical_products", "security", "military"],
        "color": "🟠",
        "level": "HIGH",
        "recommendation": "📢 Urgent. Allocate resources as soon as possible."
    },
    
    # MEDIUM - Infrastructure and service disruptions
    "medium": {
        "categories": ["buildings", "electricity", "transport", "hospitals", "shops", 
                      "aid_centers", "infrastructure_related", "storm", "floods"],
        "color": "🟡",
        "level": "MEDIUM",
        "recommendation": "📋 Moderate priority. Plan response within 24 hours."
    },
    
    # LOW - Miscellaneous or lower-priority aid requests
    "low": {
        "categories": ["clothing", "money", "other_aid", "other_infrastructure", 
                      "cold", "other_weather", "child_alone", "offer", "request"],
        "color": "🟢",
        "level": "LOW",
        "recommendation": "✅ Low priority. Log and address when resources available."
    }
}


def calculate_severity(predictions_dict):
    """
    Calculate severity score based on predicted disaster categories.
    
    Args:
        predictions_dict: Dictionary of {category: prediction_value}
        
    Returns:
        dict: {
            'severity_level': str (CRITICAL/HIGH/MEDIUM/LOW),
            'severity_score': float (0-100),
            'color': str (emoji),
            'recommendation': str,
            'critical_categories': list,
            'affected_categories': list
        }
    """
    
    # Identify all predicted categories (where prediction = 1/True)
    predicted_categories = [cat for cat, pred in predictions_dict.items() if pred == 1]
    
    if not predicted_categories:
        return {
            'severity_level': 'NONE',
            'severity_score': 0,
            'color': '⚪',
            'recommendation': 'No disaster categories detected.',
            'critical_categories': [],
            'affected_categories': []
        }
    
    # Determine highest severity level based on predicted categories
    severity_level = 'low'
    
    for level in ['critical', 'high', 'medium']:  # Check in order of severity
        level_categories = SEVERITY_MAPPING[level]['categories']
        if any(cat in level_categories for cat in predicted_categories):
            severity_level = level
            break
    
    # Calculate severity score (0-100)
    # More critical categories = higher score
    severity_weights = {
        'critical': 25,
        'high': 15,
        'medium': 8,
        'low': 3
    }
    
    severity_score = 0
    for cat in predicted_categories:
        for level, categories in SEVERITY_MAPPING.items():
            if cat in categories['categories']:
                severity_score += severity_weights[level]
    
    severity_score = min(severity_score, 100)  # Cap at 100
    
    # Find which categories are the critical factors
    critical_cats = [cat for cat in predicted_categories 
                     if cat in SEVERITY_MAPPING['critical']['categories']]
    
    severity_info = SEVERITY_MAPPING[severity_level]
    
    return {
        'severity_level': severity_info['level'],
        'severity_score': severity_score,
        'color': severity_info['color'],
        'recommendation': severity_info['recommendation'],
        'critical_categories': critical_cats,
        'affected_categories': predicted_categories
    }


def format_severity_display(severity_info):
    """
    Format severity information for Streamlit display.
    
    Returns:
        str: Formatted HTML/markdown for display
    """
    return f"""
    {severity_info['color']} **{severity_info['severity_level']} PRIORITY**
    
    Severity Score: {severity_info['severity_score']}/100
    
    {severity_info['recommendation']}
    """
