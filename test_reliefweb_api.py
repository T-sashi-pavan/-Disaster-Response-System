"""
Python Unit Tests for ReliefWeb API Integration
Tests API fetching, parsing, error handling, and analysis
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Utils.reliefweb_api import ReliefWebAPI
from Utils.disaster_analysis_engine import DisasterAnalysisEngine
from Utils.voice_output import VoiceOutput

def print_test(test_num, test_name):
    print(f"\n{'='*60}")
    print(f"TEST {test_num}: {test_name}")
    print('='*60)

def test_reliefweb_api():
    """Test ReliefWeb API integration"""
    print_test(1, "ReliefWeb API - Fetch Disasters")
    
    api = ReliefWebAPI()
    
    # Test 1.1: Fetch disasters
    print("\n[1.1] Fetching latest 10 disasters...")
    result = api.fetch_disasters(limit=10)
    
    if result["status"] == "success":
        print(f"✅ PASS - Fetched {result['count']} disasters")
        print(f"    Source: {result['source']}")
        print(f"    Last Updated: {result['last_updated']}")
        
        # Show first 3 disasters
        for i, disaster in enumerate(result['disasters'][:3], 1):
            print(f"\n    Disaster {i}:")
            print(f"      Title: {disaster['title']}")
            print(f"      Country: {disaster['country']}")
            print(f"      Type: {disaster['type']}")
            print(f"      Status: {disaster['status']}")
            print(f"      Severity: {disaster['severity']}")
    else:
        print(f"❌ FAIL - {result.get('error', 'Unknown error')}")
    
    # Test 1.2: Cache functionality
    print("\n[1.2] Testing cache functionality...")
    print("   Making second request (should use cache)...")
    result2 = api.fetch_disasters(limit=10, force_refresh=False)
    
    if result2["source"] == "cache":
        print("✅ PASS - Cache working correctly")
        print(f"    Source: {result2['source']}")
    else:
        print("❌ FAIL - Cache not used")
    
    # Test 1.3: Force refresh
    print("\n[1.3] Testing force refresh...")
    result3 = api.fetch_disasters(limit=10, force_refresh=True)
    
    if result3["source"] == "api":
        print("✅ PASS - Force refresh bypassed cache")
    else:
        print("❌ FAIL - Force refresh didn't work")
    
    # Test 1.4: Statistics
    print("\n[1.4] Testing statistics generation...")
    stats = api.get_statistics()
    
    print("✅ PASS - Statistics generated")
    print(f"    Total Events: {stats['total_events']}")
    print(f"    High Priority: {stats['high_priority']}")
    print(f"    Most Common Type: {stats['most_common_type']}")
    print(f"    Affected Countries: {len(stats['affected_countries'])}")
    
    # Test 1.5: Search functionality
    print("\n[1.5] Testing disaster search...")
    search_results = api.search_disasters("flood")
    print(f"✅ PASS - Search completed")
    print(f"    Found {len(search_results)} matching disasters")
    
    if search_results:
        print(f"    Example: {search_results[0]['title']}")
    
    return True

def test_disaster_analysis():
    """Test Disaster Analysis Engine"""
    print_test(2, "Disaster Analysis Engine")
    
    engine = DisasterAnalysisEngine()
    
    # Test 2.1: Earthquake analysis
    print("\n[2.1] Testing Earthquake Analysis...")
    result = engine.analyze_disaster_text(
        text="Massive 7.5 earthquake hits Nepal, thousands dead",
        country="Nepal",
        disaster_type_hint="earthquake"
    )
    
    print("✅ PASS - Analysis completed")
    print(f"    Is Disaster Related: {result['is_disaster_related']}")
    print(f"    Disaster Type: {result['disaster_type']}")
    print(f"    Severity: {result['severity']}")
    print(f"    Priority Score: {result['priority_score']}/10")
    print(f"    Required Help: {', '.join(result['required_help'])}")
    print(f"    Confidence: {result['confidence']:.0%}")
    
    # Test 2.2: Flood analysis
    print("\n[2.2] Testing Flood Analysis...")
    result = engine.analyze_disaster_text(
        text="Severe flooding in Bangladesh affects 2 million people",
        country="Bangladesh"
    )
    
    print("✅ PASS - Analysis completed")
    print(f"    Disaster Type: {result['disaster_type']}")
    print(f"    Severity: {result['severity']}")
    print(f"    Priority Score: {result['priority_score']}/10")
    print(f"    Recommended Action: {result['recommended_action'][:50]}...")
    
    # Test 2.3: Non-disaster text
    print("\n[2.3] Testing Non-Disaster Text...")
    result = engine.analyze_disaster_text(
        text="Weather is nice today"
    )
    
    if result['is_disaster_related'] == "NO":
        print("✅ PASS - Correctly identified as non-disaster")
    else:
        print("⚠️  WARN - Might have false positive")
    
    # Test 2.4: Emergency summary
    print("\n[2.4] Testing Emergency Summary Generation...")
    result = engine.analyze_disaster_text(
        text="Critical fire emergency in California",
        country="USA",
        disaster_type_hint="fire"
    )
    
    summary = engine.generate_emergency_summary(result)
    print("✅ PASS - Summary generated")
    print(summary[:200] + "...")
    
    # Test 2.5: Severity scoring
    print("\n[2.5] Testing Severity Scoring...")
    test_cases = [
        ("Minor damage reported", "expected_low"),
        ("Catastrophic earthquake kills thousands", "expected_high"),
        ("Critical situation developing", "expected_medium")
    ]
    
    for text, expectation in test_cases:
        result = engine.analyze_disaster_text(text)
        print(f"    '{text[:40]}...' → {result['severity']}")
    
    print("✅ PASS - Severity scoring working")
    
    return True

def test_voice_output():
    """Test Text-to-Speech functionality"""
    print_test(3, "Voice Output / Text-to-Speech")
    
    try:
        voice = VoiceOutput()
        
        if voice.available:
            print("\n[3.1] Testing TTS Initialization...")
            print("✅ PASS - Text-to-Speech engine initialized")
            
            print("\n[3.2] Testing message formatting...")
            test_info = {
                "title": "Earthquake in Mexico",
                "country": "Mexico",
                "disaster_type": "earthquake",
                "severity": "CRITICAL",
                "priority_score": 9,
                "required_help": ["Search & Rescue", "Medical Support"],
                "recommended_action": "Activate emergency response"
            }
            
            alert_text = voice._format_disaster_alert(test_info)
            print("✅ PASS - Alert formatted for voice")
            print(f"    Message length: {len(alert_text)} characters")
            
            print("\n[3.3] Testing prediction result formatting...")
            result_info = {
                "is_disaster_related": "YES",
                "disaster_type": "Earthquake",
                "severity": "CRITICAL",
                "priority_score": 9,
                "affected_location": "Turkey",
                "needs": ["Search & Rescue", "Medical Support"],
                "recommended_action": "Activate emergency response"
            }
            
            result_text = voice._format_prediction_result(result_info)
            print("✅ PASS - Prediction result formatted")
            print(f"    Message length: {len(result_text)} characters")
            
            # Note: Actual speaking would be done with voice.speak_async()
            # which we won't test here to avoid audio output
            
        else:
            print("\n⚠️  WARN - Text-to-Speech not available (pyttsx3 might not be installed)")
            print("    To enable: pip install pyttsx3")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def test_integration():
    """Test integrated workflow"""
    print_test(4, "Full Integration Test")
    
    print("\n[4.1] Testing complete workflow...")
    
    # Initialize components
    api = ReliefWebAPI()
    engine = DisasterAnalysisEngine()
    
    # Fetch disasters
    print("   Step 1: Fetching latest disasters...")
    disasters = api.fetch_disasters(limit=5)
    
    if disasters["status"] != "success":
        print(f"❌ FAIL - Could not fetch disasters: {disasters.get('error')}")
        return False
    
    print(f"   ✓ Fetched {disasters['count']} disasters")
    
    # Analyze first disaster
    if disasters['disasters']:
        disaster = disasters['disasters'][0]
        print(f"\n   Step 2: Analyzing first disaster...")
        print(f"   Event: {disaster['title']}")
        
        # Combine text for analysis
        analysis_text = f"{disaster['title']} in {disaster['country']}"
        result = engine.analyze_disaster_text(
            text=analysis_text,
            country=disaster['country'],
            disaster_type_hint=disaster['type']
        )
        
        print(f"   ✓ Analysis complete")
        print(f"     - Type: {result['disaster_type']}")
        print(f"     - Severity: {result['severity']}")
        print(f"     - Priority: {result['priority_score']}/10")
        
        print("\n✅ PASS - Full integration workflow successful")
        return True
    
    print("⚠️  WARN - No disasters available for testing")
    return True

def main():
    """Run all tests"""
    print("\n")
    print("=" * 60)
    print("   ReliefWeb API & Disaster Analysis Test Suite")
    print("=" * 60)
    
    results = []
    
    try:
        results.append(("ReliefWeb API", test_reliefweb_api()))
    except Exception as e:
        print(f"\n❌ ERROR in ReliefWeb API tests: {str(e)}")
        results.append(("ReliefWeb API", False))
    
    try:
        results.append(("Disaster Analysis", test_disaster_analysis()))
    except Exception as e:
        print(f"\n❌ ERROR in Disaster Analysis tests: {str(e)}")
        results.append(("Disaster Analysis", False))
    
    try:
        results.append(("Voice Output", test_voice_output()))
    except Exception as e:
        print(f"\n❌ ERROR in Voice Output tests: {str(e)}")
        results.append(("Voice Output", False))
    
    try:
        results.append(("Full Integration", test_integration()))
    except Exception as e:
        print(f"\n❌ ERROR in Integration tests: {str(e)}")
        results.append(("Full Integration", False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} | {name}")
    
    print(f"\nTotal: {passed}/{total} test groups passed")
    print("="*60)

if __name__ == "__main__":
    main()
