#!/usr/bin/env python3
"""
Model & Data Initialization Script
Runs at app startup to download required models and data
"""

import os
import sys
import subprocess

def setup_spacy_model():
    """Download spacy English model if not present"""
    try:
        import spacy
        try:
            spacy.load("en_core_web_sm")
            print("✅ Spacy model already available")
            return True
        except OSError:
            print("⏳ Downloading spacy model (en_core_web_sm)...")
            subprocess.check_call([
                sys.executable, "-m", "spacy", "download", "en_core_web_sm",
                "--quiet"
            ])
            print("✅ Spacy model downloaded successfully")
            return True
    except Exception as e:
        print(f"⚠️ Warning: Could not load spacy model: {e}")
        return False

def setup_nltk_data():
    """Download required NLTK data"""
    try:
        import nltk
        required_nltk = ['punkt', 'wordnet', 'averaged_perceptron_tagger', 'omw-1.4']
        
        for item in required_nltk:
            try:
                nltk.data.find(f'tokenizers/{item}' if item == 'punkt' else f'corpora/{item}')
            except LookupError:
                print(f"⏳ Downloading NLTK data: {item}...")
                nltk.download(item, quiet=True)
        
        print("✅ NLTK data available")
        return True
    except Exception as e:
        print(f"⚠️ Warning: NLTK setup issue: {e}")
        return False

def main():
    """Run all initialization tasks"""
    print("\n" + "="*60)
    print("🚀 Initializing Disaster Response System")
    print("="*60 + "\n")
    
    print("📦 Checking dependencies...\n")
    
    # Setup models
    spacy_ok = setup_spacy_model()
    nltk_ok = setup_nltk_data()
    
    print("\n" + "="*60)
    if spacy_ok and nltk_ok:
        print("✅ All models initialized successfully!")
    else:
        print("⚠️ Some models had issues (app may have limited NER)")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
