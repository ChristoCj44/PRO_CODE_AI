import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_execution(lang, code, expected_substring):
    print(f"Testing {lang} execution...")
    try:
        # Mock request directly to handlers if server isn't running, but cleaner to assume server usage if we could.
        # Since I can't easily start the background server and query it in one go without complex async,
        # I will just import the internal modules to test logic directly.
        
        from backend.executor.runner import CodeRunner
        from backend.complexity.analyzer import ComplexityAnalyzer
        
        runner = CodeRunner()
        analyzer = ComplexityAnalyzer()
        
        res = runner.run(lang, code)
        comp = analyzer.analyze(lang, code)
        
        print(f"Output: {res.get('output', '').strip()}")
        print(f"Error: {res.get('error', '').strip()}")
        print(f"Complexity: {comp['time_complexity']}")
        
        if expected_substring in res.get('output', '') or expected_substring in res.get('error', ''):
            print("✅ Execution Passed")
        else:
            print("❌ Execution Failed")
            
        return comp
        
    except Exception as e:
        print(f"❌ Test Error: {e}")

if __name__ == "__main__":
    # Test Python
    test_execution("python", "print('Hello Python')", "Hello Python")
    
    # Test C++
    test_execution("cpp", 
                   "#include <iostream>\nint main(){ std::cout << \"Hello C++\"; return 0; }", 
                   "Hello C++")
                   
    # Test Infinity Loop
    print("\nTesting Infinite Loop detection...")
    test_execution("python", "while True: pass", "Execution Timed Out")
    
    # Test Complexity
    print("\nTesting Complexity Analysis...")
    comp = test_execution("python", "for i in range(10):\n    for j in range(10): pass", "")
    if "O(n^2)" in comp['time_complexity']:
         print("✅ Complexity Analysis Passed (O(n^2))")
    else:
         print(f"❌ Complexity Analysis Failed: Got {comp['time_complexity']}")
