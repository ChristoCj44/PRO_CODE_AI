import requests
import json
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.executor.runner import CodeRunner
from backend.complexity.analyzer import ComplexityAnalyzer

def verify_system():
    print("Verifying Python Code Runner...")
    runner = CodeRunner()
    res = runner.run("python", "print('Hello AI')")
    if "Hello AI" in res['output']:
        print("✅ Python Runner works")
    else:
        print(f"❌ Python Runner Failed: {res}")

    print("\nVerifying AI Analyzer Integration...")
    # This will likely return "key missing" or similar if no env var, which is fine, verifies integration
    analyzer = ComplexityAnalyzer()
    res = analyzer.analyze("python", "print('AI')")
    
    print(f"AI Response Keys: {list(res.keys())}")
    if 'suggestions' in res:
        print("✅ AI Analyzer Interface works (returned suggestions field)")
        print(f"Explanation Preview: {res['explanation']}")
    else:
        print("❌ AI Analyzer Interface missing keys")

if __name__ == "__main__":
    verify_system()
