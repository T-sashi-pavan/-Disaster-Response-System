#!/usr/bin/env python3
"""
Test script to verify all modules load correctly for Streamlit Cloud deployment
Run this to check if deployment will succeed
"""

import sys
print("Python version:", sys.version)
print("\nTesting imports...")

tests = [
    ("numpy", "import numpy"),
    ("pandas", "import pandas"),
    ("streamlit", "import streamlit"),
    ("sklearn", "from sklearn.naive_bayes import MultinomialNB"),
    ("nltk", "import nltk"),
    ("folium", "import folium"),
    ("tinydb", "import tinydb"),
    ("feedparser", "import feedparser"),
    ("pyttsx3", "import pyttsx3"),
    ("fuzzywuzzy", "from fuzzywuzzy import fuzz"),
    ("requests", "import requests"),
]

failed = []
for name, import_stmt in tests:
    try:
        exec(import_stmt)
        print(f"  ✅ {name}")
    except Exception as e:
        print(f"  ❌ {name}: {e}")
        failed.append(name)

print("\nTesting spacy (optional)...")
try:
    import spacy
    print(f"  ✅ spacy module")
    try:
        spacy.load("en_core_web_sm")
        print(f"  ✅ spacy model (en_core_web_sm)")
    except OSError:
        print(f"  ⚠️  spacy module present but model not loaded (will be downloaded on first use)")
except Exception as e:
    print(f"  ⚠️  spacy not available: {e}")

print("\nTesting local modules...")
try:
    sys.path.insert(0, ".")
    from Utils.disaster_data_aggregator import DisasterDataAggregator
    print(f"  ✅ DisasterDataAggregator")
except Exception as e:
    print(f"  ❌ DisasterDataAggregator: {e}")
    failed.append("DisasterDataAggregator")

try:
    from Utils.disaster_map import DisasterMap
    print(f"  ✅ DisasterMap")
except Exception as e:
    print(f"  ❌ DisasterMap: {e}")
    failed.append("DisasterMap")

try:
    from Utils.helpline_database import DisasterHelplineDatabase
    print(f"  ✅ DisasterHelplineDatabase")
except Exception as e:
    print(f"  ❌ DisasterHelplineDatabase: {e}")
    failed.append("DisasterHelplineDatabase")

try:
    from Utils.disaster_analysis_engine import DisasterAnalysisEngine
    print(f"  ✅ DisasterAnalysisEngine")
except Exception as e:
    print(f"  ❌ DisasterAnalysisEngine: {e}")
    failed.append("DisasterAnalysisEngine")

print("\n" + "="*60)
if not failed:
    print("✅ All critical imports successful! Ready for Streamlit Cloud deployment")
    sys.exit(0)
else:
    print(f"❌ Failed imports: {', '.join(failed)}")
    print("Please install missing dependencies")
    sys.exit(1)
